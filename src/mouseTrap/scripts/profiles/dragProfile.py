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

import mouseTrap.events as events
import mouseTrap.environment as env
import mouseTrap.mouseTrap as mouseTrap

from mouseTrap.mTi18n import _

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
        
        self.step     = self.settings.stepSpeed
        self.active   = False

        self._loadSettings()
        self._registerMapperEvents()

    def _registerMapperEvents( self ):
        """
        Register the mapper events needed.
        
        Arguments:
        - self: The main object pointer.
        """

        events.registerMapperEvent( "dragHor", [ 0, 60 ], [ 100, 80 ], 
                                    True, ["moveMode:drag", "clickDlgVisible:False"], 
                                    self._moveDragDropMode, 0, "hor")
            
        events.registerMapperEvent( "dragVer", [100, 0], [ 120, 160], 
                                    True, ["moveMode:drag", "clickDlgVisible:False"], 
                                    self._moveDragDropMode, 0, "ver")
            
        events.registerMapperEvent( "activeDrag", [98, 80], [ 100, 82], 
                                    True, ["moveMode:drag", "clickDlgVisible:False"], 
                                    self._startStopMove, 2)

        events.registerMapperEvent( "clickPanel", [28, 98], [32, 102], 
                                    True, ["moveMode:drag", "clickDlgVisible:False"], 
                                    self.gui.clickDlgHandler, 0.5)

        #########################
        #  CLICK DIALOG EVENTS  #
        #########################
            
        events.registerMapperEvent( "clickDlgPrev", [0, 0],
                                    [ 30 - self.settings.reqMovement, 160], 
                                    True, ["moveMode:drag", "clickDlgVisible:True"], 
                                    self.gui.clickDialog.prevBtn, 2)
                                    
        events.registerMapperEvent( "clickDlgNext", [30 + self.settings.reqMovement, 0],
                                    [ 200, 160], True, ["moveMode:drag", "clickDlgVisible:True"], 
                                    self.gui.clickDialog.nextBtn, 2)
        
        events.registerMapperEvent( "clickDlgAccept", [0, 0], 
                                    [ 200, 100 - self.settings.reqMovement], 
                                    True, ["moveMode:drag", "clickDlgVisible:True"], 
                                    self.gui.clickDialog.pressButton, 2)
        
        events.registerMapperEvent( "clickDlgCancel", 
                                    [0, 100 + self.settings.reqMovement],[ 200, 160], 
                                    True, ["moveMode:drag", "clickDlgVisible:True"], 
                                    self.gui.clickDialog.hidePanel, 2)

    def _loadSettings( self ):
        """
        This load the settings of the D&D mode.
        
        Arguments:
        - self: The main object pointer.
        """
        
        try:
            getattr( self.settings, "reqMovement")
        except:
            self.settings.reqMovement = 10
            
    def _startStopMove( self, *args ):
        """
        Allow Users to Enable or Disable the mode.

        Arguments:
        - self: The main object pointer
        - args: The event arguments
        """
        self.active = not self.active

    def _moveDragDropMode( self, sense ):
        """
        Perform the mouse pointer movements based on the 'Drag Drop Mode'

        Arguments:
        - self: The main object pointer.
        - sense: The direction of the movement. 
        """

        if not self.active:
            return
        
        foreheadDiff = mouseTrap.getModVar( "cam", "foreheadDiff" )
        
        newX, newY = mouseTrap.mice( "position" )

        if "hor" in sense:
            newX += foreheadDiff.x * self.step
        else:
            newY -= foreheadDiff.y * self.step

        mouseTrap.mice( "move", newX, newY )

    def drawMapper( self, context ):
        """
        Calls the drawing function needed

        Arguments:
        - self: The main object pointer.
        - context: The Drawing area context to paint.
        """

        if self.gui.clickDialog.props.visible:
            self._clickDlgMapper( context )
        else:
            self._drawDragMapper( context )

    def _clickDlgMapper( self, context ): 
        """
        Draws the mapper acording to the Click Dialog

        Arguments:
        - self: The main object pointer.
        - context: The Drawing area context to paint.
        """

        reqLim = self.settings.reqMovement
        
        context.set_font_size (20)
        context.set_source_rgb( 255, 255, 255)
        
        self.gui.mapper.drawLine(context, 30 - reqLim, 100 - reqLim, 30 + reqLim, 100 - reqLim, (255, 255, 255))
        self.gui.mapper.drawLine(context, 30 - reqLim, 100 + reqLim, 30 + reqLim, 100 + reqLim, (255, 255, 255))
        
        self.gui.mapper.drawLine(context, 30 - reqLim, 100 - reqLim, 30 - reqLim, 100 + reqLim, (255, 255, 255))
        self.gui.mapper.drawLine(context, 30 + reqLim, 100 - reqLim, 30 + reqLim, 100 + reqLim, (255, 255, 255))
                
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
    
    
