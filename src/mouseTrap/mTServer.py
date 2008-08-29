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



"""The Server module of mouseTrap."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import threading
import thread
import gobject
import BaseHTTPServer

import debug

class _HTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    Provides support for communicating with mouseTrap via HTTP.
    
    To test this, run:

      wget --post-data='move:X,Y' localhost:20433

    """
    
    def log_request(self, code=None, size=None):
        """
        Override to avoid getting a log message on stdout for
        each GET, POST, etc. request
        """
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><body><p>mouseTrap 0.1</p></body></html>")

    def do_POST(self):
        contentLength = self.headers.getheader('content-length')
        if contentLength:
            contentLength = int(contentLength)
            inputBody = self.rfile.read(contentLength)
            
            if inputBody.startswith("move:"):
                X, Y = inputBody[5:].split(",")
                print X + " " + Y
                self.send_response(200, 'OK')
        else:
            print "mal"

#class _HTTPRequestThread(threading.Thread):
class mTServer:
    """Runs a _HTTPRequestHandler in a separate thread."""
    
    def __init__( self, mouseTrap ):
        self.mTp      = mouseTrap 
        self.httpd    = None
        self.run      = True
        self.settings = mouseTrap.settings

    def start(self):
        """
        Try to start an HTTP server on self.settings.httpPort
        """
        
        connected = False

        while not connected:
            try:
                self.httpd = BaseHTTPServer.HTTPServer(('', self.settings.httpPort),
                                                  _HTTPRequestHandler)
                connected = True
            except:
                pass
                #debug.log( debug.MODULES, "Highest")

        if not connected:
            print "problems"
        else:
            thread.start_new_thread(self.__handler, ())
            
    def __handler( self ):
        while self.run:
            self.httpd.handle_request()
            
