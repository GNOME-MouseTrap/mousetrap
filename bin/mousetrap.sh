#!/bin/bash
test -z "$PROJECT_DIRECTORY" && . "$(dirname "$0")"/lib/environment_up.sh
cd "$PROJECT_DIRECTORY"
"$PROJECT_DIRECTORY/src/mousetrap/mousetrap"
cd -
