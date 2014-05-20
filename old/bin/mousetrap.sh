#!/bin/bash
test -z "$PROJECT_DIRECTORY" && . "$(dirname "$0")"/lib/environment_up.sh
"$PROJECT_DIRECTORY/src/mousetrap/inplace_runner.py"
