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


"""The Screen Mode script."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import mousetrap.app.environment as env
import mousetrap.app.lib.mouse as mouse

# pylint: disable-msg=F0401
# Unable to import 'widgets' (No module named widgets)
# Widgets is in the parent folder
from ..widgets import Mapper

# The name given for the config file
setName = "joystick"

## Internal Modes
modes = { "screen|abs"  :  "Mouse Absolute Movements",
          "screen|rel"  :  "Mouse Relative Movements"}

# We get too many E1101 messages, but We know what we're doing.
# Mapper does have those methods.
# pylint: disable-msg=E1101
class ScriptClass(Mapper):

    def __init__(self):
        Mapper.__init__(self, 200, 160)

        self.point       = None
        self.border_width = 0

        self.connect("expose_event", self.expose_event)

    def update_items(self, point):
        self.point = point
        self.calc_move()
        self.queue_draw()

    def expose_event(self, widget, event):
        self.width, self.height = self.allocation[2], self.allocation[3]
        
#        self.draw_rectangle(0,
#                            0,
#                            self.width,
#                            self.height,
#                            self.style.fg[self.state],
#                            5.0)

        self.center = { "x" : self.width / 2,
                        "y" : self.height / 2 }

        self.safe_area = { "x" : self.center["x"] - 10,
                         "y" : self.center["y"] - 10,
                         "width"  : 20,
                         "height" : 20}

        self.draw_rectangle( self.safe_area["x"], self.safe_area["y"],
                             self.safe_area["width"], self.safe_area["height"],
                             self.style.fg[self.state], 1.0)

        if hasattr(self.point, "abs_diff"):
            self.vpoint = { "x" : self.center["x"] - self.point.abs_diff.x,
                            "y" : self.center["y"] + self.point.abs_diff.y }

            self.draw_point( self.vpoint["x"], self.vpoint["y"], 2)

    def calc_move(self):
        if not hasattr(self, "vpoint"):
            return False
        
        x, y = mouse.position()

        par = ["width", "height"]
        
        if self.vpoint["x"] > (self.safe_area["x"] + 20):
            x = x + abs((self.safe_area["x"] + 20) - self.vpoint["x"]) 
        elif self.vpoint["x"] < self.safe_area["x"]: 
            x = x - abs((self.safe_area["x"]) - self.vpoint["x"])
            
        if self.vpoint["y"] > (self.safe_area["y"] + 20):
            y = y + abs((self.safe_area["y"] + 20) - self.vpoint["y"])
        elif self.vpoint["y"] < self.safe_area["y"]: 
            y = y - abs((self.safe_area["y"]) - self.vpoint["y"])
            
        
        mouse.move( x, y)

    def prefferences(self):
        """
        This function contains the screen's script prefferences dialog tab.

        Arguments:
        - self: the main object pointer.
        """
        pass
