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

"""The Drag Mode script."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import gtk
import time
import mouseTrap.events as events
import mouseTrap.environment as env
import mouseTrap.mouseTrap as mouseTrap

from mouseTrap.mainGui import MapperArea
from mouseTrap.mTi18n import _
from opencv import cv

# The name given for the config file
setName = "drag"

## Internal Modes
modes = { "drag|none"    :  _("Mouse Drag/Drop Mode") }

class Profile:

    def __init__( self, gui ):
        """
        The DragProfile Class Constructor.
        
        Initialize the DragProfile class and sets the needed attributes.
        
        Arguments:
        - self: The main object pointer.
        - mouseTrap: The mouseTrap object pointer.
        - cAm: The camera object pointer.
        """

        self.gui      = gui
        self.mTp      = mouseTrap
        self.settings = mouseTrap.settings
        
        self.active   = True

        self._loadSettings()

        self.horArea = MapperArea()
        self.horArea.area( 0, 60, 100, 80, False )

        self.verArea = MapperArea()
        self.verArea.area( 100, 0, 120, 160, False )

        self._registerMapperEvents()

    def _registerMapperEvents( self ):
        """
        Register the mapper events needed.
        
        Arguments:
        - self: The main object pointer.
        """

        self.horArea.connect( "point-move", self._moveDragDropMode, env.ACTIVE, "hor", out = False )
        self.verArea.connect( "point-move", self._moveDragDropMode, env.ACTIVE, "ver", out = False )
        self.gui.mapper.registerTrigger( 100, 80, 4, self._startStopMove )
        #self.gui.mapper.drawPoint( 30, 100, 3, "orange")
        self.gui.mapper.registerArea( self.horArea )
        self.gui.mapper.registerArea( self.verArea )

        #self.area.connect( "point-move", self._clickDialog, env.CLKDLG, out = True )                                                                 
            
        ## events.registerMapperEvent( "activeDrag", [98, 80], [ 100, 82], 
##                                     True, ["moveMode:drag", "clickDlgVisible:False"], 
##                                     self._startStopMove, 2)

    def _loadSettings( self ):
        """
        This load the settings of the D&D mode.
        
        Arguments:
        - self: The main object pointer.
        """
        try:
            self.reqMovement = self.settings.getint( "access", "reqMovement" )
        except:
            self.settings.add_section(  "access" )
            self.settings.set( "access", "reqMovement", "10" )
            self.reqMovement = self.settings.getint( "access", "reqMovement" )

        self.step = self.settings.getint( "mouse", "stepSpeed" )
        
    def _startStopMove( self, *args, **kwds ):
        """
        Allow Users to Enable or Disable the mode.

        Arguments:
        - self: The main object pointer
        - args: The event arguments
        """
        self.active = not self.active

    def _moveDragDropMode( self, sense, *args, **kwds ):
        """
        Perform the mouse pointer movements based on the 'Drag Drop Mode'

        Arguments:
        - self: The main object pointer.
        - sense: The direction of the movement. 
        """
        
        if not self.active:
            return
        
        foreheadDiff = mouseTrap.getModVar( "cam", "foreheadDiff" )

        if not foreheadDiff:
            return
        
        newX, newY = mouseTrap.mice( "position" )

        if "hor" in sense:
            newX += foreheadDiff.x * self.step
        else:
            newY -= foreheadDiff.y * self.step

        mouseTrap.mice( "move", newX, newY )

    def prefTab( self, prefGui ):
        """
        This is the preferences tab function for the Drag Mode Profile.

        Arguments:
        - self: The main object pointer.
        """
        return True

    def _drawDragMapper( self, context ):
        """
        Draws the mapper acording to the 'Drag Drop Mode'

        Arguments:
        - self: The main object pointer.
        - context: The Drawing area context to paint.
        """
        
        for y in [ 60, 80 ]:
            self.gui.mapper.drawLine(context, 0, y, 100, y,  (255, 255, 255))
        for x in [ 100, 120 ]:
            self.gui.mapper.drawLine(context, x, 0, x,  160,  (255, 255, 255))
            
        self.gui.mapper.drawPoint( context, 100, 80, 3, "orange")
        
        self.gui.mapper.drawPoint( context, 30, 100, 3, "orange")

        context.move_to( 30, 30 )
        if self.active:
            context.show_text( "Move: On" )
        else:
            context.show_text( "Move: Off" )


        return True
    
    
