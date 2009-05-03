# -*- coding: utf-8 -*-

# mouseTrap
#
# Copyright 2009 Flavio Percoco Premoli
#
# This file is part of mouseTrap.
#
# mouseTrap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# mouseTrap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mouseTrap.  If not, see <http://www.gnu.org/licenses/>.


"""Python Opencv Handler."""

__id__        = "$Id: mousetrap.py 29 2009-03-31 12:06:44Z flaper $"
__version__   = "$Revision: 29 $"
__date__      = "$Date: 2009-03-31 14:06:44 +0200 (mar 31 de mar de 2009) $"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import os

def get_idm(idm):
    """
    Returns the idm's class instance.

    Arguments:
    - idm: The requested idm.
    """
    return __import__("ocvfw.idm.%s" % idm,
                      globals(),
                      locals(),
                      [''])

def get_idms_list():
    dirname = os.path.dirname(__file__)
    return [ f.replace(".py", "") for f in os.listdir("%s/idm/" % dirname) if "__" not in f and ".py" in f and ".pyc" not in f ]

def get_idm_inf(idm):
    tmp = __import__("ocvfw.idm.%s" % idm,
                      globals(),
                      locals(),
                      [''])
    return { "name" : tmp.a_name, "dsc" : tmp.a_description, "stgs" : tmp.a_settings}

