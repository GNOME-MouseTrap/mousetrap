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


"""Forehead IDM"""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

from ocvfw.dev.camera import *

class Module(object):

    def __init__(self, controller):
        Camera.init(idx=0)

        self.img          = None
        self.ctr          = controller
        self.cap          = None

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
        self.haar_cds     = { 'Face'  :  "../ocvfw/haars/haarcascade_frontalface_alt.xml",
                              'Eyes'  :  "../ocvfw/haars/frontalEyes35x16.xml",
                              #'Eyes'  :  "../ocvfw/haars/haarcascade_eye_tree_eyeglasses.xml",
                              'Mouth' :  "../ocvfw/haars/Mouth.xml"}

        ##############################
        #       ACTION POINTS        #
        ##############################
        self.mpPointer       = None

        ##############################
        #  CLICK RELATED VARIABLES   #
        ##############################

        self.isMoving       = False

    def set_capture(self):
        self.cap = Capture(async=True)
        self.cap.change(color="rgb")

    def calc_motion(self):
        if not hasattr(self.cap, "forehead"):
            self.get_forehead()

    def get_image(self):
        """
        Sets the forehead point if needed and returns the formated image.

        Arguments:
        - self: The main object pointer

        returns self.cap.image()
        """
        if not hasattr(self.cap, "forehead"):
            self.get_forehead()

        return self.cap.image()

    def get_pointer(self):
        """
        Returns the new MousePosition

        Arguments:
        - self: The main object pointer
        """
        if hasattr(self.cap, "forehead"):
            return self.cap.forehead

    def get_forehead(self):
        eyes = False
        #self.cap.add_message("Getting Forehead!!!")

        face     = self.cap.get_area(self.haar_cds['Face'])

        if face:
            areas    = [ (pt[1].x - pt[0].x)*(pt[1].y - pt[0].y) for pt in face ]
            startF   = face[areas.index(max(areas))][0]
            endF     = face[areas.index(max(areas))][1]

            # Shows the face rectangle
            #self.cap.add( Graphic("rect", "Face", ( startF.x, startF.y ), (endF.x, endF.y), parent=self.cap) )

            eyes = self.cap.get_area( self.haar_cds['Eyes'], {"start" : startF.x,
                                                         "end" : startF.y,
                                                         "width" : endF.x - startF.x,
                                                         "height" : endF.y - startF.y}, (startF.x, startF.y) )

        if eyes:
            areas = [ (pt[1].x - pt[0].x)*(pt[1].y - pt[0].y) for pt in eyes ]

            point1, point2   = eyes[areas.index(max(areas))][0], eyes[areas.index(max(areas))][1]

            # Shows the eyes rectangle
            #self.cap.add(Graphic("rect", "Face", ( point1.x, point1.y ), (point2.x, point2.y), parent=self.cap))

            X, Y = ( (point1.x + point2.x) / 2 ), ( point1.y + ( (point1.y + point2.y) / 2 ) ) / 2
            self.cap.add( Point("point", "forehead", ( X, Y ), parent=self.cap, follow=True) )
            return True

        self.foreheadOrig = None

        return False


