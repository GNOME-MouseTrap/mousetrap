## LICENSE

See COPYING

## INSTALL

From the mousetrap project directory:

	$ ./autogen.sh
	$ make
	$ sudo make install

## RUN

From the mousetrap project directory:

	$ cd src
	$ mousetrap

## KNOWN BUG

MouseTrap will produce errors the first time you run it. Do the following:

	# Kill running mousetrap
	^C

	# Set ShowPointMapper to False in user configuration file.
	$ vim ~/.mousetrap/userSettings.cfg

	# Run mousetrap again (still in src directory)
	$ mousetrap
