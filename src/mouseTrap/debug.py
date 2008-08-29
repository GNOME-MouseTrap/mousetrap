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

"""The debug module of mouseTrap."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import sys
import traceback
import environment as env

##
# This debug level is used to know when a feature fails,
# normaly that feature doesn't make mouseTrap crash.
ACTIONS = 600

##
# This debug level is used to know when a module fails while
# loading.
MODULES = 400

##
# This debug level is used to know when mouseTrap crashes while starting.
LOAD	= 200

##
# It will show all debugging errors.
ALL 	= 0

##
# This is just for tracing out all the executed code.
EXTREME = 100*100

##
# The starter debugLevel. Should be defined in the settings file.
debugLevel	 = ALL

def log( level, priority, Trace = None ):
    """
    Write the logs in debug file and print them in the terminal.
    
    Arguments:
    - level: The debug level
    - priority: The log priority.
    - Trace: if True: The Trace will replace the log.
    """


    debugFile = open(env.debugFile, "a")

    log = ''.join(traceback.format_exception(*sys.exc_info()))

    if Trace: log = Trace
                          
    priority = '='*30 + '\nPriority:' + priority + '\n' + '='*30 + '\n'
                          
    if level >= debugLevel:
        debugFile.write(priority)
        debugFile.writelines([log, "\n"])
        print priority
        print log

    debugFile.close()
		
# The following code has been borrowed from the following URL:
# 
# http://www.dalkescientific.com/writings/diary/archive/ \
#                                     2005/04/20/tracing_python_code.html
#
import linecache

def traceit(frame, event, arg):
    """
    Line tracing utility to output all lines as they are executed by
    the interpreter.  This is to be used by sys.settrace and is for 
    debugging purposes.
   
    Arguments:
    - frame: is the current stack frame
    - event: 'call', 'line', 'return', 'exception', 'c_call', 'c_return',
             or 'c_exception'
    - arg:   depends on the event type (see docs for sys.settrace)
    
    Returns traceit
    """ 

    if event == "line":
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        if (filename.endswith(".pyc") or
            filename.endswith(".pyo")):
            filename = filename[:-1]
        name = frame.f_globals["__name__"]
        if name == "gettext" \
           or name == "locale" \
           or name == "posixpath" \
           or name == "UserDict":
            return traceit
        line = linecache.getline(filename, lineno)
        log(ALL, "Trace", "TRACE %s:%s: %s" % (name, lineno, line.rstrip()))
    return traceit
    
if debugLevel == EXTREME:
    sys.settrace(traceit)
