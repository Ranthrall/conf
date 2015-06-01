#!/bin/sh
tmux renamew "Amora SSH"
ssh lara@192.168.0.16
tmux setw automatic-rename on > /dev/null 2>&1
