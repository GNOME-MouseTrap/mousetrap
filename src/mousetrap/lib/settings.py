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


"""MouseTrap's settings handler."""

__id__        = "$Id: settings.py 30 2009-04-03 16:00:06Z flaper $"
__version__   = "$Revision: 30 $"
__date__      = "$Date: 2009-04-03 18:00:06 +0200 (vie 03 de abr de 2009) $"
__copyright__ = "Copyright (c) 2008 Flavio Percoco Premoli"
__license__   = "GPLv2"

import ConfigParser
import environment as env

class settings( ConfigParser.ConfigParser ):

    def optionxform( self, optionstr ):
        return optionstr

def load():
    cfg = settings()
    cfg.readfp(open( env.configFile ))
    return cfg
