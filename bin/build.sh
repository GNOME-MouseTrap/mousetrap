#!/bin/bash
test -z "$PROJECT_DIRECTORY" && . "$(dirname "$0")"/lib/environment_up.sh
cd "$PROJECT_DIRECTORY"
bin/autogen.sh $@ && make
cd -
