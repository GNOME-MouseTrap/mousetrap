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

"""The Camera module of mouseTrap."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import sys

try:
    import gtk
except ImportError, e:
    module = e.message.split()[-1]
    sys.stderr.write( "\nmouseTrap needs %s to work correctly. " % module  
    + "\nPlease check if the file exist in " 
    + " the folder or if it is installed.\n" )
    sys.exit(0)
    
import time
import ocvfw
import debug
import gobject
import environment as env

import mouseTrap
from mTi18n import _

try:
    from opencv import cv
    from opencv import highgui
except:
    print "This modules depends of opencv libraries"

        
class Camera( ocvfw.ocvfw ):
    """
    The Camera module main class.
    
    Arguments:
    - cmCameraMod: cmCameraMod Class
    """
    
    def __init__( self ):
        """
        The Camera Class Constructor.
        
        Initialize the cmCameraMod class and sets the needed attributes.
        
        Arguments:
        - self: The main object pointer.
        - mouseTrap: The mouseTrap object pointer.
        """
        
        ocvfw.ocvfw.__init__(self)

        self.run          = True
        self.mTp          = mouseTrap
        self.settings     = mouseTrap.settings
        
        ##############################
        #  MOTION RELATED VARIABLES  #
        ##############################        
        
        self.step         = self.settings.getint( "mouse", "stepSpeed" )
        self.forehead     = None
        self.foreheadLast = None
        self.foreheadOrig = None
        self.foreheadDiff = None
        self.stopMove     = None
        self.startMove    = None
        self.haarCds      = { 'Face'  :  env.haarcascades + "/haarcascade_frontalface_alt.xml",
                              'Eyes'  :  env.haarcascades + "/frontalEyes35x16.xml",
                              'Mouth' :  env.haarcascades + "/Mouth.xml"}
        

        ##############################
        #       ACTION POINTS        #
        ##############################
        self.mpPointer       = None
                                      
        ##############################
        #  CLICK RELATED VARIABLES   #
        ##############################
        
        self.isMoving       = False
        
        ##############################
        #   BLINK RELATED VARIABLES  #
        ##############################
        
        self.blink = False
        self.lastBlink = time.time()
        
        
    def start( self ):
        """
        Starts the capture and the Camera GUI.
        
        Arguments:
        - self: The main object pointer.
        """
        
        try:
            self.cmStartCamera( self.settings.getint( "cam", "inputDevIndex" ) )
            
            if( self.capture ):
                gobject.timeout_add(100, self._checkImg)
                
        except:
            debug.exception( "mouseTrap.cam", "The Camera Module load failed." )
 
          
    def _checkImg( self ):
        """
        Perform the checks to the image and the capture  actions.
        
        Arguments:
        - self: The main object pointer.
        """
        
        self.cmQueryCapture( flip = self.settings.getboolean( "cam", "flipImage" ) )
        
        # create a self.gray version of the self.img
        cv.cvCvtColor (self.img, self.grey, cv.CV_BGR2GRAY)

        #if not self.foreheadOrig and not self.forehead:
        if not self.imgLKPoints["last"]:
            self._setForehead( self.cmGetHaarPoints( self.haarCds['Face'] ) )

        if len(self.imgLKPoints["last"]) > 0:
            self.cmShowLKPoints()
            self._procCapture()
        
        self.cmSwapLKPoints()

        #if self.forehead:
         #   cv.cvRectangle( self.img, cv.cvPoint( self.forehead.x - 100, self.forehead.y ), 
          # cv.cvPoint( self.forehead.x, self.forehead.y + 70 ), cv.CV_RGB(255,0,0), 3, 8, 0 );  
           # self.checkBlink()
            
        # we can now display the self.img
        highgui.cvConvertImage( self.img, self.img, highgui.CV_CVTIMG_SWAP_RB )
        mouseTrap.updateView( self.img )
        
        # handle events
        c = self.cmWaitKey(10)
        return self.run


    def _setForehead( self, face ):
        """
        Detect the forehead point and set it.
        
        Arguments:
        - self: The main object pointer.
        - points: A list with the cv.cvPoints detected.
        """
        
        self.cmAddMessage("Getting Forehead!!!")

        if face:
            areas = [ (pt[1].x - pt[0].x)*(pt[1].y - pt[0].y) for pt in face]
            
            startF   = face[areas.index(max(areas))][0]
            endF     = face[areas.index(max(areas))][1]

        #eyes = self.cmGetHaarPoints( self.haarCds['Eyes'] )

        if not face:
            return True

        rec  = cv.cvRect( startF.x, startF.y,  endF.x - startF.x, endF.y - startF.y )

        eyes = self.cmGetHaarROIPoints( self.haarCds['Eyes'], rec, (startF.x, startF.y) )

        if eyes:
            areas = [ (pt[1].x - pt[0].x)*(pt[1].y - pt[0].y) for pt in eyes ]
                    #if pt[0].x in range(startF.x, endF.x) and pt[0].y in range(startF.y, endF.y) ]

            point1   = eyes[areas.index(max(areas))][0]
            point2   = eyes[areas.index(max(areas))][1]

            X = ( (point1.x + point2.x) / 2 )
            Y = ( point1.y + ( (point1.y + point2.y) / 2 ) ) / 2
            
            self.foreheadOrig = self.foreheadLast = cv.cvPoint( X, Y )
            self.cmSetLKPoints("forehead", self.foreheadOrig)
            return
                
        self.foreheadOrig = None
        
        
    def _procCapture( self ):
        """
        Process the points information ( [X, Y] positions ) and perform the movements/clicks calls.
        
        Arguments:
        - self: The main object pointer.
        """
        
        self.foreheadDiff = cv.cvPoint( self.foreheadLast.x - self.forehead.x, 
                                        self.foreheadLast.y - self.forehead.y )
                                        
        # This helps to forbid None points to pass through
        if self.forehead is None or self.foreheadOrig is None:
            return self.cmCleanLKPoints()
        
        self.mpPointer = cv.cvPoint( 100 - (self.forehead.x - self.foreheadOrig.x),
                                        80 + (self.forehead.y - self.foreheadOrig.y))

        #if abs(self.foreheadLast.x - self.forehead.x) >= 15 or \
         #       abs(self.foreheadLast.y - self.forehead.y) >= 15:
            
          #  self.forehead = self.foreheadLast
           # self.imgLKPoints["current"] = self.imgLKPoints["last"]
        
        self.foreheadLast = self.forehead
        
    def checkBlink( self ):
        points = self.cmGetMotionPoints( cv.cvRect( self.forehead.x - 100, 
                                                    self.forehead.y, 
                                                    100, 70) )

        curTime = time.time()
        
        for point in points:
            
            if self.blink:
                self.blink = False
                if curTime - self.lastBlink > 0.5 and curTime - self.lastBlink < 2.5:
                    print point
            else:
                self.blink = True
                self.lastBlink = time.time()

    def stop( self ):
        """
        Stops the capture
        
        Arguments:
        - self: The main object pointer.
        """
        self.run = False
