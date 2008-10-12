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

from mouseTrap.mainGui import MapperArea
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
        self.step        = self.settings.get( "mouse", "stepSpeed" )
        self.reqMovement = None

        self.stopMove     = None
        self.startMove    = None
        self.isMoving     = False
 
        self._loadSettings()
        
        self.pref = { 'reqMovement' : 'spinButton' }
       
        
        self.clickCorner     = cv.cvPoint( 100 - self.reqMovement, 80 - self.reqMovement)
        self.scUpCorner      = cv.cvPoint( 100 + self.reqMovement, 80 - self.reqMovement)
        self.scDownCorner    = cv.cvPoint( 100 + self.reqMovement, 80 + self.reqMovement)
        self.defClickCorner  = cv.cvPoint( 100 - self.reqMovement, 80 + self.reqMovement)


        self.area = MapperArea()
        self.area.area( 100 - self.reqMovement, 80 - self.reqMovement, 100 + self.reqMovement, 80 + self.reqMovement, True )
            
        self._registerMapperEvents()

    def _loadSettings( self ):
        """
        This load the settings of the hold mode.
        
        Arguments:
        - self: The main object pointer.
        """
        
        try:
            self.reqMovement = self.settings.getint( "access", "reqMovement" )
        except:
            self.settings.add_section(  "access" )
            self.settings.set( "access", "reqMovement", "10" )
            self.reqMovement = self.settings.getint( "access", "reqMovement" )
            

    def _registerMapperEvents( self ):
        """
        Register the mapper events needed.
        
        Arguments:
        - self: The main object pointer.
        """

        
        self.area.connect( "point-move", self._moveHoldMode, env.ACTIVE, out = True )
        self.area.connect( "top-left-corner", self.gui.clickDlgHandler, env.ACTIVE )
        self.area.connect( "top-right-corner", mouseTrap.mice, env.ACTIVE, "click", button = "b4c" )
        self.area.connect( "bottom-left-corner", mouseTrap.mice, env.ACTIVE, "click", button = "b5c" )
        self.area.connect( "bottom-right-corner", mouseTrap.mice, env.ACTIVE, "click", button = self.settings.get( "mouse", "defClick" ) )
        
	self.gui.mapper.axis = True
        self.gui.mapper.registerArea( self.area  )
        
        ## Click's dialog event.

        self.area.connect( "point-move", self._clickDialog, env.CLKDLG, out = True )
    
    def _moveHoldMode( self, *args, **kwds ):
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
                        if abs(v) >= self.settings.getint( "access", "reqMovement" ) ] )

        for i in var:
            if i > 0: newPoss[i] += var[i]; continue
            newPoss[i] -= var[i]
            
        newX, newY = newPoss
        
                  
        if self.settings.get( "cam", "mouseMode").endswith("|acc") and self.startMove > self.stopMove:
            self.step += ( abs( time.time() - self.startMove) * 3 )
            
        if newPoss != poss:
            if self.stopMove > self.startMove: 
                self.startMove = time.time()
            self.isMoving = True
            mouseTrap.mice( "move", newX, newY )
        else:
            self.isMoving = False
            self.stopMove = time.time()
            self.step     = self.settings.getint( "mouse", "stepSpeed" )

    def _clickDialog( self, *args, **kwds ):
        """
        Click's dialog's point-move event callback

        Arguments:
        - self: The main object pointer.
        """

        dialog   = mouseTrap.getModVar( "gui", "clickDialog" )  
        mPointer = mouseTrap.getModVar( "cam", "mpPointer" ) 

        if mPointer.x in xrange( 0, self.area.xInit ):
            dialog.prevBtn()
        elif mPointer.x in xrange( self.area.xEnd, 200):
            dialogs.nextBtn()
        elif mPointer.y in xrange( 0, self.area.yInit ):
            dialog.pressButton()
        elif mPointer.y in xrange( self.area.yEnd, 160):
            dialog.hidePanel()
            
    def prefTab( self, prefGui ):
        """
        This is the preferences tab function for Hold Mode Profile.

        Arguments:
        - self: The main object pointer.
        """
        
        Frame = gtk.Frame()

        holdBox = gtk.VBox( spacing = 6 )

        reqMov = prefGui.addSpin( _("Required Movement: "), "reqMovement", self.settings.getint( "access", "reqMovement" ) )
        reqMov.get_children()[1].connect("value_changed", self._spinChanged )
        holdBox.pack_start( reqMov, False, False )

        holdBox.show_all()
        
        Frame.add( holdBox )
        Frame.show()
        
        prefGui.NoteBook.insert_page(Frame, gtk.Label( _("Hold Mode") ) )
                    

    def _spinChanged( self, widget ):
        """
        This is the callback function for the spin change event.
        
        Arguments:
        - self: The main object pointer.
        - prefgui: the preferences gui pointer.
        """
        
        self.settings.set( "access", "reqMovement", widget.get_value_as_int() )
