from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import gettext
import os

import logging
LOGGER = logging.getLogger(__name__)

LOCALE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "locale"))
LOGGER.debug("LOCALE_DIR = %s", LOCALE_DIR)

translations = gettext.translation("mousetrap", localedir=LOCALE_DIR)

try:
    _ = translations.ugettext
except AttributeError:
    _ = translations.gettext
