#!/bin/bash
test -z "$PROJECT_DIRECTORY" && . "$(dirname "$0")"/lib/environment_up.sh
cd "$PROJECT_DIRECTORY"

last_mod="$(find . \( -path './.git/*' -o -name "*.swp" -prune \) -o -type f -exec stat -f '%m %N' {} \; | sort -n | tail -1)"
read -ra ADDR <<< "$last_mod"
last_mod_file="${ADDR[1]}"

if [ "$last_mod_file" -nt .last_built ] ; then
    "$PROJECT_DIRECTORY/bin/build.sh"
fi

sudo make install
touch .last_install
cd -
