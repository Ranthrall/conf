#!/bin/bash
# Lara Maia © 2012 ~ 2013 <lara@craft.net.br>
# Contributor: BlackICE <manfredi@gmail.com>
# Versão: 3.0

echo -e "\nAguarde enquanto seu sistema é escaneado...\n"

# Catalog files
repo_file=("repo_packages_dep.cat" "repo_packages_exp.cat")
aur_file=("aur_packages_dep.cat" "aur_packages_exp.cat")

function ,() { echo -ne ".";}

function checkpackages() { # (repository, package type
	echo -ne "\e[1;32m==>\e[0m Gravando catálogo do repositório $1"
	case "$1" in
		aur)	 ,;pacman -Qqmd >> ${aur_file[0]};,
				 ,;pacman -Qqme >> ${aur_file[1]};,
				 ;;
		oficial) ,;pacman -Qqnd >> ${repo_file[0]};,
				 ,;pacman -Qqne >> ${repo_file[1]};,
				 ;;
	esac
	
	if [ "$1" == "aur" ]; then
		packages_count=($(cat ${aur_file[0]} | wc -l) $(cat ${aur_file[1]} | wc -l))
	else
		packages_count=($(cat ${repo_file[0]} | wc -l) $(cat ${repo_file[1]} | wc -l))
	fi
	
	echo -ne "\n - \e[4;37mPacotes do repositório $1\e[0m: "
	echo -ne "\e[1;33m${packages_count[0]}\e[0m instalados explicitamente, "
	echo -e  "\e[1;33m${packages_count[1]}\e[0m dependências\n"
}

# Clean files before write
rm -f ${aur_file[@]} ${repo_file[@]}

checkpackages aur
checkpackages oficial

echo -e "\e[1;32m==>\e[0m Operação concluída\n"
