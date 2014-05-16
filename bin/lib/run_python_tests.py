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
        get_source_directory(),
        get_project_directory()
    ]
    append_to_path(paths)


def append_to_path(paths):
    for path in paths:
        sys.path.append(path)


def get_source_directory():
    return get_project_directory() + '/src'


def get_project_directory():
    return dirname(dirname(dirname(abspath(__file__))))


def get_site_package_directory():
    # FIXME: this path could be different on different platforms.
    # Use autotools to determine its location by changing this file
    # into a .in file, and replace the string below with an automake(?)
    # variable.
    return '/usr/local/lib64/python2.7/site-packages'


def load_tests():
    directory = get_source_directory()
    tests = TestLoader().discover(directory)
    return tests


def run_tests(tests):
    TextTestRunner().run(tests)


if __name__ == '__main__':
    main()
