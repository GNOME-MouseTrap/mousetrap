#!/bin/bash
test -z "$PROJECT_DIRECTORY" && . "$(dirname "$0")"/environment_up.sh
cd "$PROJECT_DIRECTORY"

find . -name "test_*.sh" -exec "{}" \;

cd -
