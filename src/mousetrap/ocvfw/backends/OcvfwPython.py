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

class OcvfwPython(OcvfwBase):
    """
    This Class controlls the main camera functions.
    It works as a little framework for Openco.cv.

    This Backend uses normal opencv python bindings.
    """

    co.cv = __import__("opencv.cv",
                        globals(),
                        locals(),
                        [''])
        
    co.hg = __import__("opencv.highgui",
                        globals(),
                        locals(),
                        [''])

    def __init__( self ):
        """
        Initialize the module and set its main variables.
        """

        OcvfwBase.__init__(self)

    def add_message(self, message, font=co.cv.CV_FONT_HERSHEY_COMPLEX, poss=None):
        """
        Write a message into the image.

        Arguments:
        - self: The main object pointer.
        - message: A string with the message.
        - font: An OpenCV font to use.
        - poss: The position of the message in the image. NOTE: Not enabled yet.
        """

        font = co.cv.cvInitFont ( font, 1, 1, 0.0, 1, co.cv.CV_AA)
        textSize, ymin = co.cv.cvGetTextSize (message, font)
        pt1 = co.cv.cvPoint ( ( self.img.width - textSize.width ) / 2 , 20 )
        co.cv.cvPutText (self.img, message, pt1, font, co.cv.cvScalar (255, 0, 0))

    def get_haar_points(self, haarCascade, method=co.cv.CV_HAAR_DO_CANNY_PRUNING):
        """
        Search for points matching the haarcascade selected.

        Arguments:
        - self: The main object pointer.
        - haarCascade: The selected cascade.
        - methode: The search method to use. DEFAULT: co.cv.CV_HAAR_DO_CANNY_PRUNING.

        Returns a list with the matches.
        """

        cascade = co.cv.cvLoadHaarClassifierCascade( haarCascade, self.imgSize )

        if not cascade:
            debug.exception( "ocvfw", "The Haar Classifier Cascade load failed" )

        co.cv.cvResize( self.img, self.small_img, co.cv.CV_INTER_LINEAR )

        co.cv.cvClearMemStorage( self.storage )

        points = co.cv.cvHaarDetectObjects( self.small_img, cascade, self.storage, 1.2, 2, method, co.cv.cvSize(20, 20) )

        if points:
            matches = [ [ co.cv.cvPoint( int(r.x*self.imageScale), int(r.y*self.imageScale)), \
                          co.cv.cvPoint( int((r.x+r.width)*self.imageScale), int((r.y+r.height)*self.imageScale) )] \
                          for r in points]
            debug.debug( "ocvfw", "cmGetHaarPoints: detected some matches" )
            return matches

    def get_haar_roi_points(self, haarCascade, rect, origSize=(0, 0), method=co.cv.CV_HAAR_DO_CANNY_PRUNING):
        """
        Search for points matching the haarcascade selected.

        Arguments:
        - self: The main object pointer.
        - haarCascade: The selected cascade.
        - methode: The search method to use. DEFAULT: co.cv.CV_HAAR_DO_CANNY_PRUNING.

        Returns a list with the matches.
        """

        cascade = co.cv.cvLoadHaarClassifierCascade( haarCascade, self.imgSize )

        if not cascade:
            debug.exception( "ocvfw", "The Haar Classifier Cascade load failed" )

        co.cv.cvClearMemStorage(self.storage)

        imageROI = co.cv.cvGetSubRect(self.img, rect)

        if cascade:
            points = co.cv.cvHaarDetectObjects( imageROI, cascade, self.storage,
                                    1.2, 2, method, co.cv.cvSize(20,20) )
        else:
            debug.exception( "ocvfw", "The Haar Classifier Cascade load Failed (ROI)" )

        if points:
            matches = [ [ co.cv.cvPoint( int(r.x+origSize[0]), int(r.y+origSize[1])), \
                          co.cv.cvPoint( int(r.x+r.width+origSize[0]), int(r.y+r.height+origSize[1] ))] \
                          for r in points]

            debug.debug( "ocvfw", "cmGetHaarROIPoints: detected some matches" )
            return matches




    ##########################################
    #                                        #
    #          THIS IS NOT USED YET          #
    #                                        #
    ##########################################
    def get_motion_points(self, imgRoi=None):
        """
        Calculate the motion points in the image.

        Arguments:
        - self: The main object pointer.
        - start: The start ROI point.
        - end: The end ROI point.
        - num: The nomber of points to return

        Returns A list with the points found.
        """

        mv = []
        n_ = 4

        timestamp = time.clock()/1.0

        if imgRoi:
            img     = co.cv.cvGetSubRect( self.img, imgRoi )
            imgSize = co.cv.cvSize( imgRoi.width, imgRoi.height )
            self.imgRoi = img
        else:
            img     = self.img
            imgSize = self.imgSize

        # Motion Related Variables
        if not self.mhi or self.mhi.width != imgSize.width or self.mhi.height != imgSize.height:
            self.buf        = [ 0, 0, 0, 0 ]
            self.lastFm     = 0
            self.mhiD       = 1
            self.maxTD      = 0.5
            self.minTD      = 0.05
            self.mask       = co.cv.cvCreateImage( imgSize,  8, 1 )
            self.mhi        = co.cv.cvCreateImage( imgSize, 32, 1 )
            self.orient     = co.cv.cvCreateImage( imgSize, 32, 1 )
            self.segmask    = co.cv.cvCreateImage( imgSize, 32, 1 )

            co.cv.cvZero( self.mhi )

            for i in range( n_ ):
                self.buf[i] = co.cv.cvCreateImage( imgSize, 8, 1 )
                co.cv.cvZero( self.buf[i] )

        idx1 = self.lastFm

        # convert frame to grayscale
        co.cv.cvCvtColor( img, self.buf[self.lastFm], co.cv.CV_BGR2GRAY )

        # index of (self.lastFm - (n_-1))th frame
        idx2 = ( self.lastFm + 1 ) % n_
        self.lastFm = idx2

        silh = self.buf[idx2]

        # Get difference between frames
        co.cv.cvAbsDiff( self.buf[idx1], self.buf[idx2], silh )

        # Threshold it
        co.cv.cvThreshold( silh, silh, 30, 1, co.cv.CV_THRESH_BINARY )

        # Update MHI
        co.cv.cvUpdateMotionHistory( silh, self.mhi, timestamp, self.mhiD )

        co.cv.cvCvtScale( self.mhi, self.mask, 255./self.mhiD, (self.mhiD - timestamp)*255./self.mhiD )

        co.cv.cvCalcMotionGradient( self.mhi, self.mask, self.orient, self.maxTD, self.minTD, 3 )

        co.cv.cvClearMemStorage( self.storage )

        seq = co.cv.cvSegmentMotion( self.mhi, self.segmask, self.storage, timestamp, self.maxTD )

        for i in range(0, seq.total):
            if i < 0:  # case of the whole image
                continue
            else:  # i-th motion component
                # Movement Rectangle
                mRect = seq[i].rect

                # reject very small components
                if( mRect.width + mRect.height < 30 ):
                    continue

            center = co.cv.cvPoint( (mRect.x + mRect.width/2), (mRect.y + mRect.height/2) )

            silhRoi = co.cv.cvGetSubRect(silh, mRect)
            count = co.cv.cvNorm( silhRoi, None, co.cv.CV_L1, None )

             # calculate number of points within silhouette ROI
            if( count < mRect.width * mRect.height * 0.05 ):
                continue

            mv.append(center)

        return mv
