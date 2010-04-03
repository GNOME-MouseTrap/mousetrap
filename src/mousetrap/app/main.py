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


"""MouseTrap's main script."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

####################### TAKEN FROM ORCA'S CODE ###################
# We're going to force the name of the app to "mousetrap" so pygtk
# will end up showing us as "mousetrap" to the AT-SPI.  If we don't
# do this, the name can end up being "-c".  See Orca's bug 364452 at
# http://bugzilla.gnome.org/show_bug.cgi?id=364452 for more
# information.
import sys
sys.argv[0] = "mousetrap"

import gobject
import debug
import getopt
import environment as env

from mousetrap.ocvfw import pocv

from ui.i18n import _
from ui.main import MainGui
from ui.scripts import get_script_class

from lib import httpd, dbusd, settings

class Controller():
    """
    MouseTrap's Controller Class
    """

    def __init__(self):
        """
        The MouseTrap controller init class

        Arguments:
        - self: The main object pointer.
        """

        # We don't want to load the settings each time we need them. do we?
        self.cfg = None

        self.loop = gobject.MainLoop()
        self.httpd = httpd.HttpdServer(20433)
        self.dbusd = dbusd.DbusServer()


    def start(self):
        """
        Starts the modules, views classes.

        Arguments:
        - self: The main object pointer.
        """

        if self.cfg is None:
            conf_created, self.cfg = settings.load()

        self.proc_args()

        if not self.dbusd.start():
            self.httpd.start()

        if self.cfg.getboolean("main", "startCam"):
            # Lets start the module
            idm = pocv.get_idm(self.cfg.get("main", "algorithm"))
            self.idm = idm.Module(self)
            self.idm.set_capture(self.cfg.getint("cam", "inputDevIndex"))

            gobject.timeout_add(150, self.update_frame)
            gobject.timeout_add(50, self.update_pointers)
            
            debug.info("mousetrap", "Idm loaded and started")

        # Lets build the interface
        self.itf = MainGui(self)
        self.itf.build_interface()
        self.itf.load_addons()
        
        if conf_created:
            from ui import settings_gui
            settings_gui.showPreffGui(self)
            
        debug.info("mousetrap", "MouseTrap's Interface Built and Loaded")

        gobject.threads_init()
        self.loop.run()

    def proc_args(self):
        """
        Process the startup flags

        Arguments:
        - self: The main object pointer.
        """
   
        arguments = sys.argv[1:]
        if len(arguments) == 1:
            arguments = arguments[0].split()

        env.flags = dict((key[0], {"section" : sec}) for sec in self.cfg.sections() 
                                                    for key in self.cfg.items(sec))

        try:
            # ? for help
            # e for enable
            # d for disable
            # t for mouse tiemout
            opts, args = getopt.getopt(
                arguments,
                "?hve:d:s:",
                ["help",
                 "version",
                 "enable=",
                 "disable=",
                 "set="])

            for opt, val in opts:
               
                key = False

                # This will change the default video device input
                if opt in ("-s", "--set"):
                    key, value = val.strip().split("-")
                    
                if opt in ("-e", "--enable"):
                    key, value = [val.strip(), "True"]

                if opt in ("-d", "--disable"):
                    key, value = [val.strip(), "False"]

                if key in env.flags:
                    self.cfg.set(env.flags[key]["section"], key, value)
                elif key:
                    self.usage()
                    self.quit(2)
                         
                if opt in ("-v", "--version"):
                    print(env.version)
                    self.quit(0)
                    
                # This will show the usage of mouseTrap
                if opt in ("-?", "-h", "--help"):
                    self.usage()
                    self.quit(0)
                    
        except getopt.GetoptError, err:
            print str(err)
            self.usage()
            self.quit(2)
            pass

    def usage(self):
        """
        Prints the usage

        Arguments:
        - self: The main object pointer
        """

        print( _("Usage: mouseTrap [OPTION...]"))
    
        # '-?, --help' that is used to display usage information.
        #
        print( "-?, -h, --help              " + \
                _("        Show this help message"))
                
        
        # Option:
        # '-i' that is used to set the input camera index. E.g: -i 0
        print( "-s, --set            " + \
                _("              Sets new value to Non Boolean options E.g -s inputDevIndex-1"))
    
        # Options:
        # -e, --enable Allow the users to enable modules not permantly
        print( "-e, --enable=[" \
            + "main-window" + "|" \
            + "cam") + "]",
        
        print( _("     Enable the selected options"))
        
        # Options:
        # -d, --disable Allow the users to disable modules not permanently.
        print( "-d, --disable=[" \
            + "main-window" + "|" \
            + "cam" + "]"),
            
        print( _("    Disable the selected options"))
        
        # Options:
        # -t --timeout To change the mouse timeout not permanently.
        print( "-v, --version      " + \
                _("                 Shows mouseTrap version"))
        
        print( _("\nReport bugs to flaper87@flaper87.org"))
    
    def script(self):
        """
        Returns the main script class object.

        Arguments:
        - self: The main object pointer.
        """
        return get_script_class(self.cfg.get("scripts", "name"))()

    def update_frame(self):
        """
        Updates the User Interface frame with the latest capture.

        Arguments:
        - self: The main object pointer.
        """
        self.itf.update_frame(self.idm.get_capture(), self.idm.get_pointer())
        return True

    def update_pointers(self):
        """
        Gets the new mouse pointer position based on the las calcs.

        Arguments:
        - self: The main object pointer.
        """
        self.itf.script.update_items(self.idm.get_pointer())
        return True

    def quit(self, exitcode=1):  
        """
        Quits mouseTrap and all its process
        
        Arguments:
        - self: The main object pointer.
        - exitcode: The exitcode number. It helps to handle some quit events.
        """
        sys.exit(exitcode)
