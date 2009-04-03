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


"""Settings Handler Interface."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import gtk
import sys
from i18n import _
import environment as env
from ocvfw import pocv

class preffGui( gtk.Window ):
    """
    The Class for the preferences GUI.

    Arguments:
    - gtk.Window: The gtk.Window Object.
    """

    def __init__(self, controller):
        """
        The Class Constructor.

        Arguments:
        - self: The main object pointer.
        - mouseTrap: The mouseTrap object pointer.
        """

        gtk.Window.__init__( self )

        self.ctr = controller
        self.cfg = self.ctr.cfg
        self.preffWidgets = dict()

    def _SetWindowsIcon( self ):
        """
        Sets the icon for the preffGUI.

        Arguments:
        - self: The main object pointer.
        """

        icon_theme = gtk.icon_theme_get_default()
        try:
            icon = icon_theme.load_icon("mouseTrap", 48, 0)
        except:
            return

        gtk.window_set_default_icon(icon)

    def _buildInterface( self ):
        """
        Builds the preffGUI.

        Arguments:
        - self: The main object pointer.
        """

        accelGroup = gtk.AccelGroup()
        self.add_accel_group( accelGroup )

        accelGroup = accelGroup

        self.set_title( _("mouseTrap Preferences") )
        self.set_size_request( 600 , 400)
        self.connect( "destroy", self.close)

        self.Table = gtk.Table( 3, 6, False )

        self.NoteBook = gtk.Notebook()
        self.NoteBook.set_tab_pos( gtk.POS_TOP )
        self.Table.attach( self.NoteBook, 0, 6, 0, 1 )
        self.NoteBook.show()

        self.main_gui_tab()
        self.cam_tab()
        self.algorithm_tab()
        #self.mouseTab()
        self.debug_tab()

        ####################
        # Bottom's buttons #
        ####################
        self.ButtonsBox = gtk.HBox( False, spacing=6 )

        self.AcceptButton = gtk.Button( _("Accept"), stock=gtk.STOCK_OK)
        self.AcceptButton.connect("clicked", self.acceptButtonClick )
        self.ButtonsBox.pack_end( self.AcceptButton )

        CancelButton = gtk.Button( _("Accept"), stock=gtk.STOCK_CANCEL )
        CancelButton.connect("clicked", self.close )
        self.ButtonsBox.pack_end( CancelButton)

        self.ApplyButton = gtk.Button( _("Accept"), stock=gtk.STOCK_APPLY )
        self.ApplyButton.connect( "clicked", self.applyButtonClick )
        self.ButtonsBox.pack_end( self.ApplyButton )

        self.ButtonsBox.show_all()

        self.Table.attach(self.ButtonsBox, 1, 2, 2, 3, 'fill', False)
        self.Table.show()
        self.add( self.Table )
        self.show()

    def main_gui_tab( self ):
        """
        The mainGui Preff Tab.

        Arguments:
        - self: The main object pointer.
        """

        Frame = gtk.Frame()

        mainGuiBox = gtk.VBox( spacing = 6 )

        mWindowActive = gtk.CheckButton( _("Show main window") )
        mWindowActive.set_active( self.cfg.getboolean( "gui", "showMainGui" ) )
        mWindowActive.connect( "toggled", self._checkToggled, "gui", "showMainGui" )

        mainGuiBox.pack_start( mWindowActive, False, False )

        mainGuiBox.show_all()

        Frame.add( mainGuiBox )
        Frame.show()

        self.NoteBook.insert_page(Frame, gtk.Label( _("General") ) )

    def cam_tab( self ):
        """
        The cam module Preff Tab.

        Arguments:
        - self: The main object pointer.
        """

        Frame = gtk.Frame()

        camBox = gtk.VBox( spacing = 6 )

        cAmActive = gtk.CheckButton( _("Activate Camera module") )
        cAmActive.set_active( self.cfg.getboolean( "main", "startCam" ) )
        cAmActive.connect( "toggled", self._checkToggled, "main", "startCam" )

        camBox.pack_start( cAmActive, False, False )

        flipImage = gtk.CheckButton( _("Flip Image") )
        flipImage.set_active( self.cfg.getboolean( "cam",  "flipImage" ) )
        flipImage.connect( "toggled", self._checkToggled, "cam", "flipImage" )

        camBox.pack_start( flipImage, False, False )

        mapperActive = gtk.CheckButton( _("Show Point Mapper") )
        mapperActive.set_active( self.cfg.getboolean( "gui", "showPointMapper" ) )
        mapperActive.connect( "toggled", self._checkToggled, "gui", "showPointMapper" )

        camBox.pack_start( mapperActive, False, False )

        showCapture = gtk.CheckButton( _("Show Capture") )
        showCapture.set_active( self.cfg.getboolean( "gui", "showCapture" ) )
        showCapture.connect( "toggled", self._checkToggled, "gui", "showCapture" )

        camBox.pack_start( showCapture, False, False )

        inputDevIndex = self.addSpin( _("Input Video Device Index: "), "inputDevIndex", self.cfg.getint( "cam", "inputDevIndex" ), "cam", "inputDevIndex", 0)
        camBox.pack_start( inputDevIndex, False, False )

        camBox.show_all()

        Frame.add( camBox )
        Frame.show()

        self.NoteBook.insert_page(Frame, gtk.Label( _("Camera") ) )

    def algorithm_tab( self ):
        """
        The cam module Preff Tab.

        Arguments:
        - self: The main object pointer.
        """

        Frame = gtk.Frame()

        algo_box = gtk.VBox( spacing = 6 )

        liststore = gtk.ListStore(bool, str, bool)

        conf_button = gtk.Button(stock=gtk.STOCK_PREFERENCES)
        conf_button.set_sensitive(False)

        tree_view = gtk.TreeView(liststore)
        tree_view.connect("cursor-changed", self._tree_view_click, conf_button)

        toggle_cell = gtk.CellRendererToggle()
        toggle_cell.set_radio(True)
        toggle_cell.connect( 'toggled', self._toggle_cell_changed, liststore)
        toggle_cell.set_property('activatable', True)
        #toggle_cell.set_property('background-set' , True)

        text_cell = gtk.CellRendererText()

        toggle_column = gtk.TreeViewColumn(_('Active Algorithms'), toggle_cell)
        text_column = gtk.TreeViewColumn(_('Installed Algorithms'))

        for alg in pocv.get_idms_list():
            alg_inf = pocv.get_idm_inf(alg)
            liststore.append([False, "%s: %s" % (alg_inf["name"], alg_inf["dsc"]), alg_inf["stgs"]])

        tree_view.append_column(toggle_column)
        tree_view.append_column(text_column)

        text_column.pack_start(text_cell, True)

        toggle_column.add_attribute( toggle_cell, "active", 0 )
        toggle_column.set_max_width(30)
        #toggle_column.set_attributes( toggle_cell, background=2 )
        text_column.set_attributes(text_cell, text=1)

        algo_box.pack_start(tree_view)
        algo_box.pack_start(conf_button, False, False)



        algo_box.show_all()

        Frame.add( algo_box )
        Frame.show()

        self.NoteBook.insert_page(Frame, gtk.Label( _("Algorithm") ) )

    def mouseTab( self ):
        """
        The cam module Preff Tab.

        Arguments:
        - self: The main object pointer.
        """

        Frame = gtk.Frame()

        camBox = gtk.VBox( spacing = 6 )

        reqMov = self.addSpin( _("Step Speed: "), "stepSpeed", self.cfg.getint( "mouse", "stepSpeed" ), "mouse", "stepSpeed" )
        camBox.pack_start( reqMov, False, False )

        defClickF = gtk.Frame( _( "Default Click:" ) )

        defClicks = {  "b1c"   :  _("Left Click"),
                       "b1d"   :  _("Double Click"),
                       "b1p"   :  _("Drag/Drop Click"),
                       "b3c"   :  _("Right Click")}

        defClicksInv = dict((v,k) for k,v in defClicks.iteritems())

        defClick = gtk.combo_box_new_text()
        defClick.append_text(defClicks[self.cfg.get( "mouse", "defClick" )])

        defClicklBl = gtk.Label(self.cfg.get( "mouse", "defClick" ))
        self.preffWidgets['defClick'] = defClicklBl

        for mode in defClicks:
            if mode == self.cfg.get( "mouse", "defClick" ):
                continue
            defClick.append_text( defClicks[mode] )

        defClick.connect('changed', self._comboChanged, "mouse", "defClick", defClicksInv)
        defClick.set_active(0)

        defClickF.add( defClick)
        camBox.pack_start( defClickF, False, False )


        mouseModF = gtk.Frame( _( "Select Mouse Mode:" ) )

        mouseModes = env.mouseModes

        mouseModesInv = dict((v,k) for k,v in mouseModes.iteritems())

        mouseMod = gtk.combo_box_new_text()
        mouseMod.append_text(mouseModes[self.cfg.get( "cam", "mouseMode" )])
        mouseModlBl = gtk.Label(self.cfg.get( "cam", "mouseMode" ))
        self.preffWidgets['mouseMode'] = mouseModlBl

        for mode in mouseModes:
            if mode == self.cfg.get( "cam", "mouseMode" ):
                continue
            mouseMod.append_text( mouseModes[mode] )

        mouseMod.connect('changed', self._comboChanged, "cam", "mouseMode", mouseModesInv)
        mouseMod.set_active(0)

        mouseModF.add( mouseMod)
        camBox.pack_start( mouseModF, False, False )

        camBox.show_all()

        Frame.add( camBox )
        Frame.show()

        self.NoteBook.insert_page(Frame, gtk.Label( _("Mouse") ) )

    def debug_tab( self ):
        """
        The debuging Preff Tab.

        Arguments:
        - self: The main object pointer.
        """


        Frame = gtk.Frame()

        debugBox = gtk.VBox( spacing = 6 )

        levelHbox = gtk.HBox( spacing = 4 )

        levellabel = gtk.Label( _("Debugging Level:") )
        levellabel.set_alignment( 0.0, 0.5 )
        levellabel.show()
        levelHbox.pack_start( levellabel, False, False )

        adj = gtk.Adjustment( self.cfg.getint( "main", "debugLevel" ), 10, 50, 10, 1, 0)
        levelSpin = gtk.SpinButton( adj, 0.0, 0 )
        levelSpin.set_wrap( True )
        levelHbox.pack_start( levelSpin, False, False )
        levelSpin.connect( "value-changed", self._spinChanged, "main", "debugLevel" )

        debugBox.pack_start( levelHbox, False, False )

        debugBox.show_all()

        Frame.add( debugBox )
        Frame.show()

        self.NoteBook.insert_page(Frame, gtk.Label( _("Debug") ) )


    def acceptButtonClick( self, *args ):
        """
        Acept button callback. This will apply the settings and close the
        preferences GUI.

        Arguments:
        - self: The main object pointer.
        - *args: The button event arguments
        """

        self.cfg.write( open( env.configPath + "userSettings.cfg", "w" ) )
        self.destroy()


    def _tree_view_click(self, widget, conf_button):
        """
        Row Selection Event.

        Enables/Disables the conf_button whether the
        selected algorithm can be configured or not.

        Arguments:
        - widget: The gtk Widget
        - conf_button: The configuration button object.
        """

        ts = widget.get_selection()
        model, it = ts.get_selected()
        path = model.get_path(it)[0]
        conf_button.set_sensitive(model[path][2])

    def _toggle_cell_changed(self, cell, path, model ):
        """
        ListStore RadioButton Value Changer.
        """

        if model[path][0]:
            return False

        for pth in range(len(model)):
            pth = str(pth)
            if pth == path:
                model[pth][0] = True
            else:
                model[pth][0] = False


    def _checkToggled( self, widget, section, option ):
        """
        Sets the new value in the settings object for the toggled checkbox

        Arguments:
        - self: The main object pointer.
        - widget: The checkbox.
        - section: The section of the settings object.
        - option: The option in the section.
        """
        self.cfg.set( section, option, str(widget.get_active()))

    def _spinChanged( self, widget, section, option ):
        """
        Sets the new value in the settings object for the toggled checkbox

        Arguments:
        - self: The main object pointer.
        - widget: The checkbox.
        - section: The section of the settings object.
        - option: The option in the section.
        """
        self.cfg.set( section, option, str(widget.get_value_as_int()))


    def applyButtonClick( self, *args):
        """
        Apply button callback. This will apply the settings.

        Arguments:
        - self: The main object pointer.
        - *args: The button event arguments
        """
        self.cfg.write( open( env.configPath + 'userSettings.cfg', "w" ) )

    def _comboChanged( self, widget, section, option, modes ):
        """
        On combo change. This function is the callback for the on_change
        event.

        This helps to keep the combobox settings variable updated with the
        selected option.

        Arguments:
        - self: The main object pointer.
        - widget: The widget pointer.
        - section: The section of the settings object.
        - option: The option in the section.
        - modes: The new value.
        """

        model = widget.get_model()
        index = widget.get_active()
        self.cfg.set( section, option, modes[model[index][0]] )

    def addSpin( self, label, var, startValue, section, option, min = 1, max = 15):
        """
        Creates a new spin button inside a HBox and return it.

        Arguments:
        - self: The main object pointer.
        - label: The spin button label.
        - var: The prefferences dict variable.
        - startValue: The start value.
        """

        spinHbox = gtk.HBox( spacing = 4 )

        spinLbl = gtk.Label( label )
        spinLbl.set_alignment( 0.0, 0.5 )
        spinLbl.show()
        spinHbox.pack_start( spinLbl, False, False )

        adj = gtk.Adjustment( startValue, min, max, 1, 1, 0)
        spinButton = gtk.SpinButton( adj, 0.0, 0 )
        spinButton.set_wrap( True )
        spinButton.connect( "value-changed", self._spinChanged, section, option )
        spinHbox.pack_start( spinButton, False, False )

        spinLbl.set_mnemonic_widget( spinButton )

        return spinHbox

    def close( self, *args ):
        """
        Closes the prefferences GUI without saving the changes.

        Arguments:
        - self: The main object pointer.
        - *args: The button event arguments
        """
        self.destroy()


def showPreffGui(controller):
    """
    Starts the preffGui.

    Arguments:
    - mouseTrap: The mouseTrap object pointer.
    """

    GUI = preffGui(controller)
    GUI._SetWindowsIcon()
    GUI._buildInterface()
