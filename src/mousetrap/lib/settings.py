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


"""MouseTrap's settings handler."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import os
import ConfigParser
import mousetrap.environment as env

class settings( ConfigParser.ConfigParser ):

    def optionxform( self, optionstr ):
        return optionstr

    def write_first(self, conf_file):
        """
        Writes the first configuration file in case it doesn't exists.

        Arguments:
        self: The main object pointer
        conf_file: The config file to write.
        """

        with open(conf_file, "w") as conf:
            conf.write("[gui]")
            conf.write("\nshowCapture = True")
            conf.write("\nshowMainGui = True")
            conf.write("\nshowPointMapper = True")

            conf.write("\n\n[access]")
            conf.write("\nreqMovement = 10")

            conf.write("\n\n[cam]")
            conf.write("\nmouseMode = forehead")
            conf.write("\ninputDevIndex = 0")
            conf.write("\nflipImage = False")

            conf.write("\n\n[main]")
            conf.write("\ndebugLevel = 10")
            conf.write("\nalgorithm = forehead")
            conf.write("\nstartCam = True")

            conf.write("\n\n[mouse]")
            conf.write("\ndefClick = b1c")
            conf.write("\nstepSpeed = 5")

def load():
    cfg = settings()
    if not os.path.exists( env.configPath ):
        os.mkdir( env.configPath )
        cfg.write_first()

    if not os.path.exists( env.configFile ):
        cfg.write_first(env.configFile)

    cfg.readfp(open( env.configFile ))
    return cfg
