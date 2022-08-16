#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
from fastapi_amis_admin.models import TextChoices
# TableMeta Model
class TableType(TextChoices):
    table = 'table', 'Table'
    view = 'view', 'View'