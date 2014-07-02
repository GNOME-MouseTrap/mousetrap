from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
'''
All things image manipulation.
'''

import cv2
from gi.repository import GdkPixbuf


_GDK_PIXBUF_BIT_PER_SAMPLE = 8


class Image(object):
    def __init__(self, config, image_cv, is_grayscale=False):
        self._config = config
        self._image_cv = image_cv
        self._is_grayscale = is_grayscale
        self._image_cv_grayscale = None
        if self._is_grayscale:
            self._image_cv_grayscale = self._image_cv

    def to_cv(self):
        return self._image_cv

    def to_cv_grayscale(self):
        if self._image_cv_grayscale is None:
            self._image_cv_grayscale = _cv_rgb_to_cv_grayscale(self._image_cv)
        return self._image_cv_grayscale

    def to_pixbuf(self):
        return _cvimage_to_pixbuf(self._image_cv)

    def get_width(self):
        return self._image_cv.shape[0]

    def get_height(self):
        return self._image_cv.shape[1]


def _cv_rgb_to_cv_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


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
        colorspace,
        has_alpha_channel,
        _GDK_PIXBUF_BIT_PER_SAMPLE,
        width,
        height,
        row_stride,
        destroy_fn,
        destroy_fn_data,
    )
