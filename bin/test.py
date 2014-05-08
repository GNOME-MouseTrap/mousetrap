#!/usr/bin/env python3
from unittest import TestLoader
from unittest.runner import TextTestRunner
from pathlib import Path


def main():
    tests = load_tests()
    run_tests(tests)


def load_tests():
    directory = get_package_root_directory()
    tests = TestLoader().discover(directory)
    return tests


def get_package_root_directory():
    this_file = Path(__file__).absolute()
    package_root = this_file.parent.parent/'src/mousetrap'
    return str(package_root)


def run_tests(tests):
    TextTestRunner().run(tests)


if __name__ == '__main__':
    main()
