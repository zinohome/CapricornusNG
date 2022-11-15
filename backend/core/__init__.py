import gettext
import os
from utils.translation import i18n
from core.settings import settings

applan = settings.language
i18n.set_language(applan)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
i18n.load_translations({
    applan: gettext.translation(
        domain='messages',
        localedir=os.path.join(BASE_DIR, "locale"),
        languages=[applan]
    )
})
