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
# along with mouseTrap.  If not, see <http://www.gnu.org/licenses/>..

"""Little  Framework for OpenCV Library."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import gtk
import time
import mouse
import debug
import gobject
from math import cos,sin,sqrt, pi
import environment as env

try:
    import opencv
    from opencv import cv
    from opencv import highgui
except:
    print "This modules depends of opencv libraries"


class ocvfw:
    """
    This Class controlls the main camera functions. 
    It works as a little framework for OpenCV.
    """
    
    def __init__( self ):
        """
        Initialize the module and set its main variables.
        """
        
        self.img          = None
        self.mhi          = None
        self.imgLKPoints  = { "current" : [], 
                              "last"    : [], 
                              "labels"  : [] }
        self.imageScale   = 1.5
        
        
    def cmAddMessage(self, message, font = cv.CV_FONT_HERSHEY_COMPLEX, poss = None ):
        """
        Write a message into the image.
        
        Arguments:
        - self: The main object pointer.
        - message: A string with the message.
        - font: An OpenCV font to use.
        - poss: The position of the message in the image. NOTE: Not enabled yet.
        """
        
        font = cv.cvInitFont ( font, 1, 1, 0.0, 1, cv.CV_AA)
        textSize, ymin = cv.cvGetTextSize (message, font)
        pt1 = cv.cvPoint ( ( self.img.width - textSize.width ) / 2 , 20 )
        cv.cvPutText (self.img, message, pt1, font, cv.cvScalar (255, 0, 0))
        
    def cmGetHaarPoints( self, haarCascade, method = cv.CV_HAAR_DO_CANNY_PRUNING ):
        """
        Search for points matching the haarcascade selected.
        
        Arguments:
        - self: The main object pointer.
        - haarCascade: The selected cascade.
        - methode: The search method to use. DEFAULT: cv.CV_HAAR_DO_CANNY_PRUNING.
        
        Returns a list with the matches.
        """

        cascade = cv.cvLoadHaarClassifierCascade( haarCascade, self.imgSize )
        
        cv.cvResize( self.img, self.smallImg, cv.CV_INTER_LINEAR )
        
        cv.cvClearMemStorage( self.storage )
        
        if cascade:
            points = cv.cvHaarDetectObjects( self.smallImg, cascade, self.storage,
                                    1.2, 2, method, cv.cvSize(20,20) )
        else:
            debug.exception( "ocvfw", "The Haar Classifier Cascade load failed" )

        if points:
            matches = [ [ cv.cvPoint( int(r.x*self.imageScale), int(r.y*self.imageScale)), \
                          cv.cvPoint( int((r.x+r.width)*self.imageScale), int((r.y+r.height)*self.imageScale) )] \
                          for r in points]
            
            debug.debug( "ocvfw", "cmGetHaarPoints: detected some matches" )
            return matches

    def cmGetHaarROIPoints( self, haarCascade, rect, origSize = (0,0), method = cv.CV_HAAR_DO_CANNY_PRUNING ):
        """
        Search for points matching the haarcascade selected.
        
        Arguments:
        - self: The main object pointer.
        - haarCascade: The selected cascade.
        - methode: The search method to use. DEFAULT: cv.CV_HAAR_DO_CANNY_PRUNING.
        
        Returns a list with the matches.
        """

        cascade = cv.cvLoadHaarClassifierCascade( haarCascade, self.imgSize )
        
        cv.cvClearMemStorage( self.storage )

        imageROI = cv.cvGetSubRect( self.img, rect )
        
        if cascade:
            points = cv.cvHaarDetectObjects( imageROI, cascade, self.storage,
                                    1.2, 2, method, cv.cvSize(20,20) )
        else:
            debug.exception( "ocvfw", "The Haar Classifier Cascade load Failed (ROI)" )

        if points:
            matches = [ [ cv.cvPoint( int(r.x+origSize[0]), int(r.y+origSize[1])), \
                          cv.cvPoint( int(r.x+r.width+origSize[0]), int(r.y+r.height+origSize[1] ))] \
                          for r in points]

            debug.debug( "ocvfw", "cmGetHaarROIPoints: detected some matches" )
            return matches
            
    def cmSetLKPoints( self, label, point):
        """
        Set a point to follow it using the L. Kallman method.
        
        Arguments:
        - self: The main object pointer.
        - label: The label to identify the point. Example: "Pointer", so self.Pointer = Pointer.
        - point: A cv.cvPoint Point.
        """
        
        self.imgLKPoints["current"] = [ cv.cvPointTo32f ( point ) ]
        
        if self.imgLKPoints["current"]:
            cv.cvFindCornerSubPix (
                self.grey,
                self.imgLKPoints["current"],
                cv.cvSize (20, 20), cv.cvSize (-1, -1),
                cv.cvTermCriteria (cv.CV_TERMCRIT_ITER | cv.CV_TERMCRIT_EPS, 20, 0.03))
                
            self.imgLKPoints["labels"].append( label )
            setattr(self, label, point)
            
            if len(self.imgLKPoints["last"]) > 0:
                self.imgLKPoints["last"].append( self.imgLKPoints["current"][0] )

            debug.debug( "ocvfw", "cmSetLKPoints: New LK Point Added" )
        else:
            self.imgLKPoints["current"] = []
    
    def cmCleanLKPoints( self ):
        self.imgLKPoints = { "current" : [], 
                             "last"    : [], 
                             "labels"  : [] }
            
    def cmShowLKPoints( self ):
        """
        Callculate the optical flow of the set points and draw them in the image.
        
        Arguments:
        - self: The main object pointer.
        """
        
        # calculate the optical flow
        self.imgLKPoints["current"], status = cv.cvCalcOpticalFlowPyrLK (
            self.prevGrey, self.grey, self.prevPyramid, self.pyramid,
            self.imgLKPoints["last"], len( self.imgLKPoints["last"] ),
            cv.cvSize (20, 20), 3, len( self.imgLKPoints["last"] ), None,
            cv.cvTermCriteria (cv.CV_TERMCRIT_ITER|cv.CV_TERMCRIT_EPS,
                               20, 0.03), 0)

        # initializations
        counter = 0
        new_points = []

        for point in self.imgLKPoints["current"]:
            # go trough all the self.imgPoints

            if not status[counter]:
                # we will disable this point
                continue
            

            # this point is a correct point
            new_points.append( point )
            setattr(self, self.imgLKPoints["labels"][counter], cv.cvPoint(int(point.x), int(point.y)))
            
            # draw the current point
            cv.cvCircle (self.img, [point.x, point.y], 3, cv.cvScalar (0, 255, 0, 0), -1, 8, 0)
                         
            # increment the counter
            counter += 1

        
        #debug.debug( "ocvfw", "cmShowLKPoints: Showing %d LK Points" % counter )
        
        # set back the self.imgPoints we keep
        self.imgLKPoints["current"] = new_points
    
    def cmWaitKey( self, int ):
        """
        Simple call to the highgui.cvWaitKey function, which has to be called periodically.
        
        Arguments:
        - self: The main object pointer.
        """
        return highgui.cvWaitKey( int )
        
    def cmSwapLKPoints( self ):
        """
        Swap the LK method variables so the new points will be the last points.
        This function has to be called after showing the new points.
        
        Arguments:
        - self: The main object pointer.
        """
        
        # swapping
        self.prevGrey, self.grey               = self.grey, self.prevGrey
        self.prevPyramid, self.pyramid         = self.pyramid, self.prevPyramid
        self.imgLKPoints["last"], self.imgLKPoints["current"] = self.imgLKPoints["current"], self.imgLKPoints["last"]
        
    def cmStartCamera( self, input, params = None ):
        """
        Starts the camera capture using highgui.
        
        Arguments:
        - params: A list with the capture properties. NOTE: Not implemented yet.
        """
        self.capture = highgui.cvCreateCameraCapture( int(input) )
        debug.debug( "ocvfw", "cmStartCamera: Camera Started" )
    
    def cmQueryCapture( self, bgr = False, flip = False ):
        """
        Queries the new frame.
        
        Arguments:
        - self: The main object pointer.
        - bgr: If True. The image will be converted from RGB to BGR.
        
        Returns The image even if it was stored in self.img
        """
        
        frame = highgui.cvQueryFrame( self.capture )

        if not  self.img:
            self.storage        = cv.cvCreateMemStorage(0)
            self.imgSize        = cv.cvGetSize (frame)
            self.img            = cv.cvCreateImage ( self.imgSize, 8, 3 )
            self.img.origin     = frame.origin
            self.grey           = cv.cvCreateImage ( self.imgSize, 8, 1 )
            self.yCrCb          = cv.cvCreateImage ( self.imgSize, 8, 3 )
            self.prevGrey       = cv.cvCreateImage ( self.imgSize, 8, 1 )
            self.pyramid        = cv.cvCreateImage ( self.imgSize, 8, 1 )
            self.prevPyramid    = cv.cvCreateImage ( self.imgSize, 8, 1 )
            self.smallImg       = cv.cvCreateImage( cv.cvSize( cv.cvRound ( self.imgSize.width/self.imageScale), 
                                    cv.cvRound ( self.imgSize.height/self.imageScale) ), 8, 3 )
        self.img = frame
        if bgr:
            highgui.cvConvertImage( self.img, self.img, highgui.CV_CVTIMG_SWAP_RB )
            
        if flip:
            cv.cvFlip( self.img, self.img, 1)
        return self.img
        
    def cmGetMotionPoints( self, imgRoi = None):
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
        N = 4
        
        timestamp = time.clock()/1.0

        if imgRoi:
            img     = cv.cvGetSubRect( self.img, imgRoi )
            imgSize = cv.cvSize( imgRoi.width, imgRoi.height )
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
            self.mask       = cv.cvCreateImage( imgSize,  8, 1 )
            self.mhi        = cv.cvCreateImage( imgSize, 32, 1 )
            self.orient     = cv.cvCreateImage( imgSize, 32, 1 )
            self.segmask    = cv.cvCreateImage( imgSize, 32, 1 )
            
            cv.cvZero( self.mhi )
            
            for i in range( N ):
                self.buf[i] = cv.cvCreateImage( imgSize, 8, 1 )
                cv.cvZero( self.buf[i] )
        
        idx1 = self.lastFm
        
        # convert frame to grayscale
        cv.cvCvtColor( img, self.buf[self.lastFm], cv.CV_BGR2GRAY )
        
        # index of (self.lastFm - (N-1))th frame
        idx2 = ( self.lastFm + 1 ) % N 
        self.lastFm = idx2
        
        silh = self.buf[idx2]
        
        # Get difference between frames
        cv.cvAbsDiff( self.buf[idx1], self.buf[idx2], silh ) 
        
        # Threshold it
        cv.cvThreshold( silh, silh, 30, 1, cv.CV_THRESH_BINARY )
        
        # Update MHI
        cv.cvUpdateMotionHistory( silh, self.mhi, timestamp, self.mhiD )
        
        cv.cvCvtScale( self.mhi, self.mask, 255./self.mhiD, (self.mhiD - timestamp)*255./self.mhiD )
        
        cv.cvCalcMotionGradient( self.mhi, self.mask, self.orient, self.maxTD, self.minTD, 3 )
        
        cv.cvClearMemStorage( self.storage )
        
        seq = cv.cvSegmentMotion( self.mhi, self.segmask, self.storage, timestamp, self.maxTD )
        
        for i in range(0, seq.total):
            if i < 0:  # case of the whole image
                continue
            else:  # i-th motion component
                # Movement Rectangle
                mRect = seq[i].rect 
                
                # reject very small components
                if( mRect.width + mRect.height < 30 ):
                    continue
                
            center = cv.cvPoint( (mRect.x + mRect.width/2), (mRect.y + mRect.height/2) )
           
            silhRoi = cv.cvGetSubRect(silh, mRect)
            count = cv.cvNorm( silhRoi, None, cv.CV_L1, None )
            
             # calculate number of points within silhouette ROI
            if( count < mRect.width * mRect.height * 0.05 ):
                continue
            
            mv.append(center)
            
        return mv
