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


"""Forehead IDM"""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import mousetrap.ocvfw.debug as debug
import mousetrap.ocvfw.commons as commons
from mousetrap.ocvfw.dev.camera import Capture, Point, Graphic

a_name = "Forehead"
a_description = "Forehead point tracker based on LK Algorithm"
a_settings = { 'speed' : {"value":2}}

class Module(object):
    """
    This is the IDM's Main class, called by mousetrap.py in the load process.
    """

    def __init__(self, controller, stgs = {}):
        """
        IDM's init function.
        
        Arguments:
        - self: The main object pointer.
        - controller: mousetrap main class pointer. This is passed by MouseTrap's controller (mousetrap.py) when loaded.
        - stgs: Possible settings loaded from the user's settings file. If there aren't settings the IDM will use the a_settings dict.
        """

        debug.debug("mousetrap.ocvfw.idm", "Starting %s idm" % a_name)
        
        self.ctr          = controller
        self.cap          = None
        self.stgs         = stgs

        ##############################
        #  MOTION RELATED VARIABLES  #
        ##############################

        #self.step         = self.settings.getint( "mouse", "stepSpeed" )
        self.forehead     = None
        self.foreheadLast = None
        self.foreheadOrig = None
        self.foreheadDiff = None
        self.stopMove     = None
        self.startMove    = None

        ##############################
        #       ACTION POINTS        #
        ##############################
        self.mpPointer       = None

        ##############################
        #  CLICK RELATED VARIABLES   #
        ##############################

        self.isMoving       = False

        self.prepare_config()
        debug.info("mousetrap.ocvfw.idm", "Forhead Algorithm loaded")

    def prepare_config(self):
        """
        Prepares the IDM using the settings
        
        Arguments:
        - self: The main object pointer
        """
        global a_settings

        for key in self.stgs:
            pass

    def set_capture(self, cam):
        """
        Initialize the capture and sets the main settings.
        
        Arguments:
        - self: The main object pointer
        - cam: The camera device index. For Example: 0 = /dev/video0, 1 = /dev/video1
        """
        
        debug.debug("mousetrap.ocvfw.idm", "Setting Capture")
        self.cap = Capture(async=True, idx=cam, backend="OcvfwPython")
        self.cap.change(color="rgb")
        self.cap.set_camera("lk_swap", True)
	
    def calc_motion(self):
        if not hasattr(self.cap, "forehead"):
            self.get_forehead()

    def get_capture(self):
        """
        Sets the forehead point if needed and returns the formated image.

        Arguments:
        - self: The main object pointer

        returns self.cap.image()
        """

        if not hasattr(self.cap, "forehead"):
            self.get_forehead()

	#self.get_forehead()

        #return self.cap.resize(200, 160, True)
        return self.cap
	
    def get_pointer(self):
        """
        Returns the new MousePosition

        Arguments:
        - self: The main object pointer
        """

        if hasattr(self.cap, "forehead"):
	    #debug.debug("Forehead Point", self.cap.forehead)
            return self.cap.forehead

    def get_forehead(self):
        eyes = False
        #self.cap.message("Getting Forehead!!!")
        face     = self.cap.get_area(commons.haar_cds['Face'])

        if face:
	    debug.debug("face", face)

            areas    = [ (pt[1][0] - pt[0][0])*(pt[1][1] - pt[0][1]) for pt in face ] #replaced x with [0] and y with [1]
            startF   = face[areas.index(max(areas))][0]
	    #startF = face[0][0]
	    endF     = face[areas.index(max(areas))][1]
	    #endF = face[0][1]

            # Shows the face rectangle
            self.cap.add( Graphic("rect", "Face", ( startF[0], startF[1] ), (endF[0], endF[1]), parent=self.cap) )

            eyes = self.cap.get_area( 
                commons.haar_cds['Eyes'],
		{"start" : startF[0], "end" : startF[1], "width" : endF[0] - startF[0],"height" : endF[1] - startF[1]},
                (startF[0], startF[1]) ) # replaced x and y
	    debug.debug("eyes - get_area", eyes)

        if eyes:
            areas = [ (pt[1][0] - pt[0][0])*(pt[1][1] - pt[0][1]) for pt in eyes ] #replaced x with [0] and y with [1]

            point1, point2   = eyes[areas.index(max(areas))][0], eyes[areas.index(max(areas))][1]
	    point1, point2 = eyes[0][0], eyes[0][1]
	    debug.debug("eyes", point1)

            # Shows the eyes rectangle
            #self.cap.add(Graphic("rect", "Eyes", ( point1[0], point1[1] ), (point2[0], point2[1]), parent=self.cap))

            X, Y = ( (point1[0] + point2[0]) / 2 ), ( point1[1] + ( (point1[1] + point2[1]) / 2 ) ) / 2 #replaced x and y
	    self.cap.forehead = (X,Y)

	    self.cap.forehead = (((startF[0] + endF[0])/2),((startF[1] + endF[1])/2))
            self.cap.add( Point("point", "forehead-point", self.cap.forehead, parent=self.cap, follow=True) )
	    debug.debug("forehead point", self.cap.forehead)
            return True

        self.foreheadOrig = None

        return False

