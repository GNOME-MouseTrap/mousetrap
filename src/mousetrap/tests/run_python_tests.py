#!/usr/bin/env python
from unittest import TestLoader
from unittest.runner import TextTestRunner
from os.path import dirname, abspath
import sys


def main():
    initialize_import_path()
    tests = load_tests()
    run_tests(tests)


def initialize_import_path():
    paths = [
        get_source_directory()
    ]
    print "appending " + str(paths)
    append_to_path(paths)


def append_to_path(paths):
    for path in paths:
        sys.path.append(path)


def get_source_directory():
    return abspath(dirname(__file__) + '/../..')


def load_tests():
    directory = get_source_directory()
    tests = TestLoader().discover(directory)
    return tests


def run_tests(tests):
    TextTestRunner().run(tests)


if __name__ == '__main__':
    main()
