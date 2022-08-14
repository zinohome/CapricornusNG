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
from apps.dmodels.car_options import Car_options


class Car_optionsAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Car_Options', icon='fa fa-border-all')
    model = Car_options
    pk_name = 'option_set_id'
    search_fields = [Car_options.option_set_id]

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list