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
from fastapi_amis_admin import admin
from fastapi_amis_admin.amis import PageSchema, TableColumn
from starlette.requests import Request
import simplejson as json
from apps.dmodels.dealer_brand import Dealer_brand


class Dealer_brandAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Dealer_Brand', page_title='Dealer_Brand', icon='fa fa-border-all')
    model = Dealer_brand
    pk_name = 'dealer_id'
    enable_bulk_create = True

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list