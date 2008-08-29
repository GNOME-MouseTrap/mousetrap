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

userPref = { 'showMainGui'      : 'checkButton',
              'startCam'         : 'checkButton',
              'showPointMapper'  : 'checkButton',
              'showCapture'      : 'checkButton',
              'flipImage'        : 'checkButton',
              'stepSpeed'        : 'spinButton',
              'debugLevel'       : 'spinButton',
              'inputDevIndex'    : 'spinButton',
              'mouseMode'        : 'label',
              'defClick'         : 'label'}
                          

def writePref( widgets ):
    """
    Writes the prefferences into the user prefferences file.
    
    Arguments:
    - widgets: A dict() with all the preference widgets objects
    """
    
    prefFile = open( env.configFile, 'w' )
    
    _writeHeader( prefFile)
    
    for uP in userPref.keys():
        prefFile.write("\n\n#" + uP)
        if userPref[uP] == 'checkButton':
            prefFile.write("\n%s = %s" % (uP, str(widgets[uP].get_active())))
        elif userPref[uP] == 'spinButton':
            prefFile.write("\n%s = %s" % (uP, str(widgets[uP].get_value_as_int())))
        elif userPref[uP] == 'label':
            prefFile.write("\n%s = \"%s\"" % (uP, str(widgets[uP].get_label())))

    prefFile.write("\n")
    prefFile.close()

          
def _writeHeader( prefFile ):
    """
    Writes the header comments of the preference file.
    
    Arguments:
    - prefFile: The opened prefferences file object
    """
    
    prefFile.write("# -*- coding: utf-8 -*-")
    prefFile.write( _( "\n# This is the user settings File" ) )
    prefFile.write( _( "\n# Please Try to don't edit this file manually" ) )
    prefFile.write( _( "\n# Use the preffGui of mouseTrap.\n" ) )
    
def writeFirstConf():
    
    prefFile = open( env.configFile, 'w' )
    
    _writeHeader( prefFile)
    
    prefFile.write("\n#flipImage\n")
    prefFile.write("flipImage = False\n")

    prefFile.write("\n#showCapture\n")
    prefFile.write("showCapture = True\n")

    prefFile.write("\n#stepSpeed\n")
    prefFile.write("stepSpeed = 5\n")

    prefFile.write("\n#showPointMapper\n")
    prefFile.write("showPointMapper = True\n")

    prefFile.write("\n#startCam\n")
    prefFile.write("startCam = True\n")

    prefFile.write("\n#reqMovement\n")
    prefFile.write("reqMovement = 10\n")

    prefFile.write("\n#mouseMode\n")
    prefFile.write("mouseMode = 'screen|none'\n")

    prefFile.write("\n#inputDevIndex\n")
    prefFile.write("inputDevIndex = 0\n")

    prefFile.write("\n#debugLevel\n")
    prefFile.write("debugLevel = 1000\n")

    prefFile.write("\n#defClick\n")
    prefFile.write("defClick = 'b1c'\n")

    prefFile.write("\n#showMainGui\n")
    prefFile.write("showMainGui = True\n")
    
    prefFile.write("\n")
    prefFile.close()
