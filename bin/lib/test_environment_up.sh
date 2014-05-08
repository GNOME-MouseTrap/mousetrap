#!/bin/bash

oneTimeSetUp() {
    . "$(dirname "$0")/environment_up.sh"
}

test_absolute_directory() {
    assertEquals "$(pwd)" "$(absolute_directory .)"
}

test_project_directory() {
    assertEquals \
        "$(absolute_directory "$(dirname "$0")/../..")" \
        "$(project_directory)"
}

test_SCRIPT_DIRECTORY_defined() {
    assertNotNull "$SCRIPT_DIRECTORY"
}

test_SCRIPT_DIRECTORY_correct() {
    assertEquals \
        "$(absolute_directory "$(dirname "$0")")" \
        "$SCRIPT_DIRECTORY"
}

test_PROJECT_DIRECTORY_defined() {
    assertNotNull "$PROJECT_DIRECTORY"
}

test_PROJECT_DIRECTORY_correct() {
    assertEquals \
        "$(absolute_directory "$(dirname "$0")/../..")" \
        "$PROJECT_DIRECTORY"
}

. shunit2
