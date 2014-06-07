#!/bin/bash
test "$1" == "" && echo "Qual WM iniciar?!" && exit 1
Xephyr -name TEST -ac -br -noreset -screen 1024x768 :1 >/dev/null 2>&1 &
sleep 1
DISPLAY=:1.0 $1 &

