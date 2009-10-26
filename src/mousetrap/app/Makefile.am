
mousetrap_SCRIPTS = \
	mousetrap

mousetrapdir=$(bindir)

mousetrap_pathdir=$(pyexecdir)

mousetrap_python_PYTHON = \
	environment.py \
	debug.py \
	__init__.py \
	main.py


SUBDIRS = lib ui addons

mousetrap_pythondir=$(pyexecdir)/mousetrap/app

install-exec-hook:
	chmod a+rx $(mousetrap_pythondir) -R
