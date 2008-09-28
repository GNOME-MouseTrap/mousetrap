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

import sys
import time
import debug
import gobject

import mouseTrap
from mouseTrap import settings

# The Locker for the event listener
RUN = True

# The Mapper to check
mapper = None

# A dictionary for the events registered
mapperEvents = dict()

# A list for the registered events
regEvents = []

# A list for the registered triggers 
regTriggers = []

# A dictionary for the conditions that can exist.
conditions = dict()

eventTypes = [ "point-move",  
               "top-left-corner",
               "top-right-corner",
               "bottom-left-corner",
               "bottom-right-corner" ]

def registerArea( area ):
    """
    This function register new events for the Mapper that are going 
    to be executed if the mapper pointer is located inseide the range area
    created by the initCoords and the endCoords selected.

    Arguments:
    - area: The area to be registered.
    """

    global regEvents

    regEvents.append( area )
    debug.debug( "events", "New Area Listener Added" )

def registerTrigger( trigger ):
    """
    This functions is used to register a new trigger.

    Arguments:
    - trigger: A dictionary with the trigger information.
    """

    global regTriggers

    regTriggers.append( trigger )
    
def checkEvents( ):
    """
    Checks if an event is being executed and calls the callback function if
    the conditions supplied are right.
    """

    for area in regEvents:
        for ev in eventTypes:
            for i, reg in enumerate( area.events[ev] ):
                event = area.events[ev][i]
                if event["state"] == mouseTrap.getState() and checkCond( ev, area, i ):
                        event["callback"]( *event["args"], **event["kwds"] )

    for trigger in regTriggers:
        if isAbove( trigger["X"], trigger["Y"]) and isOnTime( trigger["last"], 2):
            trigger["last"] = time.time()
            trigger["callback"]( trigger["args"], trigger["kwds"] )
            
    return RUN

def isOnTime( last, delay ):
    """
    Check if the event can be executed based on the delay time.

    Arguments:
    - last: The last time the event was executed.
    - delay: The delay in seconds
    """
    if time.time() - last >= delay:
        return True

    return False

def isAbove( X, Y ):
    """
    Check if the mouse possition is equal to the X and Y coords

    It use a range of ( x - 2, x + 2) and ( y -2, y + 2 ) so it
    is easier to access the point.

    Arguments:
    - X: The X possition.
    - Y: The Y possition.
    """

    if mapper.pointer[0] in xrange( X - 2, X + 2) and mapper.pointer[1] in xrange( Y - 2, Y + 2):
        return True

    return False

def checkCond( ev, area, i ):
    """
    Checks if any of the possible conditions is being fired.

    Arguments:
    - ev: The event type to check
    - area: The area that is being checked.
    - i: The index in the events to check.
    """
 
    if ev == "point-move":
        if area.events[ ev ][i]["kwds"]["out"] and isInside( area ): 
            return False
        elif not area.events[ ev ][i]["kwds"]["out"] and not isInside( area ): 
            return False
        return True
    elif ev == "top-left-corner":
        if mapper.pointer[0] in xrange( area.xInit, area.xInit + 2) \
                and mapper.pointer[1] in xrange( area.yInit, area.yInit + 2):
            return True
        return False

    elif ev == "top-right-corner":
        if mapper.pointer[0] in xrange( area.xInit + area.width - 2, area.xInit + area.width) \
                and mapper.pointer[1] in xrange( area.yInit, area.yInit + 2):
            return True
        return False
    
    elif ev == "bottom-left-corner":
        if mapper.pointer[0] in xrange( area.xInit + area.width - 2, area.xInit + area.width) \
                and mapper.pointer[1] in xrange( area.yInit + area.height - 2, area.yInit + area.height):
            return True
        return False
    
    elif ev == "bottom-right-corner":
	if mapper.pointer[0] in xrange( area.xInit, area.xInit + 2) \
                and mapper.pointer[1] in xrange( area.yInit + area.height - 2, area.yInit + area.height ):
            return True
        return False

def isInside( area ):
    """
    Checks if the mapper point is inside the requested area.

    Arguments:
    - area: The requested area to check.
    """
    if mapper.pointer[0] in xrange( area.xInit, area.xEnd ) and  mapper.pointer[1] in xrange( area.yInit, area.yEnd):
        return True
    return False

def hasMapperEvent( eventName ):
    """
    Let us know if an event with the name 'eventName' has been registered.
    
    Arguments:
    - eventName: The name of the event to check. 
    
    Returns True if exists else False
    """
    
    if mapperEvents.has_key( eventName ):
        return True
    return False
    
def startMapperListener( mapperObj ):
    """
    Starts the MapperListener creating a new timeout object that
    will check whether an event is produced or not.
    
    Arguments:
    - mouseTrapObj: The mouseTrap object. This allow us to access important info.
    - mapperObj: The mapper object. This allow us to access the mapper info.
    """
    
    global mapper
    global conditions
    
    mapper = mapperObj
    
    conditions = { "moveMode"        : "mouseTrap.settings.mouseMode",
                   "clickDlgVisible" : "mouseTrap.modules['gui'].clickDialog.props.visible"}
    
    try:
        gobject.timeout_add( 40, checkEvents )
    except:
        debug.exception( "events", _( "The events module load failed" ) )
        
    
def stopMapperListener():
    """
    This will stop the Mapper Event Listener changing the value
    of the RUN global variable to False.
    """
    
    global RUN
    
    RUN = False
    debug.debug("events", "Event's handler has been stoped" )
