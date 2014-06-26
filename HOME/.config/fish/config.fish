# Cores para o grep, egrep e zgrep
set -x GREP_OPTIONS "--color=auto"

# XDG
set -x XDG_CONFIG_HOME "$HOME"/.config

#COLORS!!!!
set -x TERM screen-256color

#MOTD!
function fish_greeting -d "motd"
        echo -e "\e[1;31;40m  Welcome to BlackPi  
\e[1;32m     .~~.   .~~.      
\e[1;32m    '. \ ' ' / .'     
\e[1;31m     .~ .~~~..~.      
\e[1;31m    : .~.'~'.~. :     
\e[1;31m   ~ (   ) (   ) ~    
\e[1;31m  ( : '~'.~.'~' : )   
\e[1;31m   ~ .~ (   ) ~. ~    
\e[1;31m    (  : '~' :  )     
\e[1;31m     '~ .~~~. ~'      
\e[1;31m         '~'          
\e[1;32m      Have fun!       \e[0m"
	if test -z "$SSH_TTY"
		#alsi -ub -f
        uname -norms
        date
	else 
        #alsi -ub
        screen -X msgwait 5
        function exit; screen -X detach; end
        uname -norms
        date
        who
    end
end

### ALIASES
# Cores com grc
function configure; grc -es --colour=auto ./configure $argv; end
function make; grc -es --colour=auto make $argv; end
function gcc; grc -es --colour=auto gcc $argv; end
function g++; grc -es --colour=auto g++ $argv; end
function ld; grc -es --colour=auto ld $argv; end
function netstat; grc -es --colour=auto netstat $argv; end
function ping; grc -es --colour=auto ping -c 3 $argv; end
function traceroute; grc -es --colour=auto traceroute $argv; end
#
function gvim; gvim_checkpath $argv; end
function geany; geany_checkpath $argv; end
#
function diff; vimdiff $argv; end
function grep; /usr/bin/grep --color=auto $argv; end
function more; less $argv; end
function df; /usr/bin/df -h $argv; end
function du; /usr/bin/du -c -h $argv; end
function mkdir; /usr/bin/mkdir -p -v $argv; end
#function nano; /usr/bin/nano -w $argv; end
function vi; vim $argv; end
function dmesg; /usr/bin/dmesg -HL $argv; end
function du1; du --max-depth=1 $argv; end
function hist; history | grep $argv; end
function openports; ss --all --numeric --processes --ipv4 --ipv6 $argv; end
function pgg; ps -Af | grep $argv; end
function ..; cd .. $argv; end
function poweroff; sudo systemctl poweroff; end
function reboot; sudo systemctl reboot; end
function reload; . ~/.config/fish/config.fish; end
#LS
function ls; /usr/bin/ls -hFBX --color=auto --group-directories-first $argv; end
function lr; ls -R $argv; end
function ll; ls -l $argv; end
function la; ll -A $argv; end
function lx; ll -BX $argv; end
function lz; ll -rS $argv; end
function lt; ll -rt $argv; end
function lm; la | more $argv; end
#SEGURANÇA
function cp; /usr/bin/cp -iv $argv; end
function mv; /usr/bin/mv -iv $argv; end
function rm; /usr/bin/rm -iv $argv; end
function ln; /usr/bin/ln -i $argv; end
function chown; /usr/bin/chown --preserve-root $argv; end
function chmod; /usr/bin/chmod --preserve-root $argv; end
function chgrp; /usr/bin/chgrp --preserve-root $argv; end
#YAOURT
function yau; yaourt -S $argv; end
function yauu; yaourt -Syu $argv; end
function yaur; yaourt -Rcns $argv; end
function yaus; yaourt -Ss $argv; end
function yaui; yaourt -Si $argv; end
function yaulo; yaourt -Qqdt $argv; end
function yauc; yaourt -Scc $argv; end
function yaulf; yaourt -Ql $argv; end
function yauexpl; yaourt -D --asexp $argv; end
function yauimpl; yaourt -D --asdep $argv; end


#PROMPT
function fish_prompt -d "Write out the prompt"
    set laststatus $status
    set_color -b black
    printf '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s'\
    (set_color -o white)               \
    '❰'                                \
    (set_color green)                  \
    $USER                              \
    (set_color white)                  \
    '@'                                \
    (set_color blue)                   \
    (hostname)                         \
    (set_color white)                  \
    '❙'                                \
    (set_color yellow)                 \
    (echo $PWD | sed -e "s|^$HOME|~|") \
    (set_color white)                  \
    '❱'                                \
    (set_color white)
    if test $laststatus -eq 0
        printf "%s✔%s≻%s " \
        (set_color -o green)\
        (set_color white)   \
        (set_color normal)
    else
        printf "%s✘%s≻%s " \
        (set_color -o red)  \
        (set_color white)   \
        (set_color normal)
    end
end