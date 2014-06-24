import gettext
import locale
import os

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

translations = gettext.translation("mousetrap", localedir=LOCALE_DIR)

_ = translations.ugettext
