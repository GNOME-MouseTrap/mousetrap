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

try:
    import hotshot, hotshot.stats
except ImportError:
    print "\nProfiling module needs %s to work correctly. \nPlease install it " % module \
    + " to use the profiling module.\n"
 
def profileit(printlines=1):
    def _my(func):
        def _func(*args, **kargs):
            prof = hotshot.Profile("profiling.data")
            res = prof.runcall(func, *args, **kargs)
            prof.close()
            stats = hotshot.stats.load("profiling.data")
            stats.strip_dirs()
            stats.sort_stats('time', 'calls')
            print ">>>---- Begin profiling print"
            stats.print_stats(printlines)
            print ">>>---- End profiling print"
            return res
        return _func
    return _my

