#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

from pydantic import BaseModel as requestBaseModel

class DSWZDModel(requestBaseModel):
    ds_name: str
    ds_uri: str
    ds_schema: str
    ds_exclude_tablespaces: str
    step: str