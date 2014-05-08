#!/usr/bin/env bash

SCRIPT_DIRECTORY=$(dirname "$0")
PROJECT_DIRECTORY=$(dirname "$SCRIPT_DIRECTORY")

FILE_TO_MODIFY="$PROJECT_DIRECTORY/src/mousetrap/controller.py"

setUp() {
    echo "print('Hi')" >> "${FILE_TO_MODIFY}"
}

tearDown() {
    git checkout -- "${FILE_TO_MODIFY}"
}

testPylint() {
    ${SCRIPT_DIRECTORY}/pylint.sh
    assertEquals 'Exit w/o error expected.' 0 $?
}

. shunit2
