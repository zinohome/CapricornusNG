#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

import sqlmodel

import simplejson as json
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _


class BaseSQLModel(sqlmodel.SQLModel):
    class Config:
        use_enum_values = True
        orm_mode = True
        arbitrary_types_allowed = True