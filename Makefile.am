mousetrapdir=$(pkgpythondir)

EXTRA_DIST= \
	setup.py \
	src/mousetrap


##############################################################################
# TARGET: all

all-local:
	$(PYTHON) $(srcdir)/setup.py build \
		--build-base $(builddir)/build \
		--verbose


##############################################################################
# TARGET: dist

dist-hook: gen-ChangeLog gen-AUTHORS del-pyc

.PHONY: gen-ChangeLog gen-AUTHORS del-pyc
gen-ChangeLog:
	$(top_srcdir)/bin/mt-gen-ChangeLog $(distdir)/ChangeLog

gen-AUTHORS:
	$(top_srcdir)/bin/mt-gen-AUTHORS $(distdir)/AUTHORS

del-pyc:
	find . -name '*.pyc' -delete


##############################################################################
# TARGET: install

install-exec-local:
	$(PYTHON) $(srcdir)/setup.py install \
		--prefix $(DESTDIR)$(prefix) \
		--single-version-externally-managed \
		--record $(DESTDIR)$(pkgpythondir)/install_files.txt \
		--verbose


##############################################################################
# TARGET: uninstall

uninstall-local:
	cat $(DESTDIR)$(pkgpythondir)/install_files.txt | xargs rm -rf
	rm -r $(DESTDIR)$(pkgpythondir)


##############################################################################
# TARGET: clean

clean-local:
	$(PYTHON) $(srcdir)/setup.py clean --all


##############################################################################
# TARGET: distclean

distclean-local:
	rm -rf $(builddir)/mousetrap.egg-info
