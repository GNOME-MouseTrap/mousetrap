ocvfw_pathdir=$(pyexecdir)

## List all python files in this directory.
## Don't forget to escape the new line.
ocvfw_python_PYTHON = \
	__init__.py


## List all subdirectories.
#SUBDIRS = dev haars idm

## This should match the current directory.
ocvfw_pythondir=$(pyexecdir)/mousetrap/addons

install-exec-hook:
	chmod a+rx $(DESTDIR)$(ocvfw_pythondir) -R
