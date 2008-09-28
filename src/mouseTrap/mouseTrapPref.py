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

""" MouseTrap prefference handler. """

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import environment as env

from mTi18n import _

    
def writeFirstConf():
    
    prefFile = open( env.configFile, 'w' )

    prefFile.write( "[gui]\n" )
    prefFile.write( "showCapture = True\n" )
    prefFile.write( "showMainGui = True\n" )
    prefFile.write( "showPointMapper = True\n" )
    
    prefFile.write( "[access]\n" )
    prefFile.write( "reqMovement = 10\n" )
    
    prefFile.write( "[cam]\n" )
    prefFile.write( "mouseMode = drag|none\n" )
    prefFile.write( "inputDevIndex = 0\n" )
    prefFile.write( "flipImage = False\n" )
        
    prefFile.write( "[main]\n" )
    prefFile.write( "debugLevel = 10\n" )
    prefFile.write( "startCam = True\n" )
    
    prefFile.write( "[mouse]\n" )
    prefFile.write( "defClick = b1c\n" )
    prefFile.write( "stepSpeed = 5\n" )

    prefFile.write("\n")
    prefFile.close()
