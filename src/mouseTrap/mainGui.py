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


"""The main GUI of mouseTrap."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import gtk
import debug
import scripts
import dialogs
import mouseTrap
import environment as env

from math   import pi
from mTi18n import _
from opencv import cv

class MainGui( gtk.Window ):
    """
    MouseTrap main GUI Class
    """

    def __init__( self ):
        """
        The main GUI constructor
        
        Arguments:
        - self: The main object pointer
        - mouseTrap: The mouseTrap object pointer.
        """
    
        gtk.Window.__init__( self )
        
        self.mTp = mouseTrap
        self.settings = mouseTrap.settings
        self.image = cv.cvCreateImage( cv.cvSize( 200, 160 ), 8, 3 )
        self.clickDialog = dialogs.ClicksDialog( self )
    
    def setWindowsIcon( self ):
        """
        Sets the mainGui icon
        
        Arguments:
        - self: The main object pointer
        """
        
        icon_theme = gtk.icon_theme_get_default()
        try:
            icon = icon_theme.load_icon("mouseTrap", 48, 0)
        except:
            return
            
        gtk.window_set_default_icon(icon)


    def buildInterface( self ):
        """
        Builds the interface
        
        Arguments:
        - self: The main object pointer
        """

        accelGroup = gtk.AccelGroup()
        self.add_accel_group( accelGroup )
        
        self.accelGroup = accelGroup
        
        self.set_title( "mouseTrap" )
        self.connect( "destroy", self.close)
       
        self.vBox = gtk.VBox()

        self.buttonsBox = gtk.HButtonBox()

        self.prefButton = gtk.Button()
        self.prefButton.add(self._newStockImageButton(_("_Preferences"), gtk.STOCK_PREFERENCES))
        self.prefButton.connect("clicked", self._loadPreferences)
        self.buttonsBox.pack_start( self.prefButton )

        self.closeButton = gtk.Button()
        self.closeButton.add(self._newStockImageButton(_("_Exit"), gtk.STOCK_QUIT))
        self.closeButton.connect("clicked", self.close)
        self.buttonsBox.pack_start( self.closeButton )
        
        self.helpButton = gtk.Button()
        self.helpButton.add(self._newStockImageButton(_("_Help"), gtk.STOCK_HELP))
        self.helpButton.connect("clicked", self._loadHelp)
        self.buttonsBox.pack_start( self.helpButton )
       
        self.vBox.pack_start( self.buttonsBox )

        hBox = gtk.HBox()
        self.mapper = CoordsGui()
        hBox.pack_start(self.mapper, False, False )
        
        self.capture = gtk.Image()
        hBox.pack_start(self.capture, False, False )
        
        self.vBox.pack_end(hBox, False, False )
        
        hBox = gtk.HBox()
        showMapper = gtk.CheckButton( _("Start Point Mapper: ") )
        showMapper.set_active( self.settings.showPointMapper )
        showMapper.connect("toggled", lambda x: self.mapper.show() 
                                      if x.get_active() else  self.mapper.hide())
        hBox.pack_start( showMapper, False, False )
        
        showCapture = gtk.CheckButton( _("Show Capture: ") )
        showCapture.set_active( self.settings.showCapture )
        showCapture.connect("toggled", lambda x: self.capture.show() 
                                        if x.get_active() else  self.capture.hide())
        hBox.pack_start( showCapture, False, False )
        
        flipButton = gtk.Button( _("Flip Image") )
        flipButton.connect("clicked", self.enaDisFlip )
        hBox.pack_start( flipButton, False, False )
        
        self.vBox.pack_end(hBox, False, False )

        self.buttonsBox.show_all()
        self.vBox.show_all()
        self.add(self.vBox)
        self.show()
    
    def enaDisFlip( self, *args ):
        """
        Enables the Flip of the Image in the X axis
        
        This is for webcams that capture images as a mirror.
        
        Arguments:
        - self: The main object pointer.
        - *args: Widget related arguments.
        """
        
        self.settings.flipImage = not self.settings.flipImage
        #mouseTrap.modExec( "cam", "cmCleanLKPoints" )
        
    def updateView( self, img ):
        """
        Updates the GUI widgets (Image, Mapper)
        
        Arguments:
        - self: The main object pointer.
        """
        
        self.mapper.updateView()
        
        cv.cvResize( img, self.image, cv.CV_INTER_AREA )
        
        buff = gtk.gdk.pixbuf_new_from_data( self.image.imageData, gtk.gdk.COLORSPACE_RGB, \
                                        False, 8, int(self.image.width), int(self.image.height), \
                                        self.image.widthStep )
                                             
        #sets new pixbuf
        self.capture.set_from_pixbuf(buff)
        
    def _newStockImageButton( self, label, stock ):
        """
        Creates an image button from gtk's stock.
        
        Arguments:
        - self: The main object pointer
        - label: The buttons label
        - stock: The Stock image the button will use. E.g: gtk.STOCK_GO-FORWARD
        
        Returns buttonLabelBox A gtk.HBox that contains the new image stock button.
        """
        
        buttonLabelBox = gtk.HBox()
        
        im = gtk.image_new_from_stock( stock, gtk.ICON_SIZE_BUTTON )
        
        label = gtk.Label( label )
        label.set_alignment( 0.0, 0.5 )
        label.set_use_underline( True )
        
        buttonLabelBox.pack_start( im )
        buttonLabelBox.pack_start( label )
        buttonLabelBox.show_all()
        
        return buttonLabelBox
    
    def _loadPreferences( self, *args ):
        """
        Starts the preferences GUI
        
        Arguments:
        - self: The main object pointer.
        - *args: The widget callback arguments.
        """
        
        pref = __import__( "prefGui", globals(), locals(), [''])
        pref.showPreffGui( self.mTp )
        
    def clickDlgHandler( self, button = False ):
        """
        Process the Events related to the click panel.
        
        Arguments:
        - self: The main object pointer.
        - button: the button click to perform if not false.
        """ 
        
        poss = mouseTrap.mice( "position" )
        
        if button:
            self.clickDialog.hide()
            mouseTrap.mice("click", poss[0], poss[1], button )
            return
        
        if not self.clickDialog.props.visible:
            self.clickDialog.showPanel()
            return
        
    def _loadHelp( self, *args ):
        """
        Shows the user manual.
        
        Arguments:
        - self: The main object pointer.
        - *args: The widget callback arguments.
        """
        
        try:
            import gnome
            gnome.help_display_uri("ghelp:%s/docs/mousetrap.xml" % env.mTDataDir)
        except ImportError:
            dialogs.errorDialog( 
            "mouseTrap needs <b>gnome</b> module to show the help. Please install gnome-python and try again.", None )
            debug.log( debug.ACTIONS, _( "Highest" ) )
            
    def close( self, *args ):
        """
        Close Function for the quit button. This will kill mouseTrap.
        
        Arguments:
        - self: The main object pointer.
        - *args: The widget callback arguments.
        """
        self.mTp.quit(0)

                
class CoordsGui(gtk.DrawingArea):
    """
    A Class for the Point Mapper and its functions.
        
    Arguments:
    - gtk.DrawingArea: Widget where the mapper will be drawed
    """
    
    def __init__( self ):
        """
        Initialize the Point Mapper.
        
        Arguments:
        - self: The main object pointer.
        - mouseTrap: The mouseTrap object pointer.
        - cAm: The camera object pointer
        """
        
        gtk.DrawingArea.__init__(self)
        
        self.mTp = mouseTrap
        self.settings = mouseTrap.settings
        
        self.context  = None
        self.set_size_request(200, 160)
        self.add_events( gtk.gdk.BUTTON_PRESS_MASK | 
                         gtk.gdk.BUTTON_RELEASE_MASK | 
                         gtk.gdk.BUTTON1_MOTION_MASK )
 
        self.triggers = { 'scU' : 'orange',
                          'scD' : 'orange' }
        
        self.connect("expose_event", self.expose)

        #Desplazamiento
        self.desp = 0
        
        self.pointer = [ 0, 0 ]
    
    def drawRectangle( self, context, initX, initY, width, height, color ):
        r, g, b = color
        context.set_source_rgb(r, g, b)
        context.rectangle( initX, initY, width, height)
        context.stroke()
        
        return True
        
    def updateView( self ):
        """
        Updates the Point Mapper view using the expose_event
        
        Arguments:
        - self: The main object pointer.
        """
        
        self.queue_draw()
        return True

    def expose( self, widget, event ):
        """
        Draws in the Point Mapper calling the functions that will
        draw the plane and point.
        
        Arguments:
        - self: The main object pointer.
        - widget: The Drawing area.
        - event: The event information.
        """
        
        self.context = self.window.cairo_create()
        self.context.rectangle(event.area.x, event.area.y,
                               event.area.width, event.area.height)
        self.context.clip()

        scripts.loaded.drawMapper( self.context )
       
        pointer = mouseTrap.getModVar( "cam", "mpPointer" )
        
        if pointer:
            self.drawPoint(self.context, pointer.x, pointer.y, 4)

        return True
        
    def drawPoint(self, context, X, Y, size, color = 'green'):
        """
        Draws the point
        
        Arguments:
        - self: The main object pointer.
        - context: The Cairo Context
        """
        
        self.pointer = [ X, Y ]
        context.move_to( X, Y)
        context.arc(X, Y, size, 0, 2 * pi)
        
        if color == 'green':
            context.set_source_rgb(0.7, 0.8, 0.1)
        elif color == 'blue':
            context.set_source_rgb(0.5, 0.65, 12)
        else:
            context.set_source_rgb(10, 0.8, 0.1)
            
        context.fill_preserve()
        context.stroke()
        return True
        
    def drawLine( self, ctx, x1, y1, x2, y2, color ):
        """
        Draws a Line
        
        Arguments:
        - self:  The main object pointer.
        - ctx:   The Cairo Context.
        - x1:    The Starting X coord.
        - y1:    The Starting Y coord.
        - x2:    The Ending X coord.
        - y2:    The Ending Y coord.
        - color: The line color.
        """
            
        ctx.move_to( x1, y1 )
        ctx.line_to( x2, y2 )
        ctx.set_line_width( 1.0 )
        ctx.set_source_rgb( color[0], color[1], color[2])
        ctx.stroke()    
        return True
        
def showMainGui( ):
    """
    Loads the mainGUI components and launch it.
    
    Arguments:
    - mouseTrap: The mouseTrap object pointer
    """
    
    gui = MainGui()
    gui.setWindowsIcon()
    gui.buildInterface()
    scripts.loadProfile( gui )
    return gui

