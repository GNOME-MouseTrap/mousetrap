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

""" MouseTrap main file """

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import sys
import os 

try:
    import debug
    import dialogs
except ImportError, e:
    sys.stderr.write( "\nmouseTrap needs %s to work correctly. " % e.message.split()[-1]
    + "\nPlease check if the file exist in " 
    + " the folder or if it is installed.\n" )
    sys.exit(0)

import environment as env

from mTi18n import _

try:
    import mouse
    import shutil
    import getopt
    import gobject
    import mouseTrapPref as mTPref
except ImportError, e:
    dialogs.errorDialog( 
            "mouseTrap needs <b>%s</b> to work correctly. " % e.message.split()[-1]
            + "\nPlease check if the file exist in "  
            + " the folder or if it is installed.", None )
    debug.log( debug.LOAD, _( "Highest" ) )
    sys.exit(0)
    
# We don't want mouseTrap to fail for it.
try:
    import profiling
except:
    pass

sys.argv[0] = "mouseTrap"


## Global MainLoop
loop = gobject.MainLoop()

## Main Module's Objects Dict
modules = {}

## Settings Container
settings = None

@mouse.handler
def mice( *args ):
    pass
    
def getModVar( module, attr ):
    """
    Allow modules to share variables
        
    The idea of splitting getModVar and getModfunc is to keep order 
    and make developers think before requesting other modules attributs.
    
    Arguments:
    - module: the parent module
    - attr: The var needed
    
    return var If found, else False.
    """
    
    try:
        var = getattr( modules[module], attr )
        return var
    except:
        return False
        
def getModFunc( module, attr ):
    """
    Allow modules to share functions.
    
    The idea of splitting getModVar and getModfunc is to keep order 
    and make developers think before requesting other modules attributs.
    
    Arguments:
    - module: the parent module
    - attr: The function needed
    
    return func If found, else False
    """
        
    try:
        func = getattr( modules[module], attr )
        return func
    except:
        return False
        
def updateView( img ):
    """
    This function calls the gui's updateView function
    
    Arguments:
    - img: The image to show.
    
    return True if everything went OK!
    """
    modules["gui"].updateView( img )
    return True
    
def showMainGui( ):
    """
    This will start the mouseTraps mainGUI
    """

    global modules
    
    try:
        gui = __import__("mainGui", 
                                    globals(), 
                                    locals(), 
                                    [''])   
        if settings.showMainGui:                     
            modules["gui"] = gui.showMainGui( )
    except:
        debug.log( debug.LOAD, _( "Highest" ) )

def startCam( ):
    """
    This function starts the camera module
    """
    global modules
    
    try:
        cam            = __import__("cam", 
                                    globals(), 
                                    locals(), 
                                    [''])
                                    
        modules["cam"] = cam.Camera() 
        
        if settings.startCam:
            modules["cam"].start()
    except:
        debug.log( debug.LOAD, _( "Highest" ) )

def startEventsHandler():
    global modules
    
    try:
        modules["events"] = __import__("events", 
                                       globals(), 
                                       locals(), 
                                       [''])
        if settings.startCam:
            modules["events"].startMapperListener( modules["gui"].mapper )
    except:
        debug.log( debug.LOAD, _( "Highest" ) )
        
def startDBus( ):
    """
    This will start the mouseTraps dbus service
    """

    global dbus
    
    try:
        dbus = __import__("mTDbus", 
                                    globals(), 
                                    locals(), 
                                    [''])   
        dbus.start()
    except:
        debug.log( debug.LOAD, _( "Highest" ) )

def loadSettings( ):
    """
    This function loads the mouseTrap's settings
    """

    global settings
    
    if not settings:
        try:
            if not os.path.exists( env.configPath ):
                os.mkdir( env.configPath )
                mTPref.writeFirstConf()
            
            if not os.path.exists( env.scriptsPath ):
                shutil.copytree( "%s/scripts/" % \
                            env.appPath, env.scriptsPath )

            os.chdir(env.configPath)
            settings = __import__( "userSettings" )
        except:
            debug.log( debug.LOAD, _( "Highest" ) )
            sys.exit(0)
    else:
        try:
            reload( settings )
            
            for mod in modules:
                if getattr( modules[mod], "restart" ):
                    modules[mod].restart()
        except:
            debug.log( debug.LOAD, _( "Highest" ) )
            

def calcPoint():
    """
    Allow users to recalculate the forehead point 
    if needed.
    """
    
    if settings.startCam:
        modules["cam"].cmCleanLKPoints()

# For Profiling pourpouse uncoment the next line
# The profile file will be saved in the user config folder
# as profiling.data
# @profiling.profileit(20)
def start( ):
    """
    Starts mouseTrap executing the main functions and 
    loading the required modules.
    """
    
    loadSettings()
    
    arguments = sys.argv[1:]
    if len(arguments) == 1:
        arguments = arguments[0].split()

    try:
        # ? for help
        # e for enable
        # d for disable
        # t for mouse tiemout
        opts, args = getopt.getopt(
            arguments,
            "?hve:d:i:",
            ["help",
             "version",
             "enable=",
             "disable=",
             "timeout="])

        for opt, val in opts:
            
            # This will change the default video device input
            if opt in ("-i"):
                settings.inputDevIndex = val
                
            if opt in ("-e", "--enable"):
                value = val.strip()
                
                # This allows us to disable the main window
                # of mouseTrap to have a clearer desktop.
                if value == "main-window":
                    settings.showMainGui = True


                # This allows us to enable the webCam
                # feature in case it has been disabled.
                elif value == "cam":
                    settings.startCam = False
                else:
                    usage()
                    quit(2)

            if opt in ("-d", "--disable"):
                value = val.strip()

                if value == "main-window":
                    settings.showMainGui = False
                elif value == "cam":
                    settings.startCam = False
                else:
                    usage()
                    quit(2)
                    
            
            # This is to set a timeout for the mouse listener.
            # Whe the timeout is reached the listener will attempt
            # to get the nearest icon in case the listener is enabled.
            if opt in ("-v", "--version"):
                print env.version
                quit(0)
                    
            # This will show the usage of mouseTrap
            if opt in ("-?", "-h", "--help"):
                usage()
                quit(0)
                
            # This will show the usage of mouseTrap
            #if opt in ("-?", "-h", "--help"):
             #   usage()
              #  quit(0)
                
    except getopt.GetoptError, err:
        print str(err)
        usage()
        quit(2)

    startDBus()
    showMainGui()
    startCam()
    startEventsHandler()
    
    try:
        gobject.threads_init()
        loop.run()
    except KeyboardInterrupt:
        print "KeyboardInterrupt"
        quit(0)
    except:
        debug.log( debug.LOAD, _( "Highest" ) )

               
def usage( ):
    """
    This function shows the usage and the mouseTraps options.
    """
    print _("Usage: mouseTrap [OPTION...]")
    
    # '-?, --help' that is used to display usage information.
    #
    print "-?, -h, --help              " + \
            _("        Show this help message")
            
    
    # Option:
    # '-i' that is used to set the input camera index. E.g: -i 0
    print "-i                    " + \
            _("              Input video device index. E.g -i 0")

    # Options:
    # -e, --enable Allow the users to enable modules not permantly
    print "-e, --enable=[" \
        + _("main-window") + "|" \
        + _("cam") + "]",
    
    print _("     Enable the selected options")
    
    # Options:
    # -d, --disable Allow the users to disable modules not permanently.
    print "-d, --disable=[" \
        + _("main-window") + "|" \
        + _("cam") + "]",
        
    print _("    Disable the selected options")
    
    # Options:
    # -t --timeout To change the mouse timeout not permanently.
    print "-v, --version      " + \
            _("                 Shows mouseTrap version")
    
    print
    print _("Report bugs to flaper87@flaper87.org")
    
    
def quit( exitcode=1 ):  
    """
    Quits mouseTrap and all its process
    
    Arguments:
    - exitcode: The exitcode number. It helps to handle some quit events.
    """
    sys.exit(exitcode)
