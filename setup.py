from setuptools import setup, find_packages
from distutils.command.build import build
from setuptools.command.egg_info import egg_info
import glob
import os
import sys


SRC_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), "src"))
ABS_SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"))

sys.path.append(SRC_PATH)

from mousetrap import __version__

PYTHON_VERSION = sys.version_info

LOCALE_PATH = "src/mousetrap/locale"

all_requirements = [
    "pygobject",
    "pyyaml",
]

python2_requirements = all_requirements + [
    "python-xlib",
]

python3_requirements = all_requirements + [
    "python3-xlib",
]

if PYTHON_VERSION[0] > 2:
    requirements = python3_requirements
else:
    requirements = python2_requirements


class EggInfoCommand(egg_info):

    def run(self):
        try:
            import gi.repository
        except ImportError:
            sys.stderr.write(
"""
PyGObject does not appear to be installed.  This cannot be installed
automatically and must be installed to the system using your package manager.

On apt-based systems:

    sudo apt-get install python-gobject

On yum-based systems:

    sudo yum install python-gobject

The installation not work as expected without this dependency.
""")

        try:
            import Xlib
        except ImportError:
            # Python3-xlib can be installed automatically
            if PYTHON_VERSION[0] < 3:
                sys.stderr.write(
    """
    Python Xlib does not appear to be installed.  This cannot be installed
    automatically and must be installed to the system using your package manager.

    On apt-based systems:

        sudo apt-get install python-xlib

    On yum-based systems:

        sudo yum install python-xlib

    The installation not work as expected without this dependency.
    """)

        try:
            import cv2
        except ImportError:
            sys.stderr.write(
"""
OpenCV does not appear to be installed.  This cannot be installed
automatically and must be installed to the system using your package manager.

On apt-based systems:

    sudo apt-get install python-opencv

On yum-based systems:

    sudo yum install python-opencv

The installation not work as expected without this dependency.
""")

        if "build" in self.distribution.command_obj:
            build_command = self.distribution.command_obj["build"]

            self.egg_base = build_command.build_base

            self.egg_info = os.path.join(self.egg_base, os.path.basename(self.egg_info))

        egg_info.run(self)


class BuildCommand(build):

    def run(self):
        from subprocess import Popen

        sys.stdout.write("Compiling locale files...\n")

        program = "msgfmt"

        LOCALE_PATH = "%s/mousetrap/locale" % SRC_PATH
        DEST_PATH = "%s/mousetrap/locale" % self.build_lib

        root, directories, files = os.walk(LOCALE_PATH).next()

        language_codes = directories

        for language_code in language_codes:
            message_file = os.path.join(LOCALE_PATH, language_code, "LC_MESSAGES", "mousetrap.po")
            compiled_file = os.path.join(DEST_PATH, language_code, "LC_MESSAGES", "mousetrap.mo")

            if not os.path.exists(os.path.dirname(compiled_file)):
                sys.stdout.write("Creating %s\n" % os.path.dirname(compiled_file))
                os.makedirs(os.path.dirname(compiled_file))

            arguments = [message_file, "--output-file", compiled_file]

            sys.stdout.write("Compiling %s locale" % language_code)

            command = [program] + arguments

            process = Popen(command)

            output, errors = process.communicate()
            status_code = process.returncode

            if status_code == 0:
                sys.stdout.write(" [OK]\n")
            else:
                sys.stdout.write(" [FAIL]\n")

        build.run(self)


setup(
    name="mousetrap",
    version=__version__,
    url="https://wiki.gnome.org/Projects/MouseTrap",
    license="GPL",
    include_package_data=True,
    install_requires=requirements,
    packages=find_packages(SRC_PATH),
    cmdclass={
        "build": BuildCommand,
        "egg_info": EggInfoCommand,
    },
    package_dir={
        "": SRC_PATH,
    },
    entry_points={
        "console_scripts": [
            "mousetrap = mousetrap.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
)
