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
from apps.dmodels.manufacture_plant import Manufacture_plant


class Manufacture_plantAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Manufacture_Plant', page_title='Manufacture_Plant', icon='fa fa-border-all')
    model = Manufacture_plant
    pk_name = 'manufacture_plant_id'

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list