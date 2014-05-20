# -*- coding: utf-8 -*-

# MouseTrap
#
# Copyright 2009 Flavio Percoco Premoli
#
# This file is part of mouseTrap.
#
# MouseTrap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v2 as published
# by the Free Software Foundation.
#
# mouseTrap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mouseTrap.  If not, see <http://www.gnu.org/licenses/>.

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"


def get_scripts_list():
    """
    Generate a list of preset scripts that can be used with MouseTrap.

    This will find any scripts in the current directory that only contain a mix
    of letters (of any case) or numbers that are python files.
    """

    import re
    import os

    valid_script = re.compile(r'([A-Za-z0-9]+)\.py$', re.DOTALL)
    dirname = os.path.dirname(__file__)

    # Get all files in the current directory
    current_directory = os.listdir("%s/" % dirname)

    # Filter all of the files in the current directory to see if the match the
    # format of script files
    scripts = [valid_script.search(file_name) for file_name in current_directory if "_init__" not in file_name]

    # Get the name of the current module, this will be used for reconstructing
    # the full import path to scripts that are found
    current_module = __name__

    return ["%s.%s" % (current_module, name.group(1)) for name in scripts if name]


def get_script_class(script_name):
    """
    Get the class for script based on the name when given as a dotted path.

    For backwards compatibility, this will be able to import scripts when given
    only the name of the script, and not the full dotted path.
    """

    script_path = script_name.split(".")

    # Determine if the full dotted path or just the name was given
    if len(script_path) > 1:
        # If the full dotted path was given, import the script from it's
        # base module
        script = __import__(".".join(script_path), globals(), locals(),
                            script_path[-2])
    else:
        # If only the name of script was given, import it as though it is
        # located relative to the current directory
        script = __import__(script_name, globals(), locals())

    return getattr(script, "ScriptClass")
