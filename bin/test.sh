#!/bin/bash
test -z "$PROJECT_DIRECTORY" && . "$(dirname "$0")"/lib/environment_up.sh
cd "$PROJECT_DIRECTORY"

find . -name "test_*.sh" -exec "{}" \;
bin/test.py

cd -
