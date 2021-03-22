#! /bin/bash

function _echo() {
		case $1 in
		    "yellow" )
		     		echo -e "\e[3;33m[`date +"%d.%m.%Y %H:%M:%S"`] $2\e[0m"  | tee -a ${log_file}
		    ;;
		    "green" )
		    		echo -e "\e[3;32m[`date +"%d.%m.%Y %H:%M:%S"`] $2\e[0m"  | tee -a ${log_file}
		    ;;
		    "blue" )
		    		echo -e "\e[1;34m[`date +"%d.%m.%Y %H:%M:%S"`] $2\e[0m"  | tee -a ${log_file}
		    ;;
		    "red" )
		    		echo -e "\e[3;31m[`date +"%d.%m.%Y %H:%M:%S"`] $2\e[0m"  | tee -a ${log_file}
		    ;;
		    *)
		    		echo "$2"
		    ;;
		esac
}

if [ ! -z $1 ] ; then
  if [[ ! -z "$2" ]] ; then
    _echo yellow "[INFO] Git add"
    git add .
    _echo yellow "[INFO] Git commit: $2"
    git commit -m "${2}"
    _echo yellow "[INFO] Git checkout: $1"
    git checkout -b ${1}
    _echo yellow "[INFO] Git merge $1 to latest"
    git merge ${1} latest
    _echo green "[INFO] Git push"
    git push origin ${1}
  else
    _echo red "[ERROR] arg2 not set. Commit comment empty."
  fi
else
  _echo red "[ERROR] arg1 not set. Please set branch name."
fi
