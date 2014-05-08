#!/bin/bash
set -e
absolute_directory(){
    cd "$1" >& /dev/null || return ''
    pwd
    cd - >& /dev/null
}
project_directory(){
    original_directory="$PWD"
    while [ ! -d './src' ] ; do
        cd .. >& /dev/null
    done
    echo "$PWD"
    cd "$original_directory" >& /dev/null
}
SCRIPT_DIRECTORY="$(absolute_directory "$(dirname "$0")")"
PROJECT_DIRECTORY="$(project_directory)"
