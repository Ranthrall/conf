#
# /etc/bash.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return


## Se conexão via SSH, executar o screen ou tmux?! Haha

#if [[ -z "$TMUX" ]] ;then
#    ID="`tmux ls | grep -vm1 attached | cut -d: -f1`" # get the id of a deattached session
#    if [[ -z "$ID" ]] ;then
#        tmux new-session && exit
#    else
#        tmux attach-session -t "$ID" && exit
#    fi
#fi

[ ! -z "$SSH_TTY" ] && [ -z "$STY" ] && exec screen -xRR sshpi
##[ -z "$STY" ] && exec screen -xRR sshpi

##Para o Pi
[ "$TERM" == "screen" ] && alias exit='screen -X detach' 
#[ ! -z "$TMUX" ] && alias exit='tmux detach-client'

echo -e "\033[1;32m
    .~~.   .~~.
   '. \\ ' ' / .'\033[1;32m      ____             _                   ____  \033[1;31m
    .~ .~~~..~.    \033[1;32m  | __ |           | |                 | _  |_ \033[1;31m
   : .~.'~'.~. :   \033[1;32m  |   _|___ ___ ___| |_ ___ ___ ___ _ _|  __|_|\033[1;31m
  ~ (   ) (   ) ~  \033[1;32m  |    | .'|_ -| . | . | -_|  _|  _| | | |  | |\033[1;31m
 ( : '~'.~.'~' : ) \033[1;32m  |_|__|__,|___|  _|___|___|_| |_| |_  |_|  |_|\033[1;31m
  ~ .~ (   ) ~. ~  \033[1;32m               | |      \033[1;31mby BlackICE\033[1;32m _| |\033[1;31m
   (  : '~' :  )   \033[1;32m               |_|                 |___|      \033[1;31m
    '~ .~~~. ~'
        '~'
 Welcome to BlackPi\e[0m
"
uname -norms
date

# Definir VIM como editor padrão
export EDITOR=/usr/bin/vim

## Modified commands ## {{{
alias diff='colordiff'              # requires colordiff package
alias grep='grep --color=auto'
alias more='less'
alias df='df -h'
alias du='du -c -h'
alias mkdir='mkdir -p -v'
alias nano='nano -w'
alias ping='ping -c 5'
alias dmesg='dmesg -HL'
# }}}

## New commands ## {{{
alias da='date "+%A, %B %d, %Y [%T]"'
alias du1='du --max-depth=1'
alias hist='history | grep'         # requires an argument
alias openports='ss --all --numeric --processes --ipv4 --ipv6'
alias pgg='ps -Af | grep'           # requires an argument
alias ..='cd ..'
alias reload='source /etc/bash.bashrc'
# }}}

## ls ## {{{
alias ls='ls -hFBX --color=auto --group-directories-first'
alias lr='ls -R'                    # recursive ls
alias ll='ls -l'
alias la='ll -A'
alias lx='ll -BX'                   # sort by extension
alias lz='ll -rS'                   # sort by size
alias lt='ll -rt'                   # sort by date
alias lm='la | more'
# }}}

## Safety features ## {{{
alias cp='cp -iv'
alias mv='mv -iv'
alias rm='rm -iv'                    # 'rm -i' prompts for every file
# safer alternative w/ timeout, not stored in history
#alias rm=' timeout 3 rm -Iv --one-file-system'
alias ln='ln -i'
alias chown='chown --preserve-root'
alias chmod='chmod --preserve-root'
alias chgrp='chgrp --preserve-root'
alias cls=" echo -ne \"\033c\""       # clear screen for real (it does not work in Terminology)
# }}}

## Yaourt aliases ## {{{
alias yau="yaourt -S"						# default action	- install one or more packages
alias yauu="yaourt -Syu"					# '[u]pdate'		- upgrade all packages to their newest version
alias yaur="yaourt -Rcns"					# '[r]emove'		- uninstall one or more packages
alias yaus="yaourt -Ss"						# '[s]earch'		- search for a package using one or more keywords
alias yaui="yaourt -Si"						# '[i]nfo'		- show information about a package
alias yaulo="yaourt -Qqdt"					# '[l]ist [o]rphans'	- list all packages which are orphaned
alias yauc="yaourt -Scc"					# '[c]lean cache'	- delete all not currently installed package files
alias yaulf="yaourt -Ql"					# '[l]ist [f]iles'	- list all files installed by a given package
alias yauexpl="yaourt -D --asexp"			# 'mark as [expl]icit'	- mark one or more packages as explicitly installed 
alias yauimpl="yaourt -D --asdep"			# 'mark as [impl]icit'	- mark one or more packages as non explicitly installed

#case ${TERM} in
#  xterm*|rxvt*|Eterm|aterm|kterm|gnome*)
#    PROMPT_COMMAND=${PROMPT_COMMAND:+$PROMPT_COMMAND; }'printf "\033]0;%s@%s:%s\007" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/\~}"'
#
#    ;;
#  screen)
#    PROMPT_COMMAND=${PROMPT_COMMAND:+$PROMPT_COMMAND; }'printf "\033_%s@%s:%s\033\\" "${USER}" "${HOSTNAME%%.*}OI?" "${PWD/#$HOME/\~}"'
#    ;;
#esac

[ -r /usr/share/bash-completion/bash_completion   ] && . /usr/share/bash-completion/bash_completion

# Reset
Color_Off='\e[0m'       # Text Reset

# Regular Colors
Black='\e[0;30m'        # Black
Red='\e[0;31m'          # Red
Green='\e[0;32m'        # Green
Yellow='\e[0;33m'       # Yellow
Blue='\e[0;34m'         # Blue
Purple='\e[0;35m'       # Purple
Cyan='\e[0;36m'         # Cyan
White='\e[0;37m'        # White

# Bold
BBlack='\e[1;30m'       # Black
BRed='\e[1;31m'         # Red
BGreen='\e[1;32m'       # Green
BYellow='\e[1;33m'      # Yellow
BBlue='\e[1;34m'        # Blue
BPurple='\e[1;35m'      # Purple
BCyan='\e[1;36m'        # Cyan
BWhite='\e[1;37m'       # White

# Underline
UBlack='\e[4;30m'       # Black
URed='\e[4;31m'         # Red
UGreen='\e[4;32m'       # Green
UYellow='\e[4;33m'      # Yellow
UBlue='\e[4;34m'        # Blue
UPurple='\e[4;35m'      # Purple
UCyan='\e[4;36m'        # Cyan
UWhite='\e[4;37m'       # White

# Background
On_Black='\e[40m'       # Black
On_Red='\e[41m'         # Red
On_Green='\e[42m'       # Green
On_Yellow='\e[43m'      # Yellow
On_Blue='\e[44m'        # Blue
On_Purple='\e[45m'      # Purple
On_Cyan='\e[46m'        # Cyan
On_White='\e[47m'       # White

# High Intensity
IBlack='\e[0;90m'       # Black
IRed='\e[0;91m'         # Red
IGreen='\e[0;92m'       # Green
IYellow='\e[0;93m'      # Yellow
IBlue='\e[0;94m'        # Blue
IPurple='\e[0;95m'      # Purple
ICyan='\e[0;96m'        # Cyan
IWhite='\e[0;97m'       # White

# Bold High Intensity
BIBlack='\e[1;90m'      # Black
BIRed='\e[1;91m'        # Red
BIGreen='\e[1;92m'      # Green
BIYellow='\e[1;93m'     # Yellow
BIBlue='\e[1;94m'       # Blue
BIPurple='\e[1;95m'     # Purple
BICyan='\e[1;96m'       # Cyan
BIWhite='\e[1;97m'      # White

# High Intensity backgrounds
On_IBlack='\e[0;100m'   # Black
On_IRed='\e[0;101m'     # Red
On_IGreen='\e[0;102m'   # Green
On_IYellow='\e[0;103m'  # Yellow
On_IBlue='\e[0;104m'    # Blue
On_IPurple='\e[0;105m'  # Purple
On_ICyan='\e[0;106m'    # Cyan
On_IWhite='\e[0;107m'   # White

PS1="\n$IRed\l-$Color_Off(\t)-[\u@\h:\w]\$ "
PS2='> '
PS3='> '
PS4='+ '

#END
