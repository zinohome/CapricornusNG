import os
from pathlib import Path
from typing import List

from fastapi_amis_admin.admin.settings import Settings as AmisSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(AmisSettings):
    name: str = 'Capricornusng'
    host: str = '0.0.0.0'
    port: int = 8000
    debug: bool = True
    secret_key: str = ''
    version: str = '0.1.1'
    site_title: str = 'CapricornusNG'
    site_icon: str = 'https://baidu.gitee.io/amis/static/favicon_b3b0647.png'
    language: str = 'zh_CN'
    allow_origins: List[str] = None


settings = Settings(_env_file=os.path.join(BASE_DIR, '.env'))
