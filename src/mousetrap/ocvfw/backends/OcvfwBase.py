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

import os
import re
import time
from .. import debug
from .. import commons as co

def exists_backend(bknd):
    reg = re.compile(r'([A-Za-z0-9]+)\.py$', re.DOTALL)
    dirname = os.path.dirname(__file__)

    for f in os.listdir("%s/" % dirname):
        if reg.match(f):
            return True
    return False

def get_backend(bknd):
    return __import__("%s" % bknd, globals(), locals(), [])

class OcvfwBase:
    
    def __init__( self ):
        """
        Initialize the module and set its main variables.
        """

        self.img          = None
        self.mhi          = None
        self.img_lkpoints = { "current" : [],
                              "last"    : [],
                              "points"  : [] }

        self.__lk_swap = False
        self.imageScale   = 1.5

    def set(self, key, value):
        """
        Changes some class settings

        Arguments:
        - self: The main object pointer.
        - key: The key to change.
        - value: The new value.
        """
        if hasattr(self, "%s" % key):
            getattr(self, "%s" % key)(value)
            debug.debug("OcvfwBase", "Changed %s value to %s" % (key, value))
            return True
        
        debug.debug("OcvfwBase", "%s not found" % (key))
        return False

    def lk_swap(self, set=None):
        """
        Enables/Disable the lk points swapping action.

        Arguments:
        - self: The main object pointer.
        - set: The new value. If None returns the current state.
        """
        
        if set is None:
            return self.__lk_swap
        
        self.__lk_swap = set

    def new_image(self, size, num, ch):
        """
        Creates a new image 
        """

        if type(size) == "<type 'tuple'>":
            size = co.cv.cvSize( size[0], size[1])

        return co.cv.cvCreateImage( size, num, ch)

    def set_camera_idx(self, idx):
        """
        Changes the camera device index.

        Arguments:
        - self: The main object pointer.
        - idx: The camera index. For Example: 0 for /dev/video0
        """
        self.idx = idx

    def wait_key(self, num):
        """
        Simple call to the co.hg.cvWaitKey function, which has to be called periodically.

        Arguments:
        - self: The main object pointer.
        - num: An int value.
        """
        return co.hg.cvWaitKey(num)
    
    def start_camera(self, params = None):
        """
        Starts the camera capture using co.hg.

        Arguments:
        - params: A list with the capture properties. NOTE: Not implemented yet.
        """
        self.capture = co.hg.cvCreateCameraCapture( int(self.idx) )
        debug.debug( "ocvfw", "cmStartCamera: Camera Started" )
    
    def query_image(self, bgr=False, flip=False):
        """
        Queries the new frame.

        Arguments:
        - self: The main object pointer.
        - bgr: If True. The image will be converted from RGB to BGR.

        Returns The image even if it was stored in self.img
        """

        frame = co.hg.cvQueryFrame( self.capture )

        if not  self.img:
            self.storage        = co.cv.cvCreateMemStorage(0)
            self.imgSize        = co.cv.cvGetSize (frame)
            self.img            = co.cv.cvCreateImage ( self.imgSize, 8, 3 )
            #self.img.origin     = frame.origin
            self.grey           = co.cv.cvCreateImage ( self.imgSize, 8, 1 )
            self.yCrCb          = co.cv.cvCreateImage ( self.imgSize, 8, 3 )
            self.prevGrey       = co.cv.cvCreateImage ( self.imgSize, 8, 1 )
            self.pyramid        = co.cv.cvCreateImage ( self.imgSize, 8, 1 )
            self.prevPyramid    = co.cv.cvCreateImage ( self.imgSize, 8, 1 )
            self.small_img       = co.cv.cvCreateImage( co.cv.cvSize( co.cv.cvRound ( self.imgSize.width/self.imageScale),
                                    co.cv.cvRound ( self.imgSize.height/self.imageScale) ), 8, 3 )
        self.img = frame
        co.cv.cvCvtColor(self.img, self.grey, co.cv.CV_BGR2GRAY)

        self.wait_key(10)
        return True
    
    def set_lkpoint(self, point):
        """
        Set a point to follow it using the L. Kallman method.

        Arguments:
        - self: The main object pointer.
        - point: A co.cv.cvPoint Point.
        """

        cvPoint = co.cv.cvPoint( point.x, point.y )

        self.img_lkpoints["current"] = [ co.cv.cvPointTo32f ( cvPoint ) ]

        if self.img_lkpoints["current"]:
            co.cv.cvFindCornerSubPix (
                self.grey,
                self.img_lkpoints["current"],
                co.cv.cvSize (20, 20), co.cv.cvSize (-1, -1),
                co.cv.cvTermCriteria (co.cv.CV_TERMCRIT_ITER | co.cv.CV_TERMCRIT_EPS, 20, 0.03))

            point.set_opencv( cvPoint )
            self.img_lkpoints["points"].append(point)

            setattr(point.parent, point.label, point)

            if len(self.img_lkpoints["last"]) > 0:
                self.img_lkpoints["last"].append( self.img_lkpoints["current"][0] )

            debug.debug( "ocvfw", "cmSetLKPoints: New LK Point Added" )
        else:
            self.img_lkpoints["current"] = []

    def clean_lkpoints(self):
        """
        Cleans all the registered points.

        Arguments:
        - self: The main object pointer
        """

        self.img_lkpoints = { "current" : [],
                              "last"    : [],
                              "points"  : [] }

    def show_lkpoints(self):
        """
        Callculate the optical flow of the set points and draw them in the image.

        Arguments:
        - self: The main object pointer.
        """

        # calculate the optical flow
        optical_flow = co.cv.cvCalcOpticalFlowPyrLK (
            self.prevGrey, self.grey, self.prevPyramid, self.pyramid,
            self.img_lkpoints["last"], len( self.img_lkpoints["last"] ),
            co.cv.cvSize (20, 20), 3, len( self.img_lkpoints["last"] ), None,
            co.cv.cvTermCriteria (co.cv.CV_TERMCRIT_ITER|co.cv.CV_TERMCRIT_EPS, 20, 0.03), 0)

        if isinstance(optical_flow[0], tuple):
            self.img_lkpoints["current"], status = optical_flow[0]
        else:
            self.img_lkpoints["current"], status = optical_flow


        # initializations
        counter = 0
        new_points = []

        for point in self.img_lkpoints["current"]:

            if not status[counter]:
                continue

            # this point is a correct point
            current = self.img_lkpoints["points"][counter]
            current.set_opencv(co.cv.cvPoint(int(point.x), int(point.y)))

            new_points.append( point )

            setattr(current.parent, current.label, current)

            # draw the current point
            current.parent.draw_point(point.x, point.y)

            # increment the counter
            counter += 1


        #debug.debug( "ocvfw", "cmShowLKPoints: Showing %d LK Points" % counter )

        # set back the self.imgPoints we keep
        self.img_lkpoints["current"] = new_points


    def swap_lkpoints(self):
        """
        Swap the LK method variables so the new points will be the last points.
        This function has to be called after showing the new points.

        Arguments:
        - self: The main object pointer.
        """

        # swapping
        self.prevGrey, self.grey               = self.grey, self.prevGrey
        self.prevPyramid, self.pyramid         = self.pyramid, self.prevPyramid
        self.img_lkpoints["last"], self.img_lkpoints["current"] = \
                                   self.img_lkpoints["current"], self.img_lkpoints["last"]


