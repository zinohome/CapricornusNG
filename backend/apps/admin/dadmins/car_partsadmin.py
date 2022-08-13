#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
from typing import List

from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.amis import Page, PageSchema, TableColumn
from starlette.requests import Request

from apps.admin.dmodels.cat_parts import Car_Parts
try:
    import ujson as json
except ImportError:
    import json
from util.log import log as log


class Car_PartsAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Car_Parts', icon='fa fa-folder')
    model = Car_Parts
    pk_name = 'part_id'
    search_fields = [Car_Parts.part_name]

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list

