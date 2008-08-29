SUBDIRS = po src docs images

DISTCHECK_CONFIGURE_FLAGS = --enable-pydoc

DISTCLEANFILES =                \
	intltool-extract        \
	intltool-merge          \
	intltool-update		\
	gnome-doc-utils.make	\
	mousetrap.desktop

gtk_update_icon_cache = gtk-update-icon-cache -f -t $(datadir)/icons/hicolor

install-data-hook: update-icon-cache
uninstall-hook: update-icon-cache
update-icon-cache:
	@-if test -z "$(DESTDIR)"; then \
		echo "Updating Gtk icon cache."; \
		$(gtk_update_icon_cache); \
	else \
		echo "*** Icon cache not updated.  After (un)install, run this:"; \
		echo "***   $(gtk_update_icon_cache)"; \
	fi

desktopdir 	 = $(datadir)/applications
desktop_in_files = mousetrap.desktop.in
desktop_DATA     = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

EXTRA_DIST =                \
	ChangeLog           \
	MAINTAINERS         \
	intltool-extract.in \
	intltool-merge.in   \
	intltool-update.in

