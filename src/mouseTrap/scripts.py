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

import os
import gtk
import debug
import events
import environment as env

from mouseTrap import settings
from mTi18n import _

## A dict to store the diferente loaded modes profiles.
modes = {}

## loaded profile
loaded = None
                       
def _loadThirdProfiles():
    """
    This function loads the external profiles created by the users
    """
    
    global modes
    
    os.chdir( env.profilesPath )
    
    mods = [ file.split(".py")[0] for file in os.listdir( env.profilesPath ) if file.endswith(".py") ]

    for mod in mods:
        try:
            prof = __import__( mod, globals(), locals(), [''] )
            modes[prof.setName] = prof.Profile
            env.mouseModes.update( prof.modes )
        except:
            debug.log( debug.MODULES, _( "Highest" ) )

def loadProfile( gui ):
    """
    Loads the profile selected in the settings
    
    Arguments:
    - gui: The main gui object pointer.
    """
    global loaded
    
    if not modes:
        _loadThirdProfiles()
        
    loaded = modes[settings.mouseMode.split("|")[0]]( gui )
