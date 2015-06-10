#!/bin/sh
# 06/2015 - AcidHub <acidhub@craft.net.br>
if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi

nvidia-settings --load-config-only

if test -d /etc/profile.d/; then
    for profile in /etc/profile.d/*.sh; do
        test -r "$profile" && . "$profile"
    done
    unset profile
fi

#Come back .Xresources!!!
[[ -f ~/.Xresources ]] && xrdb -merge ~/.Xresources

exec startxfce4
