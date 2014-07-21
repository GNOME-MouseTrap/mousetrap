from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
'''
All things computer vision.
'''

import cv2
from mousetrap.i18n import _
from mousetrap.image import Image
import mousetrap.plugins.interface as interface

import logging
LOGGER = logging.getLogger(__name__)


FRAME_WIDTH = 3
FRAME_HEIGHT = 4


class Camera(object):
    S_CAPTURE_OPEN_ERROR = _(
            'Device #%d does not support video capture interface')
    S_CAPTURE_READ_ERROR = _('Error while capturing. Camera disconnected?')

    def __init__(self, config):
        self._config = config
        self._device = \
                self._new_capture_device(config['camera']['device_index'])
        self.set_dimensions(
            config['camera']['width'],
            config['camera']['height'],
        )

    @classmethod
    def _new_capture_device(cls, device_index):
        capture = cv2.VideoCapture(device_index)

        if not capture.isOpened():
            capture.release()

            raise IOError(cls.S_CAPTURE_OPEN_ERROR % device_index)

        return capture

    def set_dimensions(self, width, height):
        self._device.set(FRAME_WIDTH, width)
        self._device.set(FRAME_HEIGHT, height)

    def read_image(self):
        ret, image = self._device.read()

        if not ret:
            raise IOError(self.S_CAPTURE_READ_ERROR)

        return Image(self._config, image)


class HaarLoader(object):

    def __init__(self, config):
        self._config = config
        self._haar_files = config['haar_files']
        self._haar_cache = {}

    def from_name(self, name):
        if not name in self._haar_files:
            raise HaarNameError(name)

        haar_file = self._haar_files[name]

        haar = self.from_file(haar_file, name)

        return haar

    def from_file(self, file_, cache_name=None):
        import os

        if cache_name in self._haar_cache:
            return self._haar_cache[cache_name]

        current_dir = os.path.dirname(os.path.realpath(__file__))

        haar_file = os.path.join(current_dir, file_)

        haar = cv2.CascadeClassifier(haar_file)

        if not cache_name is None:
            if not cache_name in self._haar_cache:
                self._haar_cache[cache_name] = haar

        return haar


class HaarNameError(Exception):
    pass


class FeatureDetector(object):

    _INSTANCES = {}

    @classmethod
    def get_detector(cls, config, name, scale_factor=1.1, min_neighbors=3):
        key = (name, scale_factor, min_neighbors)
        if key in cls._INSTANCES:
            LOGGER.info("Reusing %s detector.", key)
            return cls._INSTANCES[key]
        cls._INSTANCES[key] = FeatureDetector(
                config, name, scale_factor, min_neighbors)
        return cls._INSTANCES[key]

    @classmethod
    def clear_all_detection_caches(cls):
        for instance in cls._INSTANCES.values():
            instance.clear_cache()

    def __init__(self, config, name, scale_factor=1.1, min_neighbors=3):
        '''
        name - name of feature to detect

        scale_factor - how much the image size is reduced at each image scale
                while searching. Default 1.1.

        min_neighbors - how many neighbors each candidate rectangle should have
                to retain it. Default 3.
        '''
        LOGGER.info("Building detector: %s",
                (name, scale_factor, min_neighbors))
        self._config = config
        self._name = name
        self._single = None
        self._plural = None
        self._image = None
        self._cascade = HaarLoader(config).from_name(name)
        self._scale_factor = scale_factor
        self._min_neighbors = min_neighbors
        self._last_attempt_successful = False
        self._detect_cache = {}

    def detect(self, image):
        if image in self._detect_cache:
            message = "Detection cache hit: %(image)d -> %(result)s" % \
                    {'image':id(image), 'result':self._detect_cache[image]}
            LOGGER.debug(message)
            if isinstance(self._detect_cache[image], FeatureNotFoundException):
                message = str(self._detect_cache[image])
                raise FeatureNotFoundException(message,
                        cause=self._detect_cache[image])
            return self._detect_cache[image]
        try:
            self._image = image
            self._detect_plural()
            self._exit_if_none_detected()
            self._unpack_first()
            self._extract_image()
            self._calculate_center()
            self._detect_cache[image] = self._single
            return self._detect_cache[image]
        except FeatureNotFoundException as exception:
            self._detect_cache[image] = exception
            raise

    def _detect_plural(self):
        self._plural = self._cascade.detectMultiScale(
            self._image.to_cv_grayscale(),
            self._scale_factor,
            self._min_neighbors,
        )

    def _exit_if_none_detected(self):
        if len(self._plural) == 0:
            message = _('Feature not detected: %s') % (self._name)
            if self._last_attempt_successful:
                self._last_attempt_successful = False
                LOGGER.info(message)
            raise FeatureNotFoundException(message)
        else:
            if not self._last_attempt_successful:
                self._last_attempt_successful = True
                message = _('Feature detected: %s') % (self._name)
                LOGGER.info(message)

    def _unpack_first(self):
        self._single = dict(
                zip(['x', 'y', 'width', 'height'],
                self._plural[0]))

    def _calculate_center(self):
        self._single["center"] = {
            "x": (self._single["x"] + self._single["width"]) // 2,
            "y": (self._single["y"] + self._single["height"]) // 2,
        }

    def _extract_image(self):
        single = self._single
        from_y = single['y']
        to_y = single['y'] + single['height']
        from_x = single['x']
        to_x = single['x'] + single['width']
        image_cv_grayscale = self._image.to_cv_grayscale()
        single["image"] = Image(
            self._config,
            image_cv_grayscale[from_y:to_y, from_x:to_x],
            is_grayscale=True,
        )

    def clear_cache(self):
        self._detect_cache.clear()


class FeatureDetectorClearCachePlugin(interface.Plugin):
    def __init__(self, config):
        super(FeatureDetectorClearCachePlugin, self).__init__(config)
        self._config = config

    def run(self, app):
        FeatureDetector.clear_all_detection_caches()


class FeatureNotFoundException(Exception):
    def __init__(self, message, cause=None):
        if cause is not None:
            message = message + ', caused by ' + repr(cause)
        self.cause = cause
        super(FeatureNotFoundException, self).__init__(message)
