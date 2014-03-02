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

import os
from gi.repository import Gtk
import mousetrap.app.debug as debug
import mousetrap.app.environment as env

from subprocess import Popen, PIPE
from mousetrap.app.ui.i18n import _
from mousetrap.app.addons.handler import AddonsBase

a_name = "Recalc"
a_description = "Adds a button to recalc the forehead"
a_settings = {}

class Addon(AddonsBase):

    def __init__(self, controller):
        AddonsBase.__init__(self, controller)

        if self.cfg.getboolean("main", "startCam") and \
                self.cfg.get("main", "algorithm") == "forehead":
            self.button = Gtk.Button(_("Recalc Point"))
            self.button.connect("clicked", self.recalc)
            self.button.show()
            self.add_item(self.button)
            debug.debug("addon.recalc", "Recalc Addon started")

    def recalc(self, *args):
        """
        Unsets the forehead attribute to force
        the point recalc.

        Arguments:
        - self: The main object pointer.
        - args: The callback args.
        """
        if hasattr(self.ctr.idm.cap, "forehead"):
            delattr(self.ctr.idm.cap, "forehead")
