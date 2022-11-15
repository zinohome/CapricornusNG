#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

from typing import List
from utils.amis_admin import admin
from utils.amis_admin.amis import PageSchema, TableColumn
from starlette.requests import Request
import simplejson as json
from apps.dmodels.test import Test


class TestAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='test', page_title='test', icon='fa fa-border-all')
    model = Test
    pk_name = 'id'

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list