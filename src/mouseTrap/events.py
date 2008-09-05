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
#from mouseTrap import settings


# The Locker for the event listener
RUN = True

# The Mapper to check
mapper = None

# A dictionary for the events registered
mapperEvents = dict()

# A dictionary for the conditions that can exist.
conditions = dict()
    
def hasMapperEvent( eventName ):
    """
    Let us know if an event with the name "eventName" has been registered.
    
    Arguments:
    - eventName: The name of the event to check. 
    
    Returns True if exists else False
    """
    
    if mapperEvents.has_key( eventName ):
        return True
    return False
    
def registerMapperEvent( eventName, initCoords, endCoords, inside, eventCond, eventAction, timeout, *args, **kw):
    """
    This function register new events for the Mapper that are going 
    to be executed if the mapper pointer is located inseide the range area
    created by the initCoords and the endCoords selected.
    
    Arguments:
    - eventName:  The name of the event to register. 
    - initCoords:  The initial coordinates where the event can be recognized. 
    - endCoords:   The final coordinates where the event can be recognized. 
    - inside:      True if the pointer has to be inside the selected area.
    - eventCond:   The conditions that should exist to executed the event.
    - eventAction: The callback function.
    - timeout:     The callback function timeout.
    - *args:       The areguments that are going to be passed to the callback.
    """
    
    #if mapperEvents.has_key( eventName ):
     #   debug.log( debug.MODULES, _( "Warning" ) )
      #  sys.stderr.write( "\nThe event name %s is already in use\n" % eventName )

    mapperEvents[eventName] = { "eventCond"   : eventCond,
                                "function"    : eventAction,
                                "initCoords"  : initCoords,
                                "endCoords"   : endCoords,
                                "inside"      : inside,
                                "timeout"     : timeout,
                                "last"        : time.time(),
                                "args"        : args,
                                "kw"          : kw
                              }

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
        gobject.timeout_add( 10, _checkMapperEvents )
    except:
        debug.exception( "mouseTrap.events", _( "The events module load failed" ) )
        
    
def _checkMapperEvents():
    """
    Checks if an event is being executed and calls the callback function if
    the conditions supplied are right.
    """

    for event,prop in mapperEvents.iteritems():
        _controlEvent( event, prop )
    return RUN

def _controlEvent( event, prop ):
    """
    Executes the control for each event registered.
    
    Arguments:
    - event: The event to check
    - prop: The event properties.
    """

    if mapper.pointer[0] in xrange( prop["initCoords"][0], prop["endCoords"][0]) and \
            mapper.pointer[1] in xrange( prop["initCoords"][1], prop["endCoords"][1]) and prop["inside"]:
        for cond in prop["eventCond"]:
            if not cond.split(":")[1] in str(eval(conditions[cond.split(":")[0]])):
                return False
        if not time.time() - prop["last"] >= prop["timeout"]:
            return False
        prop["function"]( *prop["args"], **prop["kw"] )
        prop["last"] = time.time()
    elif ( mapper.pointer[0] not in xrange( prop["initCoords"][0], prop["endCoords"][0]) or \
         mapper.pointer[1] not in xrange( prop["initCoords"][1], prop["endCoords"][1])) and not prop["inside"]:
        for cond in prop["eventCond"]:
            if not cond.split(":")[1] in str(eval(conditions[cond.split(":")[0]])):
                return False
        if not time.time() - prop["last"] >= prop["timeout"]:
            return False
        prop["function"]( *prop["args"], **prop["kw"] )
        prop["last"] = time.time()
    
    return True

def stopMapperListener():
    """
    This will stop the Mapper Event Listener changing the value
    of the RUN global variable to False.
    """
    
    global RUN
    
    RUN = False
