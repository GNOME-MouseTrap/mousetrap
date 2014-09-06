from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
'''
Where it all begins.
'''
from argparse import ArgumentParser
import logging
import logging.config
import sys
import yaml
from os.path import dirname, expanduser, exists
from io import open
import os.path

from mousetrap.config import Config


class Main(object):
    DEFAULT_CONFIG_PATH = os.path.join(dirname(__file__), 'mousetrap.yaml')
    USER_CONFIG_PATH = expanduser('~/.mousetrap.yaml')

    def __init__(self):
        try:
            self._args = CommandLineArguments()
            self._handle_dump_annotated()
            self._config = Config().load(self._get_config_paths())
            self._handle_dump_config()
            self._configure_logging()
        except ExitException:
            sys.exit(0)

    def _get_config_paths(self):
        paths = [self.DEFAULT_CONFIG_PATH]
        if exists(self.USER_CONFIG_PATH):
            paths.append(self.USER_CONFIG_PATH)
        if self._args.config is not None:
            paths.append(self._args.config)
        return paths

    def _handle_dump_annotated(self):
        if self._args.dump_annotated:
            self._dump_annotated()
            raise ExitException()

    def _handle_dump_config(self):
        if self._args.dump_config:
            self._dump_config()
            raise ExitException()

    @classmethod
    def _dump_annotated(cls):
        with open(cls.DEFAULT_CONFIG_PATH, 'r') as annotated_file:
            print(annotated_file.read())

    def _dump_config(self):
        print(yaml.dump(dict(self._config), default_flow_style=False))

    def _configure_logging(self):
        logging.config.dictConfig(self._config['logging'])
        logger = logging.getLogger('mousetrap.main')
        logger.debug(yaml.dump(dict(self._config), default_flow_style=False))

    def run(self):
        from mousetrap.core import App
        App(self._config).run()


class CommandLineArguments(object):

    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("--config",
                metavar="FILE",
                help="Loads configuration from FILE.")
        parser.add_argument("--dump-config",
                help="Loads and dumps current configuration to standard out.",
                action="store_true")
        parser.add_argument("--dump-annotated",
                help="Dumps default configuration" + \
                    " (with comments) to standard out.",
                action="store_true")
        parser.parse_args(namespace=self)


class ExitException(Exception):
    pass


def main():
    Main().run()


if __name__ == '__main__':
    main()
