#!/bin/bash
test -z "$PROJECT_DIRECTORY" && . "$(dirname "$0")"/lib/environment_up.sh
cd "$PROJECT_DIRECTORY"

if [ ! -f "$PROJECT_DIRECTORY/.last_built" -o \
     "$(last_modified_file)" -nt "$PROJECT_DIRECTORY/.last_built" ]
then
    "$PROJECT_DIRECTORY/bin/build.sh"
fi

sudo make install
touch .last_install
cd -
