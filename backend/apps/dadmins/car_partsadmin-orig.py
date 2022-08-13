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

from apps.dmodels.car_parts import Car_parts

try:
    import ujson as json
except ImportError:
    import json


class Car_PartsAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Car_Parts', icon='fa fa-folder')
    model = Car_parts
    pk_name = 'part_id'
    search_fields = [Car_parts.part_name]

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list

