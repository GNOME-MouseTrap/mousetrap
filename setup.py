from setuptools import setup, find_packages
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install
import os
import sys


SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "src"))

sys.path.append(SRC_PATH)

from mousetrap import __version__

PYTHON_VERSION = sys.version_info

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

        egg_info.run(self)


class InstallCommand(install):

    def run(self):
        from subprocess import Popen

        sys.stdout.write("Compiling locale files...\n")

        program = "msgfmt"

        LOCALE_PATH = "src/mousetrap/locale"

        root, directories, files = os.walk(LOCALE_PATH).next()

        language_codes = directories

        for language_code in language_codes:
            message_file = os.path.join(LOCALE_PATH, language_code, "LC_MESSAGES", "mousetrap.po")
            compiled_file = os.path.join(LOCALE_PATH, language_code, "LC_MESSAGES", "mousetrap.mo")

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

        install.run(self)


setup(
    name="mousetrap",
    version=__version__,
    url="https://wiki.gnome.org/Projects/MouseTrap",
    license="GPL",
    include_package_data=True,
    install_requires=requirements,
    packages=find_packages("src"),
    cmdclass={
        "egg_info": EggInfoCommand,
        "install": InstallCommand,
    },
    package_dir={
        "": "src",
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
    ]
)
