# -*- coding: utf-8 -*-

# MOUSEtrap
#
# Copyright 2008 Flavio Percoco Premoli
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

""" Holds mousetrap internal information. """

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli."
__license__   = "GPLv2"

import sys
import os
import gtk

## mousetrap Version
version     = "@MOUSETRAP_VERSION@"

## "--prefix" parameter used when configuring the build.
prefix      = "@prefix@"

## The package name (should be "mousetrap").
package     = "@PACKAGE@"

## The name of the data directory (usually "share").
datadirname = "%s/@DATADIRNAME@" % prefix

## Directly mousetrap data dir
mTDataDir = "%s/mousetrap" % datadirname

## The actuall running desktop manager.
desktop = os.getenv("DESKTOP_MANAGER")

## The name of the O.S
osName = os.name

## The application's path
appPath = os.path.dirname(__file__)

## The user's home directory
home = os.path.expanduser("~")

## Configurations dir
configPath = home + "/.mousetrap/"

## Configurations dir
configPath = "%s/.mousetrap/" % home

## Scripts Path
scriptsPath = "%s/scripts/" % configPath

## Profiles Path
profilesPath = "%s/profiles/" % scriptsPath

## The config file
configFile = configPath + "userSettings.cfg"

## The debug file
debugFile = configPath + "mousetrap_DEBUG.log"

## The language path
langPath = "%s/locale/" % datadirname

## The haarcascade folder
haarcascades = appPath + "/haarcascade"

## The debugging parts
DEBUG = ['widget']

## mousetrap Modules
mTModules = { 'lTr' : '_startListener',
              'cAm' : '_startCam',
			  'wTp' : '_startWidgetsTrap'}


## Screen Resolution
screen       = { 'width'  : gtk.gdk.screen_width(),
                 'height' : gtk.gdk.screen_height()}

## Mose Movement Modes
mouseModes = { }

###################################################
#                                                 #
#          MOUSETRAP'S STATES DEFINITION          #
#                                                 #
###################################################

## Mousetrap is active and the mouse pointer can be moved
ACTIVE = "active"

## Mousetrap is active and the click dialog is not hidden.
CLKDLG = "clk-dialog"
