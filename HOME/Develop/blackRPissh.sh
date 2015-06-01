#!/bin/sh
tmux renamew "BlackRPi SSH"
ssh -p 220 pc.craft.net.br
tmux setw automatic-rename on > /dev/null 2>&1
