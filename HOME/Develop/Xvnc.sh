#!/usr/bin/bash

x0vncserver -passwordFile=~/.vnc/passwd -AcceptPointerEvents=off -QueryConnect=on > ~/Xvnc.log 2>&1 &

