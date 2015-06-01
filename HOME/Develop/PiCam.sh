#!/usr/bin/bash

ssh root@192.168.1.105 /root/camera.sh
sleep 1
rsync -avz -e ssh root@192.168.1.105:camera/ picam/
