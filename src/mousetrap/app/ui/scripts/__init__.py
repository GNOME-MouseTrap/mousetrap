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

import re
import os

def get_scripts_list():
    """
    Checks the addons folder and gets the 
    list of present addons.

    Arguments:
    - self: The main object pointer.
    """
    
    reg = re.compile(r'([A-Za-z0-9]+)\.py$', re.DOTALL)
    dirname = os.path.dirname(__file__)
    return [ mod[0] for mod in [ reg.findall(f) for f in os.listdir("%s/" % dirname) if "__init__" not in f] if mod ]


def get_script_class(script_name):
    script = __import__(script_name, globals(), locals())
    return getattr(script, "ScriptClass")