# MouseTrap

License: GPL v2.0 (see COPYING)


## Required

* Python
* PyYAML
* OpenCV


## Download

    $ git clone https://git.gnome.org/browse/mousetrap


## Installing

You may install MouseTrap using either `pip` or `autotools`.

### Using `pip`

    $ cd mousetrap
    $ sudo pip install .

### Using `autotools`

    $ cd mousetrap
    $ ./autogen.sh      # On Fedora, add --prefix=/usr
    $ make
    $ sudo make install


## Running

    $ mousetrap


## Using

By default, MouseTrap tracks your face, allowing you to controll the
mouse pointer using a joystick metaphore. When you look left,
the pointer moves left; look right, it moves right; look up, it moves up;
look down, it moves down; look straight ahead, it stops moving. To click,
close your left eye for about 1.5 seconds.


## Configure

    $ cp $MOUSETRAP/src/mousetrap/config_default.yaml ~/.mousetrap.yaml
    $ vim ~/.mousetrap.yaml


## Translating

1. Generate mousetrap.POT
    $ cd $MOUSETRAP
    $ bin/mt-gen-pot
2. Translate
3. Place translated `mousetrap.po` in
`$MOUSETRAP/src/mousetrap/locale/_language_/LC_MESSAGES/mousetrap.po` where
_language_ is the proper language code
(https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html).

## Writing a Plugin

### 1. Implement plugin class.

```
# Import the interface for plugins.
import mousetrap.plugins.interface as interface


# Create a logger for logging.
import logging
LOGGER = logging.getLogger(__name__)


# Define a class that inherits from mousetrap.plugins.interface.Plugin
class MyPlugin(interface.Plugin):

    # Define a constructor that takes an instance of mousetrap.config.Config
    # as the first parameter (after self).
    def __init__(self, config):
        self._config = config

        # Access class configuration by using self as a key.
        # Here we retreive 'x' from our class configuration.
        self._x = config[self]['x']

    # Define a run method that takes an instance of mousetrap.main.App as the
    # first parameter (after self). Run is called on each pass of the main
    # loop.
    def run(self, app):

        # App contians data shared between the system and plugins.
        # See mousetrap.main.App for attributes that are defined by mousetrap.
        # For example, we can access the pointer:
        app.pointer.set_position((0, 0))

        # We can access attrbitues that are populated by other plugins.
        image = app.image

        # We can make attributes available to other plugins by adding them
        # to app.
        app.greeting = 'Just saying %s!' % (self._x)
```

### 2. Edit configuration file to tell MouseTrap about your plugin.

```
#!~/.mousetrap.yaml

assembly:
- mousetrap.plugins.camera.CameraPlugin     # sets app.image
- mousetrap.plugins.display.DisplayPlugin   # displays app.image in a window
- python.path.to.MyPlugin                   # runs after CameraPlugin

classes:
  python.path.to.MyPlugin:
    x: hi
```

For more examples, see the plugins in `mousetrap.plugin`.
