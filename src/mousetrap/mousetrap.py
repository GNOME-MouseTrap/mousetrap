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


"""MouseTrap's main script."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import gtk
import gobject
import lib.mouse as mouse
#import ocvfw.idm as idm
from ocvfw import pocv
from ui.scripts.screen import ScriptClass
from ui.main import MainGui, CoordsGui

class Controller():

    def __init__(self):
        """
        The MouseTrap controller init class

        Arguments:
        - self: The main object pointer.
        """
        print("Start")

    def start(self):
        """
        Starts the modules, views classes.

        Arguments:
        - self: The main object pointer.
        """

        # Lets start the module
        #idm = __import__("ocvfw.idm.forehead", globals(), locals(), [''])
        #self.idm = idm.Module(self)
        #self.idm.set_capture()

        idm = pocv.get_idm("forehead")
        self.idm = idm.Module(self)
        self.idm.set_capture()

        # Lets build the interface
        self.itf = MainGui(self)
        self.itf.build_interface()

    def script(self):
        """
        Returns the main script class object.

        Arguments:
        - self: The main object pointer.
        """
        return ScriptClass()

    def update_frame(self):
        self.itf.update_frame(self.idm.get_image(), self.idm.get_pointer())
        return True

    def update_pointers(self):
        self.itf.script.update_items(self.idm.get_pointer())
        return True



## This is momentary
loop = gobject.MainLoop()
a = Controller()
a.start()
gobject.timeout_add(150, a.update_frame)
#gobject.timeout_add(50, a.update_pointers)
gobject.threads_init()
loop.run()
