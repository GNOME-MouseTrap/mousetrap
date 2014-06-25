from setuptools import setup, find_packages
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

setup(
    name="mousetrap",
    version=__version__,
    url="https://wiki.gnome.org/Projects/MouseTrap",
    license="GPL",
    include_package_data=True,
    install_requires=requirements,
    packages=find_packages("src"),
    package_dir={
        "": "src",
    },
    entry_points={
        "console_scripts": [
            "mousetrap = mousetrap.main:main",
        ],
    },
)
