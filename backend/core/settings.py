#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

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
    version: str = '0.1.2'
    site_title: str = 'CapricornusNG'
    site_icon: str = '/static/favicon.ico'
    language: str = 'zh_CN'
    amis_cdn: str = '/static/'
    amis_theme: str = 'cxd'
    allow_origins: List[str] = None


settings = Settings(_env_file=os.path.join(BASE_DIR, '.env'))


if __name__ == '__main__':
    print(settings.app_profile)