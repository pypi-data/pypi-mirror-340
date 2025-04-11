# nsd_utils/i18n/l10n.py

import os
import gettext
_current_locale = "en"
BASE_DIR = os.path.dirname(__file__)
LOCALES_DIR = os.path.join(BASE_DIR, "locales")

def set_locale(lang):
    global _current_locale
    _current_locale = lang

def translate(msg):
    path = os.path.join(LOCALES_DIR, _current_locale, "LC_MESSAGES")
    if not os.path.isdir(path):
        return msg
    try:
        t = gettext.translation("bot", localedir=LOCALES_DIR, languages=[_current_locale])
        t.install()
        return t.gettext(msg)
    except:
        return msg

def _(msg):
    return translate(msg)
