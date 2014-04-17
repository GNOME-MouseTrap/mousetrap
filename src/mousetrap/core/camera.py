# -*- coding: utf-8 -*-

# MouseTrap
#
# Copyright 2009 Flavio Percoco Premoli
#
# This file is part of mouseTrap.
#
# MouseTrap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v2 as published
# by the Free Software Foundation.
#
# mouseTrap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mouseTrap.  If not, see <http://www.gnu.org/licenses/>.

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import cv2


class Camera(object):

    def __init__(self, dev=0):
        self.dev_id = None
        self.capture = None
        self.img = None

        self.set_dev_id(dev)
        self.start_camera()

    def start_camera(self):
        """
        Start a new Video capture feed with the Web Camera
        """
        self.capture = cv2.VideoCapture(self.dev_id)

    def set_dev_id(self, dev=0):
        """
        Sets the camera id for the device to be used
        Arguments:
         - dev: The Camera's Id (Default is 0)
        """
        self.dev_id = dev

    def get_image(self):
        """
        Reads a new image from the camera
        Returns the new image
        """
        ret, self.img = self.capture.read()

        return self.img