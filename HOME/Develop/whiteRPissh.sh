#!/bin/sh
tmux renamew "WhiteRPi SSH"
ssh pc.craft.net.br -p 2200
tmux setw automatic-rename on > /dev/null 2>&1
