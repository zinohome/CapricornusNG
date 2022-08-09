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
from loguru import logger as log
from core.config import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'log')
LOG_PATH = os.path.join(LOG_DIR, config('app_log_filename', default='capricornus.log'))
log.add(LOG_PATH,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            rotation="100 MB",
            retention="14 days",
            level=config('app_log_level', default='INFO'),
            enqueue=True)

if __name__ == '__main__':
    log.success('[测试log] hello, world')
    log.info('[测试log] hello, world')
    log.debug('[测试log] hello, world')
    log.warning('[测试log] hello, world')
    log.error('[测试log] hello, world')
    log.critical('[测试log] hello, world')
    log.exception('[测试log] hello, world')