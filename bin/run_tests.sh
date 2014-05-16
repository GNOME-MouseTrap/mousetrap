#!/bin/bash
test -z "$PROJECT_DIRECTORY" && . "$(dirname "$0")"/lib/environment_up.sh
cd "$PROJECT_DIRECTORY"

bin/lib/run_shell_tests.sh
python bin/lib/run_python_tests.py

cd -
