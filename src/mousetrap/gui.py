from gi.repository import Gtk
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
    return _cvimage_to_pixbuf(image)


def _cvimage_to_pixbuf(cvimage):
    data = cvimage.tostring()
    colorspace = GdkPixbuf.Colorspace.RGB
    has_alpha_channel = False
    width = cvimage.shape[1]
    height = cvimage.shape[0]
    return GdkPixbuf.Pixbuf.new_from_data(
            data,
            colorspace, # FIXME: Need to handle grayscale.
            has_alpha_channel,
            _GDK_PIXBUF_BIT_PER_SAMPLE,
            width,
            height,
            cvimage.strides[0], # FIXME: what is this parameter?
            None, # FIXME: what is this parameter?
            None  # FIXME: what is this parameter?
            )


_WINDOWS = {}
def show_image(window_name, image):
    '''Displays image in window named by window_name.
       May reuse named windows.
       '''
    if window_name not in _WINDOWS:
        _WINDOWS[window_name] = ImageWindow(window_name)
    _WINDOWS[window_name].draw(image)


def start():
    '''Start handling events.'''
    Gtk.main()
