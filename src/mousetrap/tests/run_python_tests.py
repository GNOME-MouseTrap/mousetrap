from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from unittest import TestLoader
from unittest.runner import TextTestRunner
from os.path import dirname, abspath
import sys


from mousetrap.config import Config
CONFIG = Config().load_default()
print(CONFIG['camera'])


import logging
import logging.config
logging.config.dictConfig(CONFIG['logging-test'])
LOGGER = logging.getLogger('mousetrap.tests.run_python_tests')



def main():
    initialize_import_path()
    tests = load_tests()
    run_tests(tests)


def initialize_import_path():
    paths = [
        get_source_directory()
    ]
    print("appending " + str(paths))
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
