#!/usr/bin/python

# Radio code by Average Man (AverageManVsRaspberryPi.Blogspot.com)
#
# You'll need to map your buttons with the same GPIO pins as the code here
# You'll also need to use 'mpc add' to add stations to your playlist
# You need an IFTTT account and recipe to make the evernote/tweet buttons work (see my blog)
# If you have different stations to me (Indie etc), you'll need to change the names in the code
# Add a comment to my blog if you get stuck (AverageManVsRaspberryPi.Blogspot.com)
#
# Probably too much here to work out easily without a tutorial - once I complete my Plywood case I'll do a FULL tutorial.



# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN! We do not want the LCD to send anything to the Pi @ 5v
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V
# 16: LCD Backlight GND


#import
import RPi.GPIO as GPIO
import time
import os
import subprocess
import socket
import fcntl
import struct
import datetime
import smtplib
from email.mime.text import MIMEText

# Define GPIO to LCD mapping
LCD_RS = 17
LCD_E  = 18
LCD_D4 = 27
LCD_D5 = 22
LCD_D6 = 23
LCD_D7 = 24

# Define GPIO for button Controls

OFF = 25
VOLDWN = 4
VOLUP = 10
PREV = 9
PAUSE =11
PLAY = 8
NEXT = 7
IPSHOW = 14

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def main():
  GPIO.cleanup()
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  GPIO.setup(NEXT, GPIO.IN) # Next Channel button
  GPIO.setup(PAUSE, GPIO.IN) # Stop button
  GPIO.setup(PLAY, GPIO.IN) # Start button
  GPIO.setup(PREV, GPIO.IN) # Previous Channel button
  GPIO.setup(OFF, GPIO.IN) # OFF button
  GPIO.setup(VOLDWN, GPIO.IN) # Volume down button
  GPIO.setup(VOLUP, GPIO.IN) # Volume up button
  GPIO.setup(IPSHOW, GPIO.IN) # Show IP button

  # Initialise display
  lcd_init()

  # Send some test
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Average Man's",2)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("NERDBOX!",2)
  time.sleep(1)
  menu()



def menu():
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mystring = ""
    mytime = ""
    mytemp = ""
    pretemp = "NBX ["
    posttemp = "] "
    f=os.popen("date")
    for i in f.readlines():
     mytime += i
     mytime = mytime[11:-13]
     f=os.popen("/opt/vc/bin/vcgencmd measure_temp")
     for i in f.readlines():
      mytemp += i
      mytemp = mytemp[5:-3]
      mystring = pretemp + mytemp + posttemp + mytime
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string(mystring,1)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string("< Off     Menu >",2)
   else:
    if ( GPIO.input(NEXT) == False):
     menu1()
    if ( GPIO.input(PREV) == False):
     off()

def menu1(): #iRadio
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mystring = ""
    mytime = ""
    mytemp = ""
    pretemp = "NBX ["
    posttemp = "] "
    f=os.popen("date")
    for i in f.readlines():
     mytime += i
     mytime = mytime[11:-13]
     f=os.popen("/opt/vc/bin/vcgencmd measure_temp")
     for i in f.readlines():
      mytemp += i
      mytemp = mytemp[5:-3]
      mystring = pretemp + mytemp + posttemp + mytime
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string(mystring,1)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string("[GO]  < iRadio >",2)
   else:
    if ( GPIO.input(PREV) == False):
     chooseradio()
    if ( GPIO.input(PLAY) == False):
     menu()
    if ( GPIO.input(NEXT) == False):
     menu2()


def menu2(): #IP
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mystring = ""
    mytime = ""
    mytemp = ""
    pretemp = "NBX ["
    posttemp = "] "
    f=os.popen("date")
    for i in f.readlines():
     mytime += i
     mytime = mytime[11:-13]
     f=os.popen("/opt/vc/bin/vcgencmd measure_temp")
     for i in f.readlines():
      mytemp += i
      mytemp = mytemp[5:-3]
      mystring = pretemp + mytemp + posttemp + mytime
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string(mystring,1)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string("[GO]      < IP >",2)
   else:
    if ( GPIO.input(PREV) == False):
     ip()
    if ( GPIO.input(PLAY) == False):
     menu1()
    if ( GPIO.input(NEXT) == False):
     menu3()

def menu3():#Tweet
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mystring = ""
    mytime = ""
    mytemp = ""
    pretemp = "NBX ["
    posttemp = "] "
    f=os.popen("date")
    for i in f.readlines():
     mytime += i
     mytime = mytime[11:-13]
     f=os.popen("/opt/vc/bin/vcgencmd measure_temp")
     for i in f.readlines():
      mytemp += i
      mytemp = mytemp[5:-3]
      mystring = pretemp + mytemp + posttemp + mytime
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string(mystring,1)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string("[GO]    < Tweet ",2)
   else:
    if ( GPIO.input(PREV) == False):
     tweetemail()
    if ( GPIO.input(PLAY) == False):
     menu2()

def ip():
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mystring = ""
    mytime = ""
    mytemp = ""
    pretemp = "NBX ["
    posttemp = "] "
    f=os.popen("date")
    for i in f.readlines():
     mytime += i
     mytime = mytime[11:-13]
     f=os.popen("/opt/vc/bin/vcgencmd measure_temp")
     for i in f.readlines():
      mytemp += i
      mytemp = mytemp[5:-3]
      mystring = pretemp + mytemp + posttemp + mytime
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string(mystring,1)
      preIP = "IP "
      address = get_ip_address('wlan0')
      address = preIP + address
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(address,1)
      time.sleep(2.5)
      menu2()

def station1():
  os.system("mpc play 1")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<Country>  "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[84:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station12()
      if ( GPIO.input(PAUSE) == False):
       station2()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station2():
  os.system("mpc play 2")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<Covers>   "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[46:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station1()
      if ( GPIO.input(PAUSE) == False):
       station3()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station3():
  os.system("mpc play 3")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<Beat>     "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[76:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station2()
      if ( GPIO.input(PAUSE) == False):
       station4()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station4():
  os.system("mpc play 4")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<Indie>    "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[44:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station3()
      if ( GPIO.input(PAUSE) == False):
       station5()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station5():
  os.system("mpc play 5")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<80's>     "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[66:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station4()
      if ( GPIO.input(PAUSE) == False):
       station6()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station6():
  os.system("mpc play 6")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<Groove>   "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[77:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station5()
      if ( GPIO.input(PAUSE) == False):
       station7()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station7():
  os.system("mpc play 7")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<LushFM>   "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[67:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station6()
      if ( GPIO.input(PAUSE) == False):
       station8()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station8():
  os.system("mpc play 8")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<DubStep>  "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[91:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station7()
      if ( GPIO.input(PAUSE) == False):
       station9()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station9():
  os.system("mpc play 9")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<Jazz>     "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[15:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station8()
      if ( GPIO.input(PAUSE) == False):
       station10()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station10():
  os.system("mpc play 10")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<BMarley>  "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[11:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station9()
      if ( GPIO.input(PAUSE) == False):
       station11()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station11():
  os.system("mpc play 11")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<SlowJam>  "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[9:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station10()
      if ( GPIO.input(PAUSE) == False):
       station12()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def station12():
  os.system("mpc play 12")
  time.sleep(0.4)
  while(1):
   f=os.popen("date")
   for i in f.readlines():
    mytime = ""
    pretime = "<CDelMar>  "
    mytime += i
    mytime = mytime[11:-13]
    mytime = pretime + mytime
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(mytime,1)
    f=os.popen("mpc current")
    for i in f.readlines():
     station = ""
     station += i
     str_pad = " " * 16
     station = station[13:-1]
     station = str_pad + station
     for i in range (0, len(station)):
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_text = station[i:(i+16)]
      lcd_string(lcd_text,1)
      time.sleep(0.2)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(str_pad,1)
      if ( GPIO.input(IPSHOW) == True):
       evernote()
      if ( GPIO.input(PREV) == False):
       station11()
      if ( GPIO.input(PAUSE) == False):
       station1()
      if ( GPIO.input(NEXT) == False):
       os.system("mpc stop")
       menu1()

def chooseradio():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station1()
   if ( GPIO.input(PLAY) == False):
    choose12()
   if ( GPIO.input(NEXT) == False):
    choose2()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO] < Country >",2)



def choose2():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station2()
   if ( GPIO.input(PLAY) == False):
    chooseradio()
   if ( GPIO.input(NEXT) == False):
    choose3()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO]  < Covers >",2)

def choose3():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station3()
   if ( GPIO.input(PLAY) == False):
    choose2()
   if ( GPIO.input(NEXT) == False):
    choose4()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO]    < Beat >",2)

def choose4():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station4()
   if ( GPIO.input(PLAY) == False):
    choose3()
   if ( GPIO.input(NEXT) == False):
    choose5()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO]   < Indie >",2)

def choose5():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station5()
   if ( GPIO.input(PLAY) == False):
    choose4()
   if ( GPIO.input(NEXT) == False):
    choose6()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO]    < 80's >",2)

def choose6():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station6()
   if ( GPIO.input(PLAY) == False):
    choose5()
   if ( GPIO.input(NEXT) == False):
    choose7()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO]  < Groove >",2)

def choose7():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station7()
   if ( GPIO.input(PLAY) == False):
    choose6()
   if ( GPIO.input(NEXT) == False):
    choose8()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO]  < LushFM >",2)

def choose8():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station8()
   if ( GPIO.input(PLAY) == False):
    choose7()
   if ( GPIO.input(NEXT) == False):
    choose9()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO] < DubStep >",2)

def choose9():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station9()
   if ( GPIO.input(PLAY) == False):
    choose8()
   if ( GPIO.input(NEXT) == False):
    choose10()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO]    < Jazz >",2)

def choose10():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station10()
   if ( GPIO.input(PLAY) == False):
    choose9()
   if ( GPIO.input(NEXT) == False):
    choose11()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO] < BMarley >",2)

def choose11():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station11()
   if ( GPIO.input(PLAY) == False):
    choose10()
   if ( GPIO.input(NEXT) == False):
    choose12()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO] < SlowJam >",2)

def choose12():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    station12()
   if ( GPIO.input(PLAY) == False):
    choose11()
   if ( GPIO.input(NEXT) == False):
    chooseradio()
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string(" Choose Station ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("[GO] < CDelMar >",2)

def tweetemail():
  temp1 = ""
  f=os.popen("/opt/vc/bin/vcgencmd measure_temp")
  for i in f.readlines():
   temp1 += i
   pretemp = " Pi temperature is "
   temp1 = temp1[5:]
   temp1 = pretemp + temp1
   #Gmail account details
   USERNAME = "YOURGMAILADDRESS@gmail.com" #Your gmail email address
   PASSWORD = "YOURGMAILPASSWORD" # your gmail password
   MAILTO  = "trigger@ifttt.com" # IFTTT standard email trigger address
   #Email content
   msg = MIMEText(temp1)
   msg['Subject'] = "#RaspberryPi GPIO button tweeting from my Raspberry Pi Internet Radio -"
   msg['From'] = USERNAME
   msg['To'] = MAILTO
   #Server stuff
   server = smtplib.SMTP('smtp.gmail.com:587')
   server.ehlo_or_helo_if_needed()
   server.starttls()
   server.ehlo_or_helo_if_needed()
   server.login(USERNAME,PASSWORD)
   server.sendmail(USERNAME, MAILTO, msg.as_string())
   server.quit()
   #LCD Message
   time.sleep(0.5)
   lcd_byte(LCD_LINE_1, LCD_CMD)
   lcd_string("NERDBOX",2)
   lcd_byte(LCD_LINE_2, LCD_CMD)
   lcd_string("HAS TWEETED!",2)
   time.sleep(1)
   menu3()

def evernote():
  f=os.popen("echo 'currentsong' | nc localhost 6600 | grep -e '^Title: '")
  tracknow = ""
  for i in f.readlines():
   tracknow += i
   tracknow = tracknow[7:]
   #Gmail account details
   USERNAME = "YOURGMAILADDRESS@gmail.com"
   PASSWORD = "YOURGMAILPASSWORD"
   MAILTO  = "trigger@ifttt.com"
   #Email content
   msg = MIMEText(tracknow)
   msg['Subject'] = "#song New song to record"
   msg['From'] = USERNAME
   msg['To'] = MAILTO
   #Server stuff
   server = smtplib.SMTP('smtp.gmail.com:587')
   server.ehlo_or_helo_if_needed()
   server.starttls()
   server.ehlo_or_helo_if_needed()
   server.login(USERNAME,PASSWORD)
   server.sendmail(USERNAME, MAILTO, msg.as_string())
   server.quit()
   #LCD Message
   lcd_byte(LCD_LINE_2, LCD_CMD)
   lcd_string("SENT",2)
   time.sleep(0.3)
   lcd_byte(LCD_LINE_2, LCD_CMD)
   lcd_string("",2)
   time.sleep(0.3)
   lcd_byte(LCD_LINE_2, LCD_CMD)
   lcd_string("TO",2)
   time.sleep(0.3)
   lcd_byte(LCD_LINE_2, LCD_CMD)
   lcd_string("",2)
   time.sleep(0.3)
   lcd_byte(LCD_LINE_2, LCD_CMD)
   lcd_string("EVERNOTE",2)
   time.sleep(0.6)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])

def off():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    menu()
   if ( GPIO.input(NEXT) == False):
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Shutting Down   ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("                ",2)
    time.sleep(0.5)
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Shutting Down.  ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("                ",2)
    time.sleep(0.5)
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Shutting Down.. ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("                ",2)
    time.sleep(0.5)
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Shutting Down...",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("                ",2)
    time.sleep(0.5)
    os.system("sudo halt")
    time.sleep(8)
   else:
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("   Shut down?   ",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("< No       Yes >",2)


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

if __name__ == '__main__':
  main()
