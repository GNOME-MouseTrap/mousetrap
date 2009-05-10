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


"""The main GUI of mousetrap."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import gtk
import settings_gui
from math import pi


class MainGui( gtk.Window ):
    """
    MouseTrap main GUI Class
    """

    def __init__( self, controller ):
        """
        The main GUI constructor

        Arguments:
        - self: The main object pointer
        - controller: The mouseTrap's controller.
        """

        gtk.Window.__init__( self )
        self.ctr    = controller
        self.cfg    = controller.cfg
        self.script = self.ctr.script()
        #self.set_default_size(200, 400)

    def setWindowsIcon( self ):
        """
        Sets the mainGui icon

        Arguments:
        - self: The main object pointer
        """

        icon_theme = gtk.icon_theme_get_default()
        try:
            icon = icon_theme.load_icon("mousetrap", 48, 0)
        except:
            return

        gtk.window_set_default_icon(icon)


    def build_interface( self ):
        """
        Builds the interface

        Arguments:
        - self: The main object pointer
        """

        self.setWindowsIcon()

        accelGroup = gtk.AccelGroup()
        self.add_accel_group( accelGroup )

        self.accelGroup = accelGroup

        self.set_title( "MouseTrap" )
        self.connect( "destroy", self.close)
        self.setWindowsIcon()

        self.vBox = gtk.VBox()

        self.buttonsBox = gtk.HButtonBox()
        #self.buttonsBox = gtk.HBox(False,0)

        self.prefButton = gtk.Button(stock=gtk.STOCK_PREFERENCES)
        self.prefButton.connect("clicked", self._show_settings_gui)
        self.buttonsBox.pack_start( self.prefButton, True, True )

        self.closeButton = gtk.Button(stock=gtk.STOCK_QUIT)
        self.closeButton.connect("clicked", self.close)
        self.buttonsBox.pack_start( self.closeButton, True, True )

        self.helpButton = gtk.Button(stock=gtk.STOCK_HELP)
        #self.helpButton.connect("clicked", self._loadHelp)
        self.buttonsBox.pack_start( self.helpButton, True, True )

        self.vBox.pack_start( self.buttonsBox, False, False )

        self.cap_image    = gtk.Image()

        if self.cfg.getboolean("gui", "showCapture"):
            self.cap_expander = gtk.expander_new_with_mnemonic("_Camera Image")
            self.cap_expander.add(self.cap_image)
            self.cap_expander.set_expanded(True)
            #expander.connect('notify::expanded', self.expanded_cb)
            self.vBox.pack_start(self.cap_expander)

        if self.cfg.getboolean("gui", "showPointMapper"):
            self.map_expander = gtk.expander_new_with_mnemonic("_Script Mapper")
            self.map_expander.add(self.script)
            self.map_expander.set_expanded(True)
            #expander.connect('notify::expanded', self.expanded_cb)
            self.vBox.pack_start(self.map_expander)

#         hBox = gtk.HBox()
#         showMapper = gtk.CheckButton( _("Start Point Mapper: ") )
#         showMapper.set_active( self.settings.getboolean( "gui", "showPointMapper" ) )
#         showMapper.connect("toggled", lambda x: self.mapper.show()
#                                       if x.get_active() else  self.mapper.hide())
#         hBox.pack_start( showMapper, False, False )
#
#         showCapture = gtk.CheckButton( _("Show Capture: ") )
#         showCapture.set_active( self.settings.getboolean( "gui", "showCapture" ) )
#         showCapture.connect("toggled", lambda x: self.capture.show()
#                                         if x.get_active() else  self.capture.hide())
#         hBox.pack_start( showCapture, False, False )
#
#         flipButton = gtk.Button( _("Flip Image") )
#         flipButton.connect("clicked", self.recalcPoint, "flip" )
#         hBox.pack_start( flipButton, False, False )
#
#         recalcButton = gtk.Button( _("Recalc Point") )
#         recalcButton.connect("clicked", self.recalcPoint )
#         hBox.pack_start( recalcButton, False, False )
#
#         self.vBox.pack_end(hBox, False, False )
#
#         self.buttonsBox.show_all()
        self.vBox.show_all()
        self.add(self.vBox)
        self.show()

    def update_frame(self, img, point):
        """
        Updates the image

        Arguments:
        - self: The main object pointer.
        - img: The IPLimage object.
        """

        if img is None:
            return False

        #self.script.update_items(point)
        buff = gtk.gdk.pixbuf_new_from_data( img.imageData, gtk.gdk.COLORSPACE_RGB, False, 8, \
                                             int(img.width), int(img.height), img.widthStep )

        #sets new pixbuf
        self.cap_image.set_from_pixbuf(buff)

#     def recalcPoint( self, widget, flip = ''):
#         """
#         Enables the Flip of the Image in the X axis
#
#         This is for webcams that capture images as a mirror.
#
#         Arguments:
#         - self: The main object pointer.
#         - *args: Widget related arguments.
#         """
#
#         if flip:
#             self.settings.set( "cam", "flipImage",  str(not self.settings.getboolean( "cam", "flipImage" )) )
#
#         mouseTrap.calcPoint()
#
#     def updateView( self, img ):
#         """
#         Updates the GUI widgets (Image, Mapper)
#
#         Arguments:
#         - self: The main object pointer.
#         """
#
#         self.mapper.updateView()
#
#         cv.cvResize( img, self.image, cv.CV_INTER_AREA )
#
#         buff = gtk.gdk.pixbuf_new_from_data( self.image.imageData, gtk.gdk.COLORSPACE_RGB, \
#                                         False, 8, int(self.image.width), int(self.image.height), \
#                                         self.image.widthStep )
#
#         #sets new pixbuf
#         self.capture.set_from_pixbuf(buff)
#
    def _newStockImageButton( self, label, stock ):
        """
        Creates an image button from gtk's stock.

        Arguments:
        - self: The main object pointer
        - label: The buttons label
        - stock: The Stock image the button will use. E.g: gtk.STOCK_GO-FORWARD

        Returns buttonLabelBox A gtk.HBox that contains the new image stock button.
        """

        buttonLabelBox = gtk.VBox()

        im = gtk.image_new_from_stock( stock, gtk.ICON_SIZE_BUTTON )

        label = gtk.Label( label )
        #label.set_alignment( 0.0, 0.5 )
        label.set_use_underline( True )

        buttonLabelBox.pack_start( im )
        buttonLabelBox.pack_start( label )
        buttonLabelBox.show_all()

        return buttonLabelBox

    def _show_settings_gui( self, *args ):
        """
        Starts the preferences GUI

        Arguments:
        - self: The main object pointer.
        - *args: The widget callback arguments.
        """

        settings_gui.showPreffGui(self.ctr)
#
#     def clickDlgHandler( self, button = False ):
#         """
#         Process the Events related to the click panel.
#
#         Arguments:
#         - self: The main object pointer.
#         - button: the button click to perform if not false.
#         """
#
#         poss = mouseTrap.mice( "position" )
#
#         if button:
#             self.clickDialog.hide()
#             mouseTrap.mice("click", poss[0], poss[1], button )
#             return
#
#         if not self.clickDialog.props.visible:
#             self.clickDialog.showPanel()
#             return
#
#     def _loadHelp( self, *args ):
#         """
#         Shows the user manual.
#
#         Arguments:
#         - self: The main object pointer.
#         - *args: The widget callback arguments.
#         """
#
#         try:
#             import gnome
#             gnome.help_display_uri("ghelp:%s/docs/mousetrap.xml" % env.mTDataDir)
#         except ImportError:
#             dialogs.errorDialog(
#             "mouseTrap needs <b>gnome</b> module to show the help. Please install gnome-python and try again.", None )
#             debug.exception( "mainGui", "The help load failed" )

    def close( self, *args ):
        """
        Close Function for the quit button. This will kill mouseTrap.

        Arguments:
        - self: The main object pointer.
        - *args: The widget callback arguments.
        """
        exit()
        #self.mTp.quit(0)


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

        self.areas    = []
        self.axis     = False
        self.context  = None
        self.set_size_request(200, 160)
        self.add_events( gtk.gdk.BUTTON_PRESS_MASK |
                         gtk.gdk.BUTTON_RELEASE_MASK |
                         gtk.gdk.BUTTON1_MOTION_MASK )

        self.triggers = []

        self.connect("expose_event", self.expose)

        #Desplazamiento
        self.desp = 0

        self.pointer = [ 0, 0 ]

        self.connect("motion_notify_event", self.motion_notify_event)
#
#     def registerArea( self, area ):
#         """
#         Registers a new area.
#
#         Arguments:
#         - self: The main object pointer.
#         - area: The area to register
#         """
#         self.areas.append( area )
#
#     def registerTrigger( self, X, Y, size, callback, *args, **kwds ):
#         """
#         Registers a new trigger.
#
#         Arguments:
#         - self: The main object pointer.
#         - X: The X possition.
#         - Y: The Y possition.
#         - size: The trigger point size.
#         - callback: The callback function
#         - *args: Extra arguments to pass to the callback function.
#         - **kwds: Extra keywords to pass to the callback function.
#         """
#         self.triggers.append( { "X" : X, "Y" : Y, "size" : size } )
#
#         events.registerTrigger( {  "X" : X, "Y" : Y, "size" : size, "last" : 0,
#                                    "callback" : callback, "args" : args, "kwds" : kwds })
#
    def motion_notify_event(self, *args):
        print("PASA")

    def draw_rectangle( self, x, y, width, height, color ):
        """
        Draws a rectangle in the DrawingArea.

        Arguments:
        - context: The Cairo Context.
        - initX: The initial X possition.
        - initY: The initial Y possition.
        - width: The rectangle width.
        - height: The rectangle height.
        - color: An RGB color tuple. E.g: ( 255, 255, 255 )
        """

        r, g, b = color
        self.context.set_source_rgb(r, g, b)
        self.context.rectangle( x, y, width, height)
        self.context.stroke()

        return True
#
#     def updateView( self ):
#         """
#         Updates the Point Mapper view using the expose_event
#
#         Arguments:
#         - self: The main object pointer.
#         """
#
#         self.queue_draw()
#         return True
#
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

        self.draw_rectangle( 4, 5, 100, 100, (255,255,255) )
        return True

#
#         if "clk-dialog" in mouseTrap.getState():
#             self.dialogMapper()
#             return True
#
# 	if self.axis:
# 	    self.drawAxis()
#
#         self.drawAreas()
#         self.drawTriggers()
#
#         pointer = mouseTrap.getModVar( "cam", "mpPointer" )
#
#         if pointer:
#             self.drawPoint( pointer.x, pointer.y, 4 )
#
#         return True
#
#     def drawTriggers( self ):
#         """
#         Draws the registered triggers.
#
#         Arguments:
#         - self: The main object pointer.
#         """
#         for trigger in self.triggers:
#
#             color = "orange"
#
#             if self.pointer[0] in xrange( trigger["X"] - 2, trigger["X"] + 2 ) \
#                    and self.pointer[1] in xrange( trigger["Y"] - 2, trigger["Y"] + 2 ):
#                 color = "blue"
#
#             self.drawPoint( trigger["X"], trigger["Y"], trigger["size"], color )
#
#     def drawAreas( self ):
#         """
# 	Draws the areas and the parts requested ( Corner's Points, Axis)
#
#         Arguments:
#         - self: The main object pointer.
# 	"""
#         for area in self.areas:
#             self.drawRectangle( self.context,  area.xInit, area.yInit,
#                                 area.width, area.height, (0, 0, 102))
# 	    if area.drawCorners:
# 		self.drawCorners( area )
#
#
#     def drawAxis( self ):
# 	"""
# 	Draws the axis of the plane
#
# 	Arguments:
# 	- self: The main object pointer
# 	"""
#
#         self.drawLine( self.context, 100, 0, 100, 160, (255, 255, 255))
#
#         self.drawLine( self.context, 0, 80, 200, 80, (255, 255, 255))
#
#     def drawCorners( self, area):
# 	"""
# 	Draw the corner's points for the given area.
#
# 	Arguments:
# 	- self: The main object pointer.
# 	- area: The area requesting the corners
# 	"""
#
#         self.drawPoint( area.xInit, area.yInit, 3, "orange")
#
#         self.drawPoint( area.xEnd, area.yEnd, 3, "orange" )
#
#         self.drawPoint( area.xEnd, area.yInit, 3, "orange" )
#
#         self.drawPoint( area.xInit, area.yEnd, 3, "orange" )
#
#     def drawPoint(self, X, Y, size, color = 'green'):
#         """
#         Draws the point
#
#         Arguments:
#         - self: The main object pointer.
#         - X: The X possition.
#         - Y: The Y possition
#         - size: The point diameter.
#         - color: A RGB color tuple. E.g (255,255,255)
#         """
#
#         self.pointer = [ X, Y ]
#         self.context.move_to( X, Y)
#         self.context.arc(X, Y, size, 0, 2 * pi)
#
#         if color == 'green':
#             self.context.set_source_rgb(0.7, 0.8, 0.1)
#         elif color == 'blue':
#             self.context.set_source_rgb(0.5, 0.65, 12)
#         else:
#             self.context.set_source_rgb(10, 0.8, 0.1)
#
#         self.context.fill_preserve()
#         self.context.stroke()
#         return True
#
#     def drawLine( self, ctx, x1, y1, x2, y2, color ):
#         """
#         Draws a Line
#
#         Arguments:
#         - self:  The main object pointer.
#         - ctx:   The Cairo Context.
#         - x1:    The Starting X coord.
#         - y1:    The Starting Y coord.
#         - x2:    The Ending X coord.
#         - y2:    The Ending Y coord.
#         - color: The line color.
#         """
#
#         ctx.move_to( x1, y1 )
#         ctx.line_to( x2, y2 )
#         ctx.set_line_width( 1.0 )
#         ctx.set_source_rgb( color[0], color[1], color[2])
#         ctx.stroke()
#         return True
#
#     def dialogMapper( self ):
#
#         reqLim = 10
#
#         self.context.set_font_size( 20 )
#         self.context.set_source_rgb( 255, 255, 255 )
#
#         self.drawRectangle( self.context, 100 - reqLim, 80 - reqLim, reqLim*2, reqLim*2, (255,255,255))
#
# class MapperArea:
#
#     def __init__( self ):
#
#         self.xInit = None
#         self.yInit = None
#         self.xEnd  = None
#         self.yEnd  = None
#         self.width = None
#         self.height = None
# 	self.drawCorners = False
#
#         self.events = None
#
#         self.events    = { "point-move" : [],
#                       "top-left-corner" : [],
#                      "top-right-corner" : [],
#                    "bottom-left-corner" : [],
#                   "bottom-right-corner" : [] }
#
#
#         self.eventTypes = [ "point-move",
#                    "top-left-corner",
#                    "top-right-corner",
#                    "bottom-left-corner",
#                    "bottom-right-corner" ]
#
#     def area( self, xInit, yInit, xEnd, yEnd, corners = False ):
#
#         if not int(xInit) or not int(yInit) or not int(xEnd) or not int(yEnd):
#             debug.error( "mainGui", "All arguments must be INT" )
#
#         self.xInit = xInit
#         self.yInit = yInit
#         self.xEnd  = xEnd
#         self.yEnd  = yEnd
#
#         self.width  = xEnd - xInit
#         self.height = yEnd - yInit
# 	self.drawCorners = corners
#
#     def connect( self, eventType, callback, state = "active",*args, **kwds ):
#
#         self.events[ eventType ].append( { "callback" : callback,
#                                            "state"    : state,
#                                            "args"     : args,
#                                            "kwds"     : kwds } )
#
#         events.registerArea( self )
#
#
#
def showMainGui( ):
    """
    Loads the mainGUI components and launch it.

    Arguments:
    - mouseTrap: The mouseTrap object pointer
    """

    gui = MainGui()
    gui.build_interface()
    return gui

