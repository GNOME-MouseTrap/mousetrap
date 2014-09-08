AC_PREREQ([2.69])

AC_INIT([mousetrap],[1.0.0-a],[https://bugzilla.gnome.org/enter_bug.cgi?product=mousetrap])
AM_INIT_AUTOMAKE([1.12.1 foreign])

MOUSETRAP_VERSION=1.0.0-a
AC_SUBST(MOUSETRAP_VERSION)

CURRENT_DIR=$PWD
AC_SUBST(CURRENT_DIR)

AC_PROG_INSTALL

AM_PATH_PYTHON([2.7])

AM_CHECK_PYMOD(cv2,,,[AC_MSG_ERROR(Could not find python module cv2)])
AM_CHECK_PYMOD(gi.repository,,,[AC_MSG_ERROR(Could not find python module gi.repository)])
AM_CHECK_PYMOD(Xlib,,,[AC_MSG_ERROR(Could not find python module Xlib)])
AM_CHECK_PYMOD(yaml,,,[AC_MSG_ERROR(Could not find python module yaml)])

AC_CONFIG_FILES([
Makefile
])
AC_OUTPUT
