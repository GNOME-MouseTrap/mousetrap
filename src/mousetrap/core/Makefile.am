ocvfw_pathdir=$(pyexecdir)

ocvfw_python_PYTHON = \
	__init__.py \
	camera.py \
	feature_detector.py \
	heads_up_display.py \
	image_library.py \
	motion_tracker.py \
	pointer.py \
	pointer_manager \
	settings.py \
	tracker.py

ocvfw_pythondir=$(pyexecdir)/mousetrap/core

install-exec-hook:
	chmod a+rx $(DESTDIR)$(ocvfw_pythondir) -R
