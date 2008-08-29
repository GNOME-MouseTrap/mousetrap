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
import mouseTrap.events as events
import mouseTrap.environment as env
import mouseTrap.mouseTrap as mouseTrap

from mouseTrap.mTi18n import _
from opencv import cv

# The name given for the config file
setName = "hold"

## Internal Modes
modes = { "hold|const"   :  "Holding With Constant Speed", 
          "hold|acc"     :  "Holding With Automatic Acceleration" }


class Profile:
    """
    The Hold Mode profile
    """

    def __init__( self, gui ):
        """
        The HoldProfile Class Constructor.
        
        Initialize the HoldProfile class and sets the needed attributes.
        
        Arguments:
        - self: The main object pointer.
        - mouseTrap: The mouseTrap object pointer.
        - cAm: The camera object pointer.
        """

        self.gui         = gui
        self.mTp         = mouseTrap
        self.settings    = mouseTrap.settings
        self.step        = self.settings.stepSpeed
        self.reqMovement = None

        self.stopMove     = None
        self.startMove    = None
        self.isMoving     = False
 
        self._loadSettings()
        
        self.pref = { 'reqMovement' : 'spinButton' }
       
        
        self.clickCorner     = cv.cvPoint( 100 - self.settings.reqMovement, 80 - self.settings.reqMovement)
        self.scUpCorner      = cv.cvPoint( 100 + self.settings.reqMovement, 80 - self.settings.reqMovement)
        self.scDownCorner    = cv.cvPoint( 100 + self.settings.reqMovement, 80 + self.settings.reqMovement)
        self.defClickCorner  = cv.cvPoint( 100 - self.settings.reqMovement, 80 + self.settings.reqMovement)
        self._registerMapperEvents()

    def _loadSettings( self ):
        """
        This load the settings of the hold mode.
        
        Arguments:
        - self: The main object pointer.
        """
        
        try:
            getattr( self.settings, "reqMovement")
        except:
            self.settings.reqMovement = 10
            

    def _registerMapperEvents( self ):
        """
        Register the mapper events needed.
        
        Arguments:
        - self: The main object pointer.
        """

        events.registerMapperEvent( "holdMove", 
                    [ 100 - self.settings.reqMovement, 80 - self.settings.reqMovement ], 
                    [ 100 + self.settings.reqMovement, 80 + self.settings.reqMovement ], 
                    False, ["moveMode:hold", "clickDlgVisible:False"], self._moveHoldMode, 0)

        events.registerMapperEvent( "clickPanel", 
                    [self.clickCorner.x, self.clickCorner.y],
                    [self.clickCorner.x + 2, self.clickCorner.y + 2], 
                    True, ["moveMode:hold", "clickDlgVisible:False"], 
                    self.gui.clickDlgHandler , 0.5)
                                        
        events.registerMapperEvent( "scrollUp", 
                    [self.scUpCorner.x - 2, self.scUpCorner.y],
                    [self.scUpCorner.x, self.scUpCorner.y + 2], 
                    True, ["moveMode:hold", "clickDlgVisible:False"], 
                    mouseTrap.mice, 0.5, "click", button = "b4c" )
                
        events.registerMapperEvent( "scrollDown", 
                    [self.scDownCorner.x - 2, self.scDownCorner.y - 2],
                    [self.scDownCorner.x, self.scDownCorner.y], 
                    True, ["moveMode:hold", "clickDlgVisible:False"], 
                    mouseTrap.mice, 0.5, "click", button =  "b5c" )
            
        events.registerMapperEvent( "defClick", 
                    [self.defClickCorner.x, self.scDownCorner.y - 2],
                    [self.defClickCorner.x + 2, self.scDownCorner.y], 
                    True, ["moveMode:hold", "clickDlgVisible:False"],  
                    mouseTrap.mice, 0.5, "click", button = self.settings.defClick )
             
        #########################
        #  CLICK DIALOG EVENTS  #
        #########################
            
        events.registerMapperEvent( "clickDlgPrev", [0, 0],
                        [ 100 - self.settings.reqMovement, 160], 
                        True, ["moveMode:hold", "clickDlgVisible:True"], 
                        self.gui.clickDialog.prevBtn, 2)
                        
        events.registerMapperEvent( "clickDlgNext", 
                        [100 + self.settings.reqMovement, 0], [ 200, 160], 
                        True, ["moveMode:hold", "clickDlgVisible:True"], 
                        self.gui.clickDialog.nextBtn, 2)
                        
        events.registerMapperEvent( "clickDlgAccept", 
                        [98, 80 - self.settings.reqMovement - 2 ],
                        [ 102, 80 - self.settings.reqMovement + 2], 
                        True, ["moveMode:hold", "clickDlgVisible:True"], 
                        self.gui.clickDialog.pressButton, 2)
                        
        events.registerMapperEvent( "clickDlgCancel", 
                        [98, 80 + self.settings.reqMovement - 2], 
                        [ 102, 80 + self.settings.reqMovement - 2 ], 
                        True, ["moveMode:hold", "clickDlgVisible:True"], 
                        self.gui.clickDialog.hidePanel, 2)

    def _moveHoldMode( self, *args ):
        """
        Perform the movements using the 'HOLD' mode.
        
        The 'HOLD' mode methods are:
        switch-hold-const: Will move the mouse with a constant speed.
        switch-hold-acc: Will move the mouse with a constant acceleration. 
                                   Each second the speed will be increased.
        
        Arguments:
        - self: The main object pointer.
        """
        
        forehead     = mouseTrap.getModVar("cam", "forehead")
        foreheadOrig = mouseTrap.getModVar("cam", "foreheadOrig")
 
        if not forehead or not foreheadOrig:
            return False

        poss = mouseTrap.mice( "position" )
        
        newPoss = poss[:]
        
        var = dict( [ ( i, self.step*(v/abs(v))) 
                        for i,v in enumerate( [ forehead.x - foreheadOrig.x,
                                                forehead.y - foreheadOrig.y] )  
                        if abs(v) >= self.settings.reqMovement ] )

        for i in var:
            if i > 0: newPoss[i] += var[i]; continue
            newPoss[i] -= var[i]
            
        newX, newY = newPoss
        
                  
        if self.settings.mouseMode.endswith("|acc") and self.startMove > self.stopMove:
            self.step += ( abs( time.time() - self.startMove) * 3 )
            
        if newPoss != poss:
            if self.stopMove > self.startMove: 
                self.startMove = time.time()
            self.isMoving = True
            mouseTrap.mice( "move", newX, newY )
        else:
            self.isMoving = False
            self.stopMove = time.time()
            self.step     = self.settings.stepSpeed

    def prefTab( self, prefGui ):
        """
        This is the preferences tab function for Hold Mode Profile.

        Arguments:
        - self: The main object pointer.
        """
        
        Frame = gtk.Frame()

        holdBox = gtk.VBox( spacing = 6 )

        reqMov = prefGui.addSpin( _("Required Movement: "), "reqMovement", self.settings.reqMovement)
        reqMov.get_children()[1].connect("value_changed", self.spinChanged )
        holdBox.pack_start( reqMov, False, False )

        holdBox.show_all()
        
        Frame.add( holdBox )
        Frame.show()
        
        prefGui.NoteBook.insert_page(Frame, gtk.Label( _("Hold Mode") ) )
                    

    def spinChanged( self, widget ):
        """
        This is the callback function for the spin change event.
        
        Arguments:
        - self: The main object pointer.
        - prefgui: the preferences gui pointer.
        """
        
        self.settings.reqMovement = widget.get_value_as_int() 
                                        
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
            self._drawCartesianPlane( context )
            
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
        
        self.gui.mapper.drawLine(context, 100 - reqLim, 80 - reqLim, 100 + reqLim, 80 - reqLim, (255, 255, 255))
        self.gui.mapper.drawLine(context, 100 - reqLim, 80 + reqLim, 100 + reqLim, 80 + reqLim, (255, 255, 255))
        
        self.gui.mapper.drawLine(context, 100 - reqLim, 80 - reqLim, 100 - reqLim, 80 + reqLim, (255, 255, 255))
        self.gui.mapper.drawLine(context, 100 + reqLim, 80 - reqLim, 100 + reqLim, 80 + reqLim, (255, 255, 255))
                
        msgs = { _( "Cancel" ) : { "x" : 80, "y" : 100 + reqLim },
                 _( "Accept" ) : { "x" : 80, "y" : 70 - reqLim },
                  "-->"   : { "x" : 100 + reqLim, "y" : 85},
                 "<--"    : { "x" : 70 - reqLim,  "y" : 85 }
                }
                
        for msg,arr in msgs.iteritems():
            context.move_to ( arr["x"] , arr["y"] )
            context.show_text ( msg )    
            
        # Accept Point
        self.gui.mapper.drawPoint( context, 100, 80 - reqLim, 3, "orange")
        
        # Cancel Point
        self.gui.mapper.drawPoint( context, 100, 80 + reqLim, 3, "orange")

    def _drawCartesianPlane( self, context ):
        """
        Draws the Cartesian Plane
        
        Arguments:
        - self:  The main object pointer.
        - context: The Cairo Context.
        """
        
        reqLim = self.settings.reqMovement


        #Safe area   
            
        # Y Line
        self.gui.mapper.drawLine(context, 100, 0, 100, 160, (255, 255, 255))
        
        # X Line
        self.gui.mapper.drawLine(context, 0, 80, 200, 80, (255, 255, 255))
        
        self.gui.mapper.drawLine(context, 100 - reqLim, 80 - reqLim, 100 + reqLim, 80 - reqLim, (255, 255, 255))
        self.gui.mapper.drawLine(context, 100 - reqLim, 80 + reqLim, 100 + reqLim, 80 + reqLim, (255, 255, 255))
        
        self.gui.mapper.drawLine(context, 100 - reqLim, 80 - reqLim, 100 - reqLim, 80 + reqLim, (255, 255, 255))
        self.gui.mapper.drawLine(context, 100 + reqLim, 80 - reqLim, 100 + reqLim, 80 + reqLim, (255, 255, 255))
        
        # Up/Left ( Click Panel )
        self.gui.mapper.drawPoint( context, 100 - reqLim, 80 - reqLim, 3, "orange")
        
        #Down/Right ( Scroll Button )
        self.gui.mapper.drawPoint( context, 100 + reqLim, 80 + reqLim, 3, self.gui.mapper.triggers['scD'])
            
        #Up/Right ( Scroll Button )
        self.gui.mapper.drawPoint( context, 100 + reqLim, 80 - reqLim, 3, self.gui.mapper.triggers['scU'])
            
        # Down/Left ( Default Click Launcher )
        self.gui.mapper.drawPoint( context, 100 - reqLim, 80 + reqLim, 3, "orange")

        return True 
