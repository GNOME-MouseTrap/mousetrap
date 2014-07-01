import gettext
import os

import logging
LOGGER = logging.getLogger(__name__)

LOCALE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "locale"))
LOGGER.debug("LOCALE_DIR = %s", LOCALE_DIR)

_ = gettext.translation("mousetrap", localedir=LOCALE_DIR).ugettext
