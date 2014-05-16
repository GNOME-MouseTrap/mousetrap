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

test_SCRIPT_DIRECTORY_correct() {
    assertEquals \
        "$(absolute_directory "$(dirname "$0")")" \
        "$SCRIPT_DIRECTORY"
}

test_PROJECT_DIRECTORY_correct() {
    assertEquals \
        "$(absolute_directory "$(dirname "$0")/../..")" \
        "$PROJECT_DIRECTORY"
}

test_last_modified_file() {
	file="test_last_modified_file.tmp"
	touch "$file"
	assertEquals "./$file" "$(last_modified_file .)"
	rm "$file"
}

. /usr/share/shunit2/shunit2
