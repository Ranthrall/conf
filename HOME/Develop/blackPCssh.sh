#!/bin/sh
tmux renamew "SuperICE SSH"
ssh blackice@pc.craft.net.br -p 2200
tmux setw automatic-rename on > /dev/null 2>&1
