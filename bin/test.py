#!/usr/bin/env python3
from unittest import TestLoader
from unittest.runner import TextTestRunner
import os.path


def main():
    tests = load_tests()
    run_tests(tests)


def load_tests():
    directory = get_package_root_directory()
    tests = TestLoader().discover(directory)
    return tests


def get_package_root_directory():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src/mousetrap'


def run_tests(tests):
    TextTestRunner().run(tests)


if __name__ == '__main__':
    main()
