#
# ~/.bashrc
#

# Check if interactive
[ -z "$PS1" ] && return

# Check if user is my beaultyful, fantastic, cute, stunning, angel of my life laracraft304
test `whoami` == laracraft304 && return

# Se conexão via SSH, executar o screen
[ ! -z "$SSH_TTY" ] && [ -z "$STY" ] && exec screen

# Ativar completações do bash
source /usr/share/bash-completion/bash_completion

# Ativar o gancho "command-not-found" do pkgfile
source /usr/share/doc/pkgfile/command-not-found.bash

#cowsay
#command fortune -a | fmt -80 -s | $(shuf -n 1 -e cowsay cowthink) -$(shuf -n 1 -e b d g p s t w y) -f $(shuf -n 1 -e $(cowsay -l | tail -n +2)) -n

#alsi
alsi -ub -f

# Definir VIM como editor padrão
export EDITOR=/usr/bin/vim

# XDG
export XDG_CONFIG_HOME="$HOME"/.config

# Aliases
## by LaraCraft304 ##
alias yaourt='yaourt_wrapper'
alias geany='geany_checkpath'
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

# Privileged access
if [ `id -u` -ne 0 ]; then
    alias sudo='sudo '
    alias reboot='sudo systemctl reboot'
    alias poweroff='sudo systemctl poweroff'
fi

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
alias yau="yaourt_wrapper -S"						# default action	- install one or more packages
alias yauu="yaourt_wrapper -Syu"					# '[u]pdate'		- upgrade all packages to their newest version
alias yaur="yaourt_wrapper -Rcns"					# '[r]emove'		- uninstall one or more packages
alias yaus="yaourt_wrapper -Ss"						# '[s]earch'		- search for a package using one or more keywords
alias yaui="yaourt_wrapper -Si"						# '[i]nfo'		- show information about a package
alias yaulo="yaourt_wrapper -Qqdt"					# '[l]ist [o]rphans'	- list all packages which are orphaned
alias yauc="yaourt_wrapper -Scc"					# '[c]lean cache'	- delete all not currently installed package files
alias yaulf="yaourt_wrapper -Ql"					# '[l]ist [f]iles'	- list all files installed by a given package
alias yauexpl="yaourt_wrapper -D --asexp"			# 'mark as [expl]icit'	- mark one or more packages as explicitly installed 
alias yauimpl="yaourt_wrapper -D --asdep"			# 'mark as [impl]icit'	- mark one or more packages as non explicitly installed
alias yauro="yaourt_wrapper -Orphans"

extract() {
    local c e i

    (($#)) || return

    for i; do
        c=''
        e=1

        if [[ ! -r $i ]]; then
            echo "$0: file is unreadable: \`$i'" >&2
            continue
        fi

        case $i in
            *.t@(gz|lz|xz|b@(2|z?(2))|a@(z|r?(.@(Z|bz?(2)|gz|lzma|xz)))))
                   c='bsdtar xvf';;
            *.7z)  c='7z x';;
            *.Z)   c='uncompress';;
            *.bz2) c='bunzip2';;
            *.exe) c='cabextract';;
            *.gz)  c='gunzip';;
            *.rar) c='unrar x';;
            *.xz)  c='unxz';;
            *.zip) c='unzip';;
            *)     echo "$0: unrecognized file extension: \`$i'" >&2
                   continue;;
        esac

        command $c "$i"
        e=$?
    done

    return $e
}

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

PS1="\n\
$BWhite($(if [ `id -u` -eq 0 ]; then echo "\
$BRed ROOT "; else echo "\
$BBlue\u@\h"; fi)\
$BWhite)─(\$(if [ \$? -eq 0 ]; then echo '\
$BGreen\342\234\223'; else echo '\
$BRed\342\234\227'; fi)\
$BWhite)─(\
$BGreen\w\
$BWhite)─> \
$Color_Off"
