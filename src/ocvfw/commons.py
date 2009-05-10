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

"""Ocvfw Global Vars."""

__id__        = "$Id: _ocv.py 20 2009-02-21 21:34:12Z flaper $"
__version__   = "$Revision: 20 $"
__date__      = "$Date: 2009-02-21 22:34:12 +0100 (sáb 21 de feb de 2009) $"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import os

abs_path = os.path.abspath(os.path.dirname(__file__))

haar_cds = { 'Face'  :  "%s/haars/haarcascade_frontalface_alt.xml" % abs_path,
             'Eyes'  :  "%s/haars/frontalEyes35x16.xml" % abs_path,
             #'Eyes'  :  "../ocvfw/haars/haarcascade_eye_tree_eyeglasses.xml",
             'Mouth' :  "%s/haars/Mouth.xml" % abs_path}
