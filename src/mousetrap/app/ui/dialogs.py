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

""" A group of formated dialogs functions used by mousetrap. """

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

from gi.repository import Gtk
from mousetrap.app.ui.i18n import _


def addLabelMessage( dialog, message ):
    """
    Adds a label to the dialog

    Arguments:
    - dialog: The dialog object pointer.
    - message: The dialog message
    """

    label = Gtk.Label()
    label.set_use_markup(True)
    label.set_markup('<span>' + \
        message + "</span>")
    label.show()
    dialog.hbox.pack_start(label, True, True, 0)

def addImage( dialog, stockImage, stock=False):
    """
    Adds an image to a dialog.

    Arguments:
    - dialog: The dialog object pointer.
    - stockImage: The image to set.
    - stock. is it a stock image? False if it isn't.
    """

    image = Gtk.Image()
    if stock:
        image.set_from_stock( stockImage, Gtk.IconSize.DIALOG )
    else:
        pass
    image.set_alignment( 0.0, 0.5 )
    image.show()
    dialog.hbox.pack_start(image, True, True, 0)

def confirmDialog( message, parent ):
    """
    Creates a confirmation dialog.

    Arguments:
    - message: The dialog message
    - parent: The parent window. None if there's not one.
    """

    dialog = createDialog( _( "Confirmation Dialog" ), parent,
                            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, \
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT, \
                            Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
    addImage( dialog, Gtk.STOCK_DIALOG_WARNING, True)
    addLabelMessage( dialog, message )
    return dialog.run()

def errorDialog( message, parent ):
    """
    Creates an error dialog using the messageDialog function.

    Arguments:
    - message: The dialog message
    - parent: The parent window. None if there's not one.
    """
    return messageDialog( _("Error Dialog"), message, parent,  Gtk.STOCK_DIALOG_ERROR )

def warningDialog( message, parent ):
    """
    Creates a warning dialog using the messageDialog function.

    Arguments:
    - message: The dialog message
    - parent: The parent window. None if there's not one.
    """
    return messageDialog( _("Information Dialog"), message, parent,  Gtk.STOCK_DIALOG_WARNING )

def informationDialog( message, parent ):
    """
    Creates an information dialog using the messageDialog function.

    Arguments:
    - message: The dialog message
    - parent: The parent window. None if there's not one.
    """
    return messageDialog( _("Information Dialog"), message, parent,  Gtk.STOCK_DIALOG_INFO )

def messageDialog( title, message, parent, stockImage, stock = True ):
    """
    Creates a simple message dialog. E.g: Error, Warnings, Informations.

    Arguments:
    - title: The dialog title.
    - message: The dialog message.
    - parent: The parent Window, None if there's not one.
    - stockImage: The image to show.
    - stock: If the image is a stock image.
    """
    dialog = createDialog( title, parent, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, \
                            (Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))

    addImage( dialog, stockImage, stock)
    addLabelMessage( dialog, message )
    return dialog.run()

def closeDialog( dialog, *args ):
    """
    Close Function for dialogs.

    Arguments:
    - dialog: the dialog to destroy.
    - *args: The widget event arguments.
    """
    dialog.destroy()

def createDialog( title, parent, flags, buttons ):
    """
    Creates a Dialog Window.

    Arguments:
    - self: The main object pointer.
    - title: The Dialog window Title
    - parent: The parent window.
    - message: A message to show in the dialog.
    - stockImage: A GTK+ stock image.
    - flags: gtk.Dialog Flags to set the typo of dialog. E.g: gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
    - buttons: A tuple with the gtk.Buttons to show. E.g: ( gtk.STOCK_OK, gtk.STOCK_CANCEL )
    """

    dialog = Gtk.Dialog( title, parent, flags, buttons )

    dialog.set_default_size(150, 100)
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.set_border_width(8)
    dialog.vbox.set_spacing ( 4 )

    hbox = Gtk.HBox(spacing=4)

    dialog.vbox.pack_start(hbox, True, True, 0)

    setattr(dialog, 'hbox', hbox)

    dialog.connect('delete-event', closeDialog, dialog)

    dialog.show_all()

    return dialog

class IdmSettings(Gtk.Window):

    def __init__(self, cfg, name, stgs):
        """
        Idm Settings window.

        Arguments:
        self: The main object pointer.
        cfg: The config object.
        stgs: The idm's settings dict to parse.
        """
        super(IdmSettings, self).__init__()

        self.cfg = cfg
        self.idm_stgs = eval(stgs)
        self.idm = name.lower()
        self.tmp = {}

        self.set_title(_("%s Config's Dialog" % self.idm.capitalize()))

        self.main_vbox = Gtk.VBox(spacing=6)
        self.add_widgets()

        buttons_box = Gtk.HBox(spacing=6)

        button = Gtk.Button( _("Accept"), stock=Gtk.STOCK_OK )

        button.connect("clicked", self.accept_button)
        buttons_box.pack_start(button, False, False, 0)

        button = Gtk.Button( _("Cancel"), stock=Gtk.STOCK_CANCEL )

        button.connect("clicked", self.cancel_button)
        buttons_box.pack_start(button, False, False, 0)

        buttons_box.show_all()

        self.main_vbox.pack_start(buttons_box, False, False, 0)

        self.main_vbox.show_all()
        self.show_all()
        self.add(self.main_vbox)

        if not self.cfg.has_section(self.idm):
            self.cfg.add_section(self.idm)

    def accept_button(self, widget, *args):
        for key in self.tmp:
            self.cfg.set(self.idm, key, self.tmp[key])

        self.destroy()

    def cancel_button(self, widget, *args):
        self.destroy()

    def add_widgets(self):
        """
        Adds dinamicaly the widgets to the dialog.

        Arguments:
        - self: The main object pointer.
        """
        for key in self.idm_stgs:
            self.main_vbox.pack_start(self.create_labled_input(key, True, True, 0), False, False, 0)

    def value_changed(self, widget, key):
        self.tmp[key] = widget.get_text()

    def create_labled_input(self, key):
        """
        Creates a textbox with a lable.

        Arguments:
        - self: The main object pointer.
        - key: The parent key.
        """
        hbox = Gtk.HBox()
        label = Gtk.Label(_(key.capitalize()))

        label.set_use_underline( True )
        label.show()

        hbox.pack_start(label, True, True, 0)

        val = str(self.idm_stgs[key]["value"])

        if self.cfg.get(self.idm, key):
            val = self.cfg.get(self.idm, key)

        entry = Gtk.Entry()

        entry.set_text(val)
        entry.connect("changed", self.value_changed, key)
        entry.show()
        hbox.pack_start(entry, True, True, 0)
        hbox.show_all()

        return hbox


class CairoTransGui( Gtk.Window ):

    def __init__( self, message ):
        super(CairoTransGui, self).__init__()

        self.set_property("skip-taskbar-hint", True)
        self.connect("expose-event", self.expose)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.clicked)
        self.set_size_request( 700 , 100)

        self.set_title('MouseTrap Message!!!')

        self.set_app_paintable(True)
        self.set_decorated(False)

        self.message = message

        self.show_all()

    def expose( self, widget, event):
        cr = widget.window.cairo_create()

        cr.set_operator(1)
        cr.paint()

        cr.set_source_rgba (255.0, 255.0, 255.0, 100.0)
        cr.set_font_size (50)
        cr.move_to (0, 70)
        cr.show_text (self.message)
        cr.fill()
        cr.stroke()
        return False

    def clicked(self, widget, event):
        #If a shift key is pressed, start resizing
        self.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)

