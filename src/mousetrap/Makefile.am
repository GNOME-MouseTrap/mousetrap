mousetrap_pathdir=$(pyexecdir)

mousetrap_python_PYTHON = \
	__init__.py \
	main.py

SUBDIRS = app ocvfw

mousetrap_pythondir=$(pyexecdir)/mousetrap/

install-exec-hook:
	chmod a+rx $(DESTDIR)$(mousetrap_pythondir) -R
