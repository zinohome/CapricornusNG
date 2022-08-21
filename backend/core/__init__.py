import gettext
import os
from util.translation import i18n
from core.settings import settings

i18n.set_language(settings.language)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
i18n.load_translations({
    "zh_CN": gettext.translation(
        domain='messages',
        localedir=os.path.join(BASE_DIR, "locale"),
        languages=['zh_CN']
    )
})
