
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


"""Settings Handler Interface."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

from gi.repository import GObject
from gi.repository import Gtk
import dialogs
from i18n import _
from mousetrap.ocvfw import pocv
import mousetrap.app.environment as env

from mousetrap.app.ui.scripts import get_scripts_list
from mousetrap.app.addons.handler import AddonsHandler

class PreffGui( Gtk.Window ):
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

        GObject.GObject.__init__( self )

        self.ctr = controller
        self.cfg = self.ctr.cfg
        self.adds = AddonsHandler(self.ctr)
        self.preffWidgets = dict()

    def setWindowsIcon( self ):
        """
        Sets the icon for the preffGUI.

        Arguments:
        - self: The main object pointer.
        """

        icon_theme = Gtk.IconTheme.get_default()
        try:
            icon = icon_theme.load_icon("mouseTrap", 48, 0)
        except:
            return

        Gtk.Window_set_default_icon(icon)

    def buildInterface( self ):
        """
        Builds the preffGUI.

        Arguments:
        - self: The main object pointer.
        """

        accelGroup = Gtk.AccelGroup()
        self.add_accel_group( accelGroup )

        accelGroup = accelGroup

        self.set_title( _("mouseTrap Preferences") )
        self.set_size_request( 300, 100)
        self.connect( "destroy", self.close)

        self.window = Gtk.Grid()

        self.noteBook = Gtk.Notebook()
        self.noteBook.set_tab_pos( Gtk.PositionType.TOP )
        self.window.add( self.noteBook )
        self.noteBook.show()

        self.main_gui_tab()
        self.cam_tab()
        self.algorithm_tab()
        self.addons_tab()
        self.mouseTab()
        self.debug_tab()

        ####################
        # Bottom's buttons #
        ####################
        self.buttonsBox = Gtk.Grid()

        self.acceptButton = Gtk.Button( _("Accept"), stock=Gtk.STOCK_OK)
        self.acceptButton.connect("clicked", self.acceptButtonClick )
        self.buttonsBox.add( self.acceptButton )

        self.cancelButton = Gtk.Button( _("Accept"), stock=Gtk.STOCK_CANCEL )
        self.cancelButton.connect("clicked", self.close )
        self.buttonsBox.add( self.cancelButton )

        self.applyButton = Gtk.Button( _("Accept"), stock=Gtk.STOCK_APPLY )
        self.applyButton.connect( "clicked", self.applyButtonClick )
        self.buttonsBox.add( self.applyButton )

        self.buttonsBox.show_all()

        self.window.attach_next_to(self.buttonsBox, self.noteBook, Gtk.PositionType.BOTTOM, 1, 1)
        self.window.show_all()
        self.add( self.window )
        self.show()

    def main_gui_tab( self ):
        """
        The mainGui Preff Tab.

        Arguments:
        - self: The main object pointer.
        """

        frame = Gtk.Frame()

        general_box = Gtk.Grid()
        general_box.set_column_spacing(6)

#     mWindowActive = Gtk.CheckButton( _("Show main window") )
#     mWindowActive.set_active( self.cfg.getboolean( "gui", "showMainGui" ) )
#     mWindowActive.connect( "toggled", self._checkToggled, "gui", "showMainGui" )
#
#     mainGuiBox.add( mWindowActive )

        cAmActive = Gtk.CheckButton( _("Activate Camera module") )
        cAmActive.set_active( self.cfg.getboolean( "main", "startCam" ) )
        cAmActive.connect( "toggled", self._checkToggled, "main", "startCam" )

        general_box.add( cAmActive )

        flipImage = Gtk.CheckButton( _("Flip Image") )
        flipImage.set_active( self.cfg.getboolean( "cam",  "flipImage" ) )
        flipImage.connect( "toggled", self._checkToggled, "cam", "flipImage" )

        general_box.attach_next_to( flipImage, cAmActive, Gtk.PositionType.BOTTOM, 1, 1 )

        inputDevIndex = self.addSpin( _("Input Video Device Index: "), "inputDevIndex",
                        self.cfg.getint( "cam", "inputDevIndex" ), "cam", "inputDevIndex", 0)
        general_box.attach_next_to( inputDevIndex, flipImage, Gtk.PositionType.BOTTOM, 1, 1 )

        general_box.show_all()

        frame.add( general_box )
        frame.show()

        self.noteBook.insert_page(frame, Gtk.Label(label= _("General")), -1)

    def cam_tab( self ):
        """
        The cam module Preff Tab.

        Arguments:
        - self: The main object pointer.
        """

        frame = Gtk.Frame()

        camBox = Gtk.Grid()
        camBox.set_column_spacing(6)

        mapperActive = Gtk.CheckButton( _("Show Point Mapper") )
        mapperActive.set_active( self.cfg.getboolean( "gui", "showPointMapper" ) )
        mapperActive.connect( "toggled", self._checkToggled, "gui", "showPointMapper" )

        camBox.add( mapperActive )

        showCapture = Gtk.CheckButton( _("Show Capture") )
        showCapture.set_active( self.cfg.getboolean( "gui", "showCapture" ) )
        showCapture.connect( "toggled", self._checkToggled, "gui", "showCapture" )

        camBox.attach_next_to( showCapture, mapperActive, Gtk.PositionType.BOTTOM, 1, 1 )

        camBox.show_all()

        frame.add( camBox )
        frame.show()

        self.noteBook.insert_page(frame, Gtk.Label(label= _("Camera")), -1)

    def algorithm_tab( self ):
        """
        The cam module Preff Tab.

         Arguments:
        - self: The main object pointer.
        """

        frame = Gtk.Frame()

        algo_box = Gtk.Grid()
        algo_box.set_column_spacing(6)

        liststore = Gtk.ListStore(bool, str, str, str)

        conf_button = Gtk.Button(stock=Gtk.STOCK_PREFERENCES)
        conf_button.connect('clicked', self.show_alg_pref, liststore)
        conf_button.set_sensitive(False)

        scripts_combo = Gtk.ComboBoxText()
        scripts_combo.append_text(self.cfg.get("scripts", "name"))

        for script in get_scripts_list():
            if script.lower() != self.cfg.get("scripts", "name"):
                scripts_combo.append_text(script)

        scripts_combo.connect('changed', self._comboChanged, "scripts", "name")
        scripts_combo.set_active(0)

        tree_view = Gtk.TreeView(liststore)
        tree_view.connect("cursor-changed", self._tree_view_click, conf_button)

        toggle_cell = Gtk.CellRendererToggle()
        toggle_cell.set_radio(True)
        toggle_cell.connect( 'toggled', self._toggle_cell_changed, liststore)
        toggle_cell.set_property('activatable', True)
        #toggle_cell.set_property('background-set' , True)

        name_cell = Gtk.CellRendererText()
        desc_cell = Gtk.CellRendererText()

        toggle_column = Gtk.TreeViewColumn(_('Active Algorithms'), toggle_cell)
        name_column = Gtk.TreeViewColumn(_('Installed Algorithms'))
        desc_column = Gtk.TreeViewColumn(_('Description'))

        for alg in pocv.get_idms_list():
            alg_inf = pocv.get_idm_inf(alg)

            if not alg_inf:
                continue

            state = False
            if alg_inf["name"].lower() in self.cfg.get("main", "algorithm").lower():
                state = True
            # FIXME: I don't know what the purpose of this liststore is,
            # but it wants strings, so let's not argue for now. ;)
            liststore.append([state, alg_inf["name"], alg_inf["dsc"], str(alg_inf["stgs"])])

            #liststore.append([False, "%s: %s" % (alg_inf["name"], alg_inf["dsc"]), alg_inf["stgs"]])

        tree_view.append_column(toggle_column)
        tree_view.append_column(name_column)
        tree_view.append_column(desc_column)

        name_column.pack_start(name_cell, True)
        desc_column.pack_start(desc_cell, True)

        toggle_column.add_attribute( toggle_cell, "active", 0 )
        toggle_column.set_max_width(30)
        #toggle_column.set_attributes( toggle_cell, background=2 )
        name_column.set_attributes(name_cell, text=1)
        desc_column.set_attributes(desc_cell, text=2)

        algo_box.add(tree_view)
        algo_box.attach_next_to(conf_button, tree_view, Gtk.PositionType.BOTTOM, 1, 1)
        algo_box.attach_next_to(scripts_combo, conf_button, Gtk.PositionType.BOTTOM, 1, 1)

        algo_box.show_all()

        frame.add( algo_box )
        frame.show()

        self.noteBook.insert_page(frame, Gtk.Label(label= _("Algorithm")), -1)

    def addons_tab( self ):
        """
        The cam module Preff Tab.

        Arguments:
        - self: The main object pointer.
        """

        frame = Gtk.Frame()

        algo_box = Gtk.Grid()
        algo_box.set_column_spacing(6)

        liststore = Gtk.ListStore(bool, str, str, str)

        conf_button = Gtk.Button(stock=Gtk.STOCK_PREFERENCES)
        conf_button.connect('clicked', self.show_alg_pref, liststore)
        conf_button.set_sensitive(False)

        tree_view = Gtk.TreeView(liststore)
        tree_view.connect("cursor-changed", self._tree_view_click, conf_button)

        toggle_cell = Gtk.CellRendererToggle()
        toggle_cell.connect( 'toggled', self._enable_disable_addon, liststore)
        toggle_cell.set_property('activatable', True)

        name_cell = Gtk.CellRendererText()
        desc_cell = Gtk.CellRendererText()

        toggle_column = Gtk.TreeViewColumn(_('Active'), toggle_cell)
        name_column = Gtk.TreeViewColumn(_('Name'))
        desc_column = Gtk.TreeViewColumn(_('Description'))

        for add in self.adds.get_addons_list():
            add_inf = self.adds.get_addon_inf(add)

            if not add_inf:
                continue

            state = False
            if add_inf["name"].lower() in self.cfg.getList("main", "addon"):
                state = True
            # FIXME: I don't know what the purpose of this liststore is,
            # but it wants strings, so let's not argue for now. ;)
            liststore.append([state, add_inf["name"], add_inf["dsc"], str(add_inf["stgs"])])

        tree_view.append_column(toggle_column)
        tree_view.append_column(name_column)
        tree_view.append_column(desc_column)

        name_column.pack_start(name_cell, True)
        desc_column.pack_start(desc_cell, True)

        toggle_column.add_attribute( toggle_cell, "active", 0 )
        toggle_column.set_max_width(30)
        #toggle_column.set_attributes( toggle_cell, background=2 )
        name_column.set_attributes(name_cell, text=1)
        desc_column.set_attributes(desc_cell, text=2)

        algo_box.add(tree_view)
        algo_box.attach_next_to(conf_button, tree_view, Gtk.PositionType.BOTTOM, 1, 1)

        algo_box.show_all()

        frame.add( algo_box )
        frame.show()

        self.noteBook.insert_page(frame, Gtk.Label(label= _("Addons")), -1)

    def mouseTab( self ):
        """
        The cam module Preff Tab.

        Arguments:
        - self: The main object pointer.
        """

        frame = Gtk.Frame()

        camBox = Gtk.Grid()
        camBox.set_column_spacing(6)

        reqMov = self.addSpin( _("Step Speed: "), "stepSpeed", self.cfg.getint( "mouse", "stepSpeed" ), "mouse", "stepSpeed" )
        camBox.add( reqMov )

    ###############################################
    #                         #
    #    THE WHEEL HAS ALREADY BEEN DISCOVERED    #
    #     SO, LETS USE MOUSETWEAK INSTEAD OF      #
    #      ADD THIS SUPPORT TO MOUSETRAP.     #
    ###############################################

#     defClickF = gtk.frame( _( "Default Click:" ) )
#
#     defClicks = {  "b1c"   :  _("Left Click"),
#            "b1d"   :  _("Double Click"),
#            "b1p"   :  _("Drag/Drop Click"),
#            "b3c"   :  _("Right Click")}
#
#     defClicksInv = dict((v,k) for k,v in defClicks.iteritems())
#
#     defClick = gtk.combo_box_new_text()
#     defClick.append_text(defClicks[self.cfg.get( "mouse", "defClick" )])
#
#     defClicklBl = gtk.Label(self.cfg.get( "mouse", "defClick" ))
#     self.preffWidgets['defClick'] = defClicklBl
#
#     for mode in defClicks:
#         if mode == self.cfg.get( "mouse", "defClick" ):
#         continue
#         defClick.append_text( defClicks[mode] )
#
#     defClick.connect('changed', self._comboChanged, "mouse", "defClick", defClicksInv)
#     defClick.set_active(0)
#
#     defClickF.add( defClick)
#     camBox.pack_start( defClickF, False, False )

        camBox.show_all()

        frame.add( camBox )
        frame.show()

        self.noteBook.insert_page(frame, Gtk.Label(label= _("Mouse")), -1)

    def debug_tab( self ):
        """
        The debuging Preff Tab.

        Arguments:
        - self: The main object pointer.
        """

        frame = Gtk.Frame()

        debugBox = Gtk.Grid()
        debugBox.set_column_spacing(6)

        levelHbox = Gtk.Grid()
        levelHbox.set_row_spacing(4)

        levellabel = Gtk.Label(label= _("Debugging Level:") )
        levellabel.set_alignment( 0.0, 0.5 )
        levellabel.show()
        levelHbox.add( levellabel )

        adj = Gtk.Adjustment( self.cfg.getint( "main", "debugLevel" ), 10, 50, 10, 1, 0)
        levelSpin = Gtk.SpinButton()
        levelSpin.set_adjustment(adj)
        levelSpin.set_wrap( True )
        levelHbox.add( levelSpin )
        levelSpin.connect( "value-changed", self._spinChanged, "main", "debugLevel" )

        debugBox.add( levelHbox )

        debugBox.show_all()

        frame.add( debugBox )
        frame.show()

        self.noteBook.insert_page(frame, Gtk.Label(label= _("Debug")), -1)

    def show_alg_pref(self, widget, liststore):
        dlg = dialogs.IdmSettings(self.cfg, self.selected_idm, self.selected_idm_stgs)
        dlg.set_transient_for(self)
        dlg.set_destroy_with_parent(True)

    def acceptButtonClick( self, *args ):
        """
        Accept button callback. This will apply the settings and close the
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
        if model[path][0] and model[path][3]:
            self.selected_idm = model[path][1]
            self.selected_idm_stgs = model[path][3]
            conf_button.set_sensitive(True)

    def _toggle_cell_changed(self, cell, path, model):
        """
        ListStore RadioButton Value Changer.
        """

        if model[path][0]:
            return False

        for pth in range(len(model)):
            pth = str(pth)
            if pth == path:
                model[pth][0] = True
                self.cfg.set("main", "algorithm", model[pth][1].lower())
            else:
                model[pth][0] = False

    def _enable_disable_addon(self, cell, path, model):
        """
        ListStore RadioButton Value Changer.
        """

        model[path][0] = not model[path][0]

        cur = self.cfg.getList("main", "addon")

        if model[path][1] in cur:
            cur.remove(model[path][1].lower())
        else:
            cur.append(model[path][1].lower())

        self.cfg.setList("main", "addon", cur)

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

    def _comboChanged( self, widget, section, option, modes=None ):
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
        val = (modes and modes[model[index][0]]) or model[index][0]
        self.cfg.set( section, option, val)

    def addSpin( self, label, var, startValue, section, option, min_ = 1, max_ = 15):
        """
        Creates a new spin button inside a HBox and return it.

        Arguments:
        - self: The main object pointer.
        - label: The spin button label.
        - var: The prefferences dict variable.
        - startValue: The start value.
        """

        spinHbox = Gtk.Grid()
        spinHbox.set_row_spacing(4)

        spinLbl = Gtk.Label(label= label )
        spinLbl.set_alignment( 0.0, 0.5 )
        spinLbl.show()
        spinHbox.add( spinLbl )

        adj = Gtk.Adjustment( startValue, min_, max_, 1, 1, 0)
        spinButton = Gtk.SpinButton()
        spinButton.set_adjustment(adj)
        spinButton.set_wrap( True )
        spinButton.connect( "value-changed", self._spinChanged, section, option )
        spinHbox.add( spinButton )

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

    gui = PreffGui(controller)
    gui.setWindowsIcon()
    gui.buildInterface()
