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

__id__ = "$Id$"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__ = "GPLv2"

import cv2


class Camera(object):

    def __init__(self, device_id=0):
        self._device_id = device_id
        self._capture = None

    def start_camera(self):
        self._capture = cv2.VideoCapture(self._device_id)

    def get_image(self):
        if not self.is_started():
            raise CameraError("Camera has not been started.")
        return self._read_image()

    def is_started(self):
        return self._capture is not None and self._capture.isOpened()

    def _read_image(self):
        read_was_successful, image = self._capture.read()
        if not read_was_successful:
            raise CameraError("Read was not successful.")
        return image


class CameraError(Exception):

    def __init__(self, message):
        super(CameraError, self).__init__()
        self.message = message
