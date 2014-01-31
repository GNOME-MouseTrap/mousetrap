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


"""Scripts Common Widgets Module."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import cairo
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk
from math import pi

BORDER_WIDTH = 0

# A quite simple gtk.Widget subclass which demonstrates how to subclass
# and do realizing, sizing and drawing.

class Mapper(Gtk.Widget):

    def __init__(self, width, height):
        GObject.GObject.__init__(self)

        self.width   = width
        self.height  = height
        self.events  = { "motion" : [],
                         "click"  : []}
        self.set_size_request(width, height)
#         self._layout = self.create_pango_layout(text)
#         self._layout.set_font_description(pango.FontDescription("Sans Serif 16"))

    def do_realize(self):
        """
        Called when the widget should create all of its
        windowing resources.  We will create our gtk.gdk.Window
        and load our star pixmap.
        """

        # For some reason pylint says that a VBox doesn't have a set_spacing or pack_start member.
        # pylint: disable-msg=E1101
        # Mapper.do_realize: Class 'style' has no 'attach' member
        # Mapper.do_realize: Class 'style' has no 'set_background' member
        # Mapper.do_realize: Class 'style' has no 'fg_gc' member

        # First set an internal flag telling that we're realized
        self.set_realized(True)

        # Create a new gdk.Window which we can draw on.
        # Also say that we want to receive exposure events
        # and button click and button press events

        attr = Gdk.WindowAttr()
        attr.window_type = Gdk.WindowType.CHILD
        attr.wclass = Gdk.WindowWindowClass.INPUT_OUTPUT
        attr.event_mask = self.get_events() | Gdk.EventMask.EXPOSURE_MASK | Gdk.EventMask.BUTTON1_MOTION_MASK | \
                 Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.POINTER_MOTION_MASK | \
                 Gdk.EventMask.POINTER_MOTION_HINT_MASK
        attr.width = self.width #self.allocation.width
        attr.height = self.height #self.allocation.height
        attr.visual = self.get_visual()

        mask = Gdk.WindowAttributesType.VISUAL | \
            Gdk.WindowAttributesType.X | \
            Gdk.WindowAttributesType.Y

        self.window = Gdk.Window.new(self.get_parent_window(), attr, mask)

        # Associate the gdk.Window with ourselves, Gtk+ needs a reference
        # between the widget and the gdk window
        self.window.set_user_data(self)

        # Attach the style to the gdk.Window, a style contains colors and
        # GC contextes used for drawing
        self.set_window(self.window)    #LMH 12/15/13

        # The default color of the background should be what
        # the style (theme engine) tells us.
        self.window.move_resize(self.allocation.x,self.allocation.y, self.allocation.width, self.allocation.height)

    def do_unrealize(self):
        # The do_unrealized method is responsible for freeing the GDK resources

        # De-associate the window we created in do_realize with ourselves
        self.window.set_user_data(None)

    def do_size_request(self, requisition):
        # The do_size_request method Gtk+ is calling on a widget to ask
        # it the widget how large it wishes to be. It's not guaranteed
        # that gtk+ will actually give this size to the widget

        requisition.width  = self.width
        requisition.height = self.height

    def do_size_allocate(self, allocation):
        # The do_size_allocate is called by when the actual size is known
        # and the widget is told how much space could actually be allocated

        # Save the allocated space
        self.allocation = allocation
        #FIXME: Shouldn't need to set x manually
        self.allocation.x = 50

        # If we're realized, move and resize the window to the
        # requested coordinates/positions
        # pylint: disable-msg=W0142
        # Mapper.do_size_allocate: Used * or ** magic
        # WE DO NEED THE *
        if self.get_realized():
            self.window.move_resize(self.allocation.x,self.allocation.y, self.allocation.width, self.allocation.height)
        # pylint: enable-msg=W0142

    def expose_event(self, widget, event):
        """
        Mapper expose event.
        """
        # The do_expose_event is called when the widget is asked to draw itself
        # Remember that this will be called a lot of times, so it's usually
        # a good idea to write this code as optimized as it can be, don't
        # Create any resources in here.

        return True

    def draw_rectangle(self, x, y, width, height, color, line):
        """
        A Method to draw rectangles.
        """

        cr = self.window.cairo_create()
        cr.rectangle(x, y, width, height)
        cr.set_line_width(line)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()

    def draw_point(self, X, Y, size, color = 'green'):
        """
        Draws the point

        Arguments:
        - self: The main object pointer.
        - X: The X possition.
        - Y: The Y possition
        - size: The point diameter.
        - color: A RGB color tuple. E.g (255,255,255)
        """

        cr = self.window.cairo_create()
        cr.set_source_rgb(0.7, 0.8, 0.1)
        cr.arc(X, Y, size, 0, 2 * pi)
        cr.fill_preserve()
        cr.stroke()

        return True

    def connect_point_event(self, event, x, y, width, height, callback):
        """
        Connects a new event in the spesified areas.

        Arguments:
        - self: The main object pointer.
        - event: The event type.
        - x: The x coord.
        - y: The y coord.
        - width: Event area width.
        - height: Event area height.
        - callback: The callback function.
        """

        if event not in self.events:
            return False

#         Working on Mapper events
#         self.events[event].append( {"x_range" : range(reg_event["x"], reg_event["x"] + reg_event["width"]),
#                                     "y_range" : range(reg_event["x"], reg_event["y"] + reg_event["height"]),
#                                     "callback" : callback} )

    def motion_notify_event(self, event):
        """
        Events
        """
        for reg_event in self.events["motion"]:
            if event.x in  reg_event["x_range"] and event.y in reg_event["y_range"]:
                reg_event["callback"]()


GObject.type_register(Mapper)
