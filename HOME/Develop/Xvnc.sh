#!/usr/bin/bash

x0vncserver -passwordFile=/home/blackice/.vnc/passwd -AcceptPointerEvents=off -QueryConnect=on > /home/blackice/Xvnc.log 2>&1 &

