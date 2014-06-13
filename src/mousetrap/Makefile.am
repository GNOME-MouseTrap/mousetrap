mousetrapdir=$(bindir)

mousetrap_pathdir=$(pyexecdir)

mousetrap_python_PYTHON = \
	__init__.py \
	vision.py \
	pointer.py \
	main.py \
	gui.py

#SUBDIRS =

mousetrap_pythondir=$(pyexecdir)/mousetrap/

install-exec-hook:
	chmod a+r $(DESTDIR)$(mousetrap_pythondir) -R
