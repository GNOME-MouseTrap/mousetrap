from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf


_GDK_PIXBUF_BIT_PER_SAMPLE = 8


class ImageWindow(object):
    def __init__(self, message):
        self._window = Gtk.Window(title=message)
        self._canvas = Gtk.Image()
        self._window.add(self._canvas)

        # FIXME: Closing any window kills the application. Need a mechanism
        # that allows windows to be openned and closed, and only kill the
        # application when the last window is closed.
        self._window.connect("delete-event", Gtk.main_quit)

        self._window.show_all()

    def draw(self, image):
        '''Draw image to this window.
        '''
        image = _get_pixbuf_from_image(image)
        self._canvas.set_from_pixbuf(image)
        self._canvas.queue_draw()


def _get_pixbuf_from_image(image):
    if isinstance(image, GdkPixbuf.Pixbuf):
        return image
    return _cvimage_to_pixbuf(image.to_cv())


def _cvimage_to_pixbuf(cvimage):
    data = cvimage.tostring()
    colorspace = GdkPixbuf.Colorspace.RGB
    has_alpha_channel = False
    width = cvimage.shape[1]
    height = cvimage.shape[0]

    # dist in bytes between row starts
    row_stride = cvimage.strides[0]

    # Function used to free the data when the pixbuf's reference count drops to
    # zero, or None if the data should not be freed.
    destroy_fn = None

    # Closure data to pass to the destroy notification function.
    destroy_fn_data = None

    return GdkPixbuf.Pixbuf.new_from_data(
            data,
            colorspace, # FIXME: Need to handle grayscale.
            has_alpha_channel,
            _GDK_PIXBUF_BIT_PER_SAMPLE,
            width,
            height,
            row_stride,
            destroy_fn,
            destroy_fn_data
            )


class Gui(object):
    def __init__(self):
        self._windows = {}

    def show_image(self, window_name, image):
        '''Displays image in window named by window_name.
           May reuse named windows.
           '''
        if window_name not in self._windows:
            self._windows[window_name] = ImageWindow(window_name)
        self._windows[window_name].draw(image)

    def start(self):
        '''Start handling events.'''
        Gtk.main()


class Pointer(object):
    def __init__(self):
        gdk_display = Gdk.Display.get_default()
        device_manager = gdk_display.get_device_manager()
        self._pointer = device_manager.get_client_pointer()
        self._screen = gdk_display.get_default_screen()

    def get_position(self):
        x_index = 1
        y_index = 2
        position = self._pointer.get_position()
        return (position[x_index], position[y_index])

    def set_position(self, point):
        self._pointer.warp(self._screen, point[0], point[1])
