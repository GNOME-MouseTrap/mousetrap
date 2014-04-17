mousetrap_pathdir=$(pyexecdir)

mousetrap_python_PYTHON = \
	debug.py \
	__init__.py


SUBDIRS = lib ui addons

mousetrap_pythondir=$(pyexecdir)/mousetrap/app

install-exec-hook:
	chmod a+rx $(DESTDIR)$(mousetrap_pythondir) -R
