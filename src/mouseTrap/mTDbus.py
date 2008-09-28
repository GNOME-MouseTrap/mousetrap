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



""" Exposes mouseTrap as a DBus service for comunication purposes. """

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import dbus
import debug
import mouseTrap
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

dbusserver = None
main_loop = DBusGMainLoop()
bus = dbus.SessionBus(mainloop=main_loop)

DBUS_NAME = "org.gnome.mouseTrap"
DBUS_PATH = "/org/gnome/mouseTrap"

class mTDbusServer(dbus.service.Object):
    """DBus service"""
    
    def __init__( self ):
        """
        Initialize the dbus server module.
        
        Arguments:
        - lself: The main object pointer
        - mouseTrap: The mouseTrap onject pointer
        """
        
        global bus
        bus_name = dbus.service.BusName(DBUS_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, DBUS_PATH)
        
    @dbus.service.method(DBUS_NAME)
    def move(self, action):
        """
        Just Move the mouse to de required position.
        """
        X, Y = action.split(",")
        mouseTrap.move( "click", X, Y )

def start():
    """
    Start's the dbus server and store it in the global variable
    dbusserver, so it won't be started twice.
    """
    global dbusserver
    
    if dbusserver:
        return
    
    try:
        dbusserver = mTDbusServer() 
    except:
        debug.exception( "mouseTrap.mTDbus", "The dbus server load failed" )
    
    
def shutdown():
    """
    Fake shutdown
    """
    pass
