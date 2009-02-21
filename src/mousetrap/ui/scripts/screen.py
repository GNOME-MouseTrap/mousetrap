# -*- coding: utf-8 -*-

# mouseTrap
#
# Copyright 2008 Flavio Percoco Premoli
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

"""The Screen Mode script."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import gtk
import time
from ui.main import CoordsGui
from ui.widgets import Mapper

# The name given for the config file
setName = "screen"

## Internal Modes
modes = { "screen|abs"  :  "Mouse Absolute Movements",
          "screen|rel"  :  "Mouse Relative Movements"}

class ScriptClass(Mapper):

    def __init__(self):
        #CoordsGui.__init__(self)
        Mapper.__init__(self, 100, 50)

    def prefferences(self):
        """
        This function contains the screen's script prefferences dialog tab.

        Arguments:
        - self: the main object pointer.
        """
