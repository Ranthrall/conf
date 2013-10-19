#!/bin/sh
# Lara Maia © 2012 ~ 2013 <lara@craft.net.br>
# Mod by BlackXT <blackice@craft.net.br>
# version: 0.1

test $(id -u) == 0 && echo "EPA" && exit 1
test "$1" == "" && echo "Forneça a mensagem do commit" && exit 1

function checkfiles() {
	for file in ${FILES[@]}; do
		
		# if is $home
		if [ ${file:0:${#HOME}} == "$HOME" ]; then
			dest=HOME${file:${#HOME}}
		elif [ ${file:0:1} == "/" ]; then
			dest=${file:1}
		fi
		
		if [ -f "$file" ]; then
		
			# Prevent destination not found
			test ! -f "$dest" && mkdir -p ${dest%/*} && touch $dest
			
			if ! colordiff -u "$dest" "$file"; then
				while true; do
					echo -ne "==> [C]opiar, [R]estaurar, [I]gnorar, [S]air: "
					read -n 1 opc
					
					case $opc in
						C|c) echo "==> Fazendo backup de '$file'"
						     cp -f "$file" "$dest" && echo -e "\n" && break || exit 1 ;;
						R|r) sudo cp -f "$dest" "$file" && echo -e "\n" && break || exit 1 ;;
						I|i) test -f $dest && rm $dest; echo -e "\n" && break ;;
						S|s|E|e) exit 1 ;;
						*) echo -ne " < Opção incorreta\r\n" && continue ;;
					esac
				done
			fi
		else
			echo -e "\n * O arquivo $file não existe no sistema de arquivos, ignorando."
		fi
	done
}

echo -n "Criando lista de arquivos arquivos... "

declare -x FILES=(

# HOME
${HOME}/.asoundrc
${HOME}/.asoundrc.asoundconf

# lxdm custom theme
/usr/share/lxdm/themes/BlackICE/background.png
/usr/share/lxdm/themes/BlackICE/COPYING
/usr/share/lxdm/themes/BlackICE/greeter.ui
/usr/share/lxdm/themes/BlackICE/gtkrc
/usr/share/lxdm/themes/BlackICE/panel.png
/usr/share/lxdm/themes/BlackICE/README 

# xfce4-notifyd custom theme
/usr/share/themes/BlackICE/xfce-notify-4.0/gtkrc

# /etc
/etc/bash.bashrc
/etc/fstab
/etc/makepkg.conf
/etc/yaourtrc
/etc/pacman.conf
/etc/pacman.d/mirrorlist
/etc/hostname
/etc/mkinitcpio.conf
/etc/netctl/icenet
/etc/lxdm/lxdm.conf
/etc/lightdm/lightdm.conf
/etc/lightdm/lightdm-gtk-greeter.conf
/etc/X11/xorg.conf

# udev
/etc/udev/rules.d/80-net-name-slot.rules

# boot
/boot/syslinux/syslinux.cfg

`find $HOME/.config/xfce4/panel -iname '*' -type f`

); echo -e "Concluído.\n"

echo -n "Verificando arquivos... "; checkfiles; echo -e "Concluído.\n"

echo -n "Construindo o commit..."; git commit -am "$1"; echo -e "Concluído.\n"

echo -n "Enviando commit"; git push; echo -e "Concluído.\n"

echo "Tarefa completada com sucesso!"
exit 0
