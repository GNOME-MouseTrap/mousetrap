imgdir = $(datadir)/mouseTrap/images

install-data-local:
	@-$(mkinstalldirs) $(DESTDIR)$(imgdir)
	$(INSTALL_DATA) $(srcdir)/leftClick.png $(DESTDIR)$(imgdir)/leftClick.png
	$(INSTALL_DATA) $(srcdir)/doubleClick.png $(DESTDIR)$(imgdir)/doubleClick.png
	$(INSTALL_DATA) $(srcdir)/leftHold.png $(DESTDIR)$(imgdir)/leftHold.png
	$(INSTALL_DATA) $(srcdir)/middleClick.png $(DESTDIR)$(imgdir)/middleClick.png
	$(INSTALL_DATA) $(srcdir)/rightClick.png $(DESTDIR)$(imgdir)/rightClick.png

uninstall-hook:
	rm -f $(DESTDIR)$(imgdir)/leftClick.png
	rm -f $(DESTDIR)$(imgdir)/leftHold.png
	rm -f $(DESTDIR)$(imgdir)/middleClick.png
	rm -f $(DESTDIR)$(imgdir)/rightClick.png
	rm -Rf $(DESTDIR)$(datadir)/mouseTrap
