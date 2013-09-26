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
import debug
import commons as co
import cv2 #remove
import cv2.cv as cv
import numpy
import array

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
        """
        if hasattr(self, "%s" % key):
            getattr(self, "%s" % key)(value)
            debug.debug("_ocv - set", "Changed %s value to %s" % (key, value))
            return True

        debug.debug("_ocv - set", "%s not found" % (key))
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

        #if type(size) == "<type 'tuple'>":
            #size = co.cv.cvSize( size[0], size[1])
        return co.cv.CreateImage( (size[0], size[1]), num, ch)# was size'

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
        Simple call to the co.cv.WaitKey function, which has to be called periodically.

        Arguments:
        - self: The main object pointer.
        - num: An int value.
        """
        return co.cv.WaitKey(num)

    def start_camera(self, params = None):
        """
        Starts the camera capture

        Arguments:
        - params: A list with the capture properties. NOTE: Not implemented yet.
        """
        self.capture = cv.CaptureFromCAM(self.idx )

        debug.debug( "ocvfw", "start_camera: Camera Started" )

    def query_image(self, bgr=False, flip=False):
        """
        Queries the new frame.

        Arguments:
        - self: The main object pointer.
        - bgr: If True. The image will be converted from RGB to BGR.

        Returns The image even if it was stored in self.img
        """

        frame = cv.QueryFrame( self.capture )

        #Test to make sure camera starts properly
        #cv.ShowImage("webcam", frame)


        if not  self.img:
            self.storage        = co.cv.CreateMemStorage(0)
            self.imgSize        = co.cv.GetSize (frame)
            self.img            = co.cv.CreateImage ( self.imgSize, 8, 3 )
            #self.img.origin     = frame.origin
            self.grey           = co.cv.CreateImage ( self.imgSize, 8, 1 )
            self.yCrCb          = co.cv.CreateImage ( self.imgSize, 8, 3 )
            self.prevGrey       = co.cv.CreateImage ( self.imgSize, 8, 1 )
            self.pyramid        = co.cv.CreateImage ( self.imgSize, 8, 1 )
            self.prevPyramid    = co.cv.CreateImage ( self.imgSize, 8, 1 )
            #a = co.cv.Round(self.img.width/self.imageScale)
            #b = co.cv.Round(self.img.height/self.imageScale)
            #c = (a, b)
            self.small_img      = co.cv.CreateImage(
                                ( co.cv.Round(self.img.width/self.imageScale),
                                  co.cv.Round(self.img.height/self.imageScale) ),
                                8, 3 )

        self.img = frame

        self.wait_key(10)
        return True

    def set_lkpoint(self, point):
        """
        Set a point to follow it using the L. Kallman method.

        Arguments:
        - self: The main object pointer.
        - point: A co.cv.Point Point.
        """

        #Point = co.cv.Point( point.x, point.y )

        self.img_lkpoints["current"] = numpy.zeros((point.x, point.y), numpy.float32)
        self.img_lkpoints["current"] = cv.fromarray(self.img_lkpoints["current"])

        self.grey = numpy.asarray(self.grey[:,:])        #new

        if numpy.all(self.img_lkpoints["current"]):
            #co.cv.FindCornerSubPix(
            cv2.cornerSubPix(                                # was cv.FindCornerSubPix
                self.grey,
                self.img_lkpoints["current"],
                (20, 20), (0,0),
                (cv.CV_TERMCRIT_ITER | cv.CV_TERMCRIT_EPS, 20, 0.03))
            point.set_opencv( point )
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
        Calculate the optical flow of the set points and draw them in the image.

        Arguments:
        - self: The main object pointer.
        """

        self.prevGrey = numpy.asarray(self.prevGrey[:,:])
        prevGrey = cv2.cvtColor(self.prevGrey, cv2.COLOR_BGR2GRAY)

        self.grey = numpy.asarray(self.grey[:,:])
        grey = cv2.cvtColor(self.grey, cv2.COLOR_BGR2GRAY)

           # calculate the optical flow
        nextPts, status, err = cv2.calcOpticalFlowPyrLK (
            prevGrey, #prevImg
            grey, #nextImg
                self.prevPyramid, #prevPts
                self.pyramid, #nextPts
                None, #status
                (20, 20), #winSize
                2, #maxLevel
                (cv2.TERM_CRITERIA_MAX_ITER|cv2.TERM_CRITERIA_EPS, 20, 0.03), #criteria
                cv2.OPTFLOW_USE_INITIAL_FLOW #flags
                )
        cv.ShowImage("test",self.grey)

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
            current.set_opencv(co.cv.Point(int(point.x), int(point.y)))

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


class OcvfwCtypes(OcvfwBase):
    """
    This Class controlls the main camera functions.
    It works as a little framework for Opencv.cv.

    This Backend uses ctypes opencv python bindings.
    """


    def __init__(self):
        """
        Initialize the module and set its main variables.
        """
        co.cv = __import__("pyopencv.cv",
                        globals(),
                        locals(),
                        [''])

        co.hg = __import__("pyopencv.cv",
                        globals(),
                        locals(),
                        [''])#should be removed

        OcvfwBase.__init__(self)


class OcvfwPython(OcvfwBase):
    """
    This Class controlls the main camera functions.
    It works as a little framework for Openco.cv.

    This Backend uses normal opencv python bindings.
    """

    co.cv = __import__("cv",
                        globals(),
                        locals(),
                        [''])

    co.hg = __import__("cv",
                        globals(),
                        locals(),
                        ['']) #should be removed

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

        font = co.cv.InitFont ( font, 1, 1, 0.0, 1, co.cv.CV_AA)
        textSize, ymin = co.cv.GetTextSize (message, font)
        pt1 = (( self.img.width - textSize.width ) / 2 , 20 )
        co.cv.PutText (self.img, message, pt1, font, co.cv.Scalar (255, 0, 0))

    def get_haar_points(self, haarCascade, method=co.cv.CV_HAAR_DO_CANNY_PRUNING):
        """
        Search for points matching the haarcascade selected.

        Arguments:
        - self: The main object pointer.
        - haarCascade: The selected cascade.
        - methode: The search method to use. DEFAULT: co.cv.CV_HAAR_DO_CANNY_PRUNING.

        Returns a list with the matches.
        """

        cascade = co.cv.Load( haarCascade) #, self.imgSize )

        if not cascade:
            debug.exception( "ocvfw", "The Haar Classifier Cascade load failed" )

        co.cv.Resize( self.img, self.small_img, co.cv.CV_INTER_LINEAR )

        #co.cv.ClearMemStorage( self.storage )

        points = co.cv.HaarDetectObjects( self.small_img, cascade, self.storage, 1.2, 2, method, (20, 20) )

        if points:
            matches = [ [ ( int(r[0][0]*self.imageScale), int(r[0][1]*self.imageScale)), \
                        ( int((r[0][0]+r[0][3])*self.imageScale), int((r[0][0]+r[0][2])*self.imageScale) )] \
                        for r in points]

            debug.debug( "ocvfw", "cmGetHaarPoints: detected some matches" )
            debug.debug("ocvfw-getHaarPoints", matches)
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
        cascade = co.cv.Load( haarCascade ) #, self.imgSize )
        if not cascade:
            debug.exception( "ocvfw", "The Haar Classifier Cascade load failed" )

        debug.debug( "ocvfw-get_haar_roi_points", self.img)

        #FIXME: Work around to fix when the rect is too big
        if (rect[0]+rect[2]) > self.img.width:
            rect = (rect[0], rect[1], self.img.width-rect[0],self.img.height-rect[1])
        if (rect[1]+rect[3]) > self.img.height:
            rect = (rect[0], rect[1], self.img.width-rect[0],self.img.height-rect[1])

        debug.debug("before GetSubRect - rect",rect)
        debug.debug("before GetSubRect - self.img", self.img)
        imageROI = co.cv.GetSubRect(self.img, rect)

        if cascade:
            points = co.cv.HaarDetectObjects( imageROI, cascade, self.storage,
                                    1.2, 2, method, (20,20) )
        else:
            debug.exception( "ocvfw", "The Haar Classifier Cascade load Failed (ROI)" )

        if points:
            matches = [ [ ( int(r[0][0]*origSize[0]), int(r[0][1]*origSize[1])), \
                          ( int((r[0][0]+r[0][3])+origSize[0]), int((r[0][1]+r[0][2])*origSize[1]) )] \
                          for r in points]
            #matches = [ [ ( int(r[0][0]), int(r[0][1])), \
             #             ( int((r[0][0]+r[0][3])), int((r[0][1]+r[0][2])) )] \
              #            for r in points]
           #FIXME: I don't think the  matches are right

            debug.debug( "ocvfw", "cmGetHaarROIPoints: detected some matches" )
            debug.debug("ocvfw-getHaarROIPoints", matches)
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
            img     = co.cv.GetSubRect( self.img, imgRoi )
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
            self.mask       = co.cv.CreateImage( imgSize,  8, 1 )
            self.mhi        = co.cv.CreateImage( imgSize, 32, 1 )
            self.orient     = co.cv.CreateImage( imgSize, 32, 1 )
            self.segmask    = co.cv.CreateImage( imgSize, 32, 1 )

            co.cv.SetZero( self.mhi )

            for i in range( n_ ):
                self.buf[i] = co.cv.CreateImage( imgSize, 8, 1 )
                co.cv.cvZero( self.buf[i] )

        idx1 = self.lastFm

        # convert frame to grayscale
        cv2.cvtColor( img, self.buf[self.lastFm], cv2.CV_BGR2GRAY )

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

            center = co.cv.Point( (mRect.x + mRect.width/2), (mRect.y + mRect.height/2) )

            silhRoi = co.cv.cvGetSubRect(silh, mRect)
            count = co.cv.cvNorm( silhRoi, None, co.cv.CV_L1, None )

             # calculate number of points within silhouette ROI
            if( count < mRect.width * mRect.height * 0.05 ):
                continue

            mv.append(center)

        return mv

