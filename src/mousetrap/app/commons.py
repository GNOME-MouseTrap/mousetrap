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

""" Common MouseTrap Functions. """

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli."
__license__   = "GPLv2"

import os
import re

def get_py_list(dirlist):
    """
    Checks for .py files on directories in dirlist 
    and removes the extensions. 
        
    Arguments:
    - dirlist: The directories list.
    """

    if not type(dirlist) is list:
        dirlist = [dirlist]
        
    reg = re.compile(r'([A-Za-z0-9]+)\.py$', re.DOTALL)

    group = []
    for dir in dirlist:
        if not os.path.isdir(dir):
            continue
        group.append([ mod[0] for mod in [ reg.findall(f) for f in os.listdir("%s/" % dir) if "handler" not in f] if mod ])

    return [] + [x for l in group for x in l]

