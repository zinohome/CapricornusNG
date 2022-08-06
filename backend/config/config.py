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

import decouple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = decouple.AutoConfig()
config.encoding = 'utf-8'
config.search_path = BASE_DIR


if __name__ == '__main__':
    pass
    #config = decouple.AutoConfig()
    #print(config('app_log_filename', default='capricornus.log'))
