# -*- coding: utf-8 -*-

# Ocvfw
#
# Copyright 2009 Flavio Percoco Premoli
#
# This file is part of Ocvfw.
#
# Ocvfw is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v2 as published
# by the Free Software Foundation.
#
# Ocvfw is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ocvfw.  If not, see <http://www.gnu.org/licenses/>>.

"""Little  Framework for OpenCV Library."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"


import time
from OcvfwBase import OcvfwBase
from .. import debug
from .. import commons as co

class OcvfwCtypes(OcvfwBase):
    """
    This Class controlls the main camera functions.
    It works as a little framework for Openco.cv.

    This Backend uses ctypes opencv python bindings.
    """
    

    def __init__(self):
        """
        Initialize the module and set its main variables.
        """
        co.cv = __import__("ctypesopencv.cv",
                        globals(),
                        locals(),
                        [''])
        
        co.hg = __import__("ctypesopencv.highgui",
                        globals(),
                        locals(),
                        [''])
 
        OcvfwBase.__init__(self)



