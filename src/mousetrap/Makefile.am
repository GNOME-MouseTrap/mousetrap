mousetrap_SCRIPTS = \
	mousetrap

mousetrapdir=$(bindir)

mousetrap_pathdir=$(pyexecdir)

mousetrap_python_PYTHON = \
	__init__.py \
	environment.py \
	controller.py

SUBDIRS = addons app core ocvfw ui

mousetrap_pythondir=$(pyexecdir)/mousetrap/

install-exec-hook:
	chmod a+rx $(DESTDIR)$(mousetrap_pythondir) -R

##### START DIRECTORY VARIABLE SUBSTITUTIONS ##################################
# Substitution of autotool's directory vars (outside of Makefiles) must be done
# by make. edit defines a sed substitution for all the special variables. The
# mousetrap rule calls $(edit)
edit = sed \
		-e 's|@PYTHON[@]|$(PYTHON)|g' \
		-e 's|@pythondir[@]|$(pythondir)|g' \
		-e 's|@pyexecdir[@]|$(pyexecdir)|g' \
		-e 's|@pkgdatadir[@]|$(pkgdatadir)|g' \
		-e 's|@prefix[@]|$(prefix)|g'

mousetrap: Makefile
	rm -f $@ $@.tmp
	srcdir=''; \
		test -f ./$@.in || srcdir=$(srcdir)/; \
		$(edit) $${srcdir}$@.in >$@.tmp

	chmod +x $@.tmp
	chmod a-w $@.tmp
	mv $@.tmp $@

mousetrap: $(srcdir)/mousetrap.in
##### END DIRECTORY VARIABLE SUBSTITUTIONS ####################################
