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

""" The main GUI of mousetrap. """

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import GdkPixbuf
import dialogs
import settings_gui
import mousetrap.app.debug as debug
import mousetrap.app.environment as env
from mousetrap.app.addons import cpu
import numpy

class MainGui( Gtk.Window ):
    '''
    MouseTrap's main GUI Class.
    '''

    def __init__( self, controller ):
        '''
        The main GUI constructor

        Arguments:
        - self: The main object pointer.
        - controller: The mouseTrap's controller.
        '''

        GObject.GObject.__init__( self )
        self.ctr    = controller
        self.cfg    = controller.cfg
        self.script = self.ctr.script()
        self.set_default_size(200, 400)

    def setWindowsIcon( self ):
        '''
        Sets the mainGui icon

        Arguments:
        - self: The main object pointer.
        '''

        icon_theme = Gtk.IconTheme.get_default()
        try:
            icon = icon_theme.load_icon("mousetrap", 48, 0)
        except:
            return

        self.set_default_icon(icon)

    def build_interface( self ):
        '''
        Builds the interface

        Arguments:
        - self: The main object pointer.
        '''

        self.setWindowsIcon()

        accelGroup = Gtk.AccelGroup()
        self.add_accel_group( accelGroup )

        self.accelGroup = accelGroup

        self.set_title("MouseTrap")
        self.connect("destroy", self.close)

        self.vbox = Gtk.Grid()

        self.buttonsBox = Gtk.ButtonBox()

        self.prefButton = Gtk.Button(stock=Gtk.STOCK_PREFERENCES)
        self.prefButton.connect("clicked", self._show_settings_gui)
        self.buttonsBox.add(self.prefButton)

        self.closeButton = Gtk.Button(stock=Gtk.STOCK_QUIT)
        self.closeButton.connect("clicked", self.close)
        self.buttonsBox.add(self.closeButton)

        self.helpButton = Gtk.Button(stock=Gtk.STOCK_HELP)
        self.helpButton.connect("clicked", self._loadHelp)
        self.buttonsBox.add(self.helpButton)

        self.vbox.add(self.buttonsBox)

        self.addonBox = Gtk.Grid()
        self.addonBox.show_all()
        self.vbox.attach_next_to(self.addonBox, self.buttonsBox, Gtk.PositionType.BOTTOM, 1, 1)

        self.cap_image = Gtk.Image()

        if self.cfg.getboolean("gui", "showCapture"):
            self.cap_expander = Gtk.Expander.new_with_mnemonic("_Camera Image")
            self.cap_expander.add(self.cap_image)
            self.cap_expander.set_expanded(True)
            self.vbox.attach_next_to(self.cap_expander, self.addonBox, Gtk.PositionType.BOTTOM, 1, 1)

        if self.cfg.getboolean("gui", "showPointMapper"):
            self.map_expander = Gtk.Expander.new_with_mnemonic("_Script Mapper")
            self.map_expander.add(self.script)
            self.map_expander.set_expanded(True)
            self.vbox.attach_next_to(self.map_expander, self.cap_expander, Gtk.PositionType.BOTTOM, 1, 1)

        self.statusbar = Gtk.Statusbar()
        self.statusbar_id = self.statusbar.get_context_id("statusbar")

        self.vbox.attach_next_to(self.statusbar, self.addonBox, Gtk.PositionType.BOTTOM, 1, 1)

        self.vbox.show_all()
        self.add(self.vbox)
        self.show_all()

    def load_addons(self):
        '''
        Loads the enabled addons

        Arguments:
        - self: The main object pointer.
        '''

        for add in self.cfg.getList("main", "addon"):
            tmp = __import__("mousetrap.app.addons.%s" % add, globals(), locals(),[''])

            setattr(self, add, tmp.Addon(self.ctr))

    def update_frame(self, cap, point):
        '''
        Updates the image

        Arguments:
        - self: The main object pointer.
        - img: The IPLimage object.
        '''
        if not numpy.any(cap.image()):
            return False

        #sets new pixbuf
        self.cap_image.set_from_pixbuf(cap.to_gtk_buff().scale_simple(200, 160, GdkPixbuf.InterpType.BILINEAR))

#    def recalPoint(self, widget, flip = ''):
#        '''
#        Enables the Flip of the Image in the X axis
#
#        This is for webcams that capture images as a mirror.
#
#        Arguments:
#        - selfL The main object pointer.
#        - *args: Widget related arguments.
#        '''
#
#        if flip:
#            self.settings.set( "cam", "flipImage", str(not self.settings.getboolean("cam", "flipImage")) )
#
#        mouseTrap.calcPoint()

    def _newStockImageBurron(self, label, stock):
        '''
        Creates an image button from gtk's stock.

        Arguments:
        - self: The main object pointer.
        - label: The button's label.
        - stock: The Stock image the button will use. E.g. Gtk.STOCK_GO-FORWARD.

        Returns buttonLabelBox - A Gtk.Grid that contains the new image stock button.
        '''

        buttonLabelBox = Gtk.Grid()

        im = Gtk.Image.new_from_stock( stock, Gtk.IconSize.BUTTON )

        label = Gtk.Label( label = label )
        #label.set_alignment( 0.0, 0.5 )
        label.set_use_underline( True )

        buttonLabelBox.add( im )
        buttonLabelBox.attach_next_to( label, im, Gtk.PositionType.BOTTOM, 1, 1 )
        buttonLabelBox.show_all()
        return buttonLabelBox

    def _show_settings_gui(self, *args):
        '''
        Starts the preferences GUI

        Arguments:
        - self: The main object pointer.
        - *args: The widget callback arguments.
        '''

        settings_gui.showPreffGui(self.ctr)

    def _loadHelp(self, *args):
        '''
        Shows the user manual.

        Arguments:
        - self: The main object pointer.
        - *args: The widget callback arguments.
        '''

        uri = "ghelp:%s/docs/mousetrap.xml" % env.mTDataDir
        try:
            Gtk.show_uri(Gdk.Screen.get_default(), uri, Gtk.get_current_event_time())
        except:
            debug.exception( "mainGui", "The help load failed" )

    def close(self, *args):
        '''
        Close function for the quit button. This will kill mouseTrap.

        Arguments:
        - self: The main object pointer.
        - *args: The widget callback arguments.
        '''
        self.ctr.quit(0)

def showMainGui( ):
    '''
    Loads the mainGUI components and launches it.

    Arguments:
    - mouseTrap: The mouseTrap object pointer.
    '''

    gui = MianGui()
    gui.build_interface()
    return gui
