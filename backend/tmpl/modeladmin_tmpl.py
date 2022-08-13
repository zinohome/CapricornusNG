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
from apps.dmodels.{{ name|trim|lower }} import {{ name|trim|capitalize }}


class {{ name|trim|capitalize }}Admin(admin.ModelAdmin):
    group_schema = None
    {% if table_type|trim|lower == 'table' %}
    page_schema = PageSchema(label='{{ name|trim }}', icon='fa fa-border-all')
    {% else %}
    page_schema = PageSchema(label='{{ name|trim }}', icon='fa fa-border-none')
    {% endif %}
    model = {{ name|trim|capitalize }}
    {% set lklist = logicprimarykeys.split(',') %}
    {% set lkstr=lklist[0] %}
    {% set lkliststr=name.strip().capitalize()+'.'+(', '+name.strip().capitalize()+'.').join(lklist) %}
    pk_name = '{{ lkstr }}'
    search_fields = [{{ lkliststr }}]

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list
