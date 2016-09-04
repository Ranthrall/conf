# alsi -ub -f
export GPG_TTY=`tty`
export XDG_CONFIG_HOME="$HOME"/.config
alias diff='colordiff'              # requires colordiff package
alias grep='grep --color=auto'
alias more='less'
alias mkdir='mkdir -p -v'
# Privileged access
if [ `id -u` -ne 0 ]; then
    alias sudo='sudo '
    alias reboot='sudo systemctl reboot'
    alias poweroff='sudo systemctl poweroff'
fi
alias ls='ls -hFBX --color=auto --group-directories-first'
alias lr='ls -R'                    # recursive ls
alias ll='ls -l'
alias la='ll -A'
alias lx='ll -BX'                   # sort by extension
alias lz='ll -rS'                   # sort by size
alias lt='ll -rt'                   # sort by date
alias lm='la | more'
alias cp='cp -iv'
alias mv='mv -iv'
alias rm='rm -iv'                    # 'rm -i' prompts for every file
alias ln='ln -i'
alias chown='chown --preserve-root'
alias chmod='chmod --preserve-root'
alias chgrp='chgrp --preserve-root'
alias yau="yaourt -S"						# default action	- install one or more packages
alias yauu="yaourt -Syu"					# '[u]pdate'		- upgrade all packages to their newest version
alias yaur="yaourt -Rcns"					# '[r]emove'		- uninstall one or more packages
alias yauro="yaourt -Rcns $(yaourt -Qqdt)"	# '[r]remove [o]rphans'	- remove all packages which are orphaned
