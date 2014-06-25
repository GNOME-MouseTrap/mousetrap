import gettext
import locale
import os

LOCALE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "locale"))

translations = gettext.translation("mousetrap", localedir=LOCALE_DIR)

_ = translations.ugettext
