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

import os
import mousetrap.ocvfw.debug as debug
import mousetrap.ocvfw.commons as co
from mousetrap.ocvfw.dev.camera import Capture, Point, Graphic
from threading import Timer

a_name = "Finger"
a_description = "Finger point tracker based on LK Algorithm"
a_settings = { "speed" : {"value":2 }, 
               "conf_path" : "%s/.finger" % os.path.expanduser("~")}

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
        self.tmpl          = None

        self.timer         = None

        self.prepare_config()
        debug.info("mousetrap.ocvfw.idm", "Finger Algorithm loaded")

    def prepare_config(self):
        """
        Prepares the IDM using the settings
        
        Arguments:
        - self: The main object pointer
        """
        global a_settings

        for key in self.stgs:
            a_settings[key] = self.stgs[key]

        self.stgs = a_settings

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
        if not hasattr(self.cap, "finger"):
            self.follow_finger()

    def get_capture(self):
        """
        Sets the forehead point if needed and returns the formated image.

        Arguments:
        - self: The main object pointer

        returns self.cap.image()
        """

        if not hasattr(self.cap, "finger") and not hasattr(self.cap, "finger"):
            self.get_template()

        return self.cap

    def get_template(self):
        """
        Sets the template capture rectangle.

        Arguments:
        - self: The main object pointer
        """

        self.cap.add(Graphic("rect", "tpl_rect", ( 325, 325 ), (425, 425), parent=self.cap))
        self.timer = Timer(10.0, self.follow_finger)
        self.timer.start()

    def cap_template(self):
        """
        Captures the template

        Arguments:
        - self: The main object pointer.
        """

        debug.debug("finger", "Trying to save capture template")
        self.timer.cancel()
        self.cap.save(os.path.abspath("%s/tmpl.jpg" % self.stgs["conf_path"]), self.cap.rect(100, 100, 150, 150))

    def load_template(self):
        """
        Loads the finger template if exists

        Arguments:
        - self: The main object pointer.
        """

        try:
            self.tmpl = co.hg.cvLoadImage("%s/tmpl.jpg" % self.stgs["conf_path"], 3)
            debug.debug("finger", "Loading template")
        except:
            pass


    def get_pointer(self):
        """
        Returns the new MousePosition

        Arguments:
        - self: The main object pointer
        """

        if hasattr(self.cap, "finger"):
            return self.cap.finger

    def follow_finger(self):
        self.cap.add( Point("point", "finger", ( 375, 375 ), parent=self.cap, follow=True) )

