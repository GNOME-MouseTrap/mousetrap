AC_PREREQ([2.69])

AC_INIT([mousetrap],[1.0.0-a],[https://bugzilla.gnome.org/enter_bug.cgi?product=mousetrap])
AM_INIT_AUTOMAKE([1.13.4 foreign])

MOUSETRAP_VERSION=1.0.0-a
AC_SUBST(MOUSETRAP_VERSION)

CURRENT_DIR=$PWD
AC_SUBST(CURRENT_DIR)

AC_PROG_INSTALL

AM_PATH_PYTHON([2.7])

AM_CHECK_PYMOD(cv,,,[AC_MSG_ERROR(Could not find python module cv)])
AM_CHECK_PYMOD(cv2,,,[AC_MSG_ERROR(Could not find python module cv2)])
AM_CHECK_PYMOD(gi.repository,,,[AC_MSG_ERROR(Could not find python module gi.repository)])
AM_CHECK_PYMOD(Xlib,,,[AC_MSG_ERROR(Could not find python module Xlib)])
AM_CHECK_PYMOD(yaml,,,[AC_MSG_ERROR(Could not find python module yaml)])

AC_CONFIG_FILES([
Makefile
src/Makefile
src/mousetrap/Makefile
src/mousetrap/plugins/Makefile
src/mousetrap/tests/Makefile
src/mousetrap/haars/Makefile
src/mousetrap/locale/Makefile
src/mousetrap/locale/en/Makefile
src/mousetrap/locale/en/LC_MESSAGES/Makefile
bin/Makefile
])
AC_OUTPUT

###############################################################################
# Don't include src/mousetrap/app/mousetrap.in in AC_OUTPUT.  It will be
# processed by make (see src/mousetrap/app/Makefile.am), not by autoconf or
# automake. For more information read
# http://www.gnu.org/software/autoconf/manual/autoconf.html#Installation-Directory-Variables
#
# Other files may require this same "fix" (e.g., i18n.py, environment.py,
# mousetrap.desktop).
#
#   - Stoney Jackson, dr.stoney@gmail.com, 10/10/2013
###############################################################################
