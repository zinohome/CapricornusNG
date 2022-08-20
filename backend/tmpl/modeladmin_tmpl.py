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
from apps.dmodels.{{ meta_name|trim|lower }} import {{ meta_name|trim|capitalize }}


class {{ meta_name|trim|capitalize }}Admin(admin.ModelAdmin):
    group_schema = None
    {% if table_type|trim|lower == 'table' %}
    page_schema = PageSchema(page_title='{{ page_title|trim }}', icon='fa fa-border-all')
    {% else %}
    page_schema = PageSchema(page_title='{{ page_title|trim }}', icon='fa fa-border-none')
    {% endif %}
    model = {{ meta_name|trim|capitalize }}
    {% set lklist = page_logicprimarykeys.split(',') %}
    {% set lkstr=lklist[0] %}
    {% set lkliststr=meta_name.strip().capitalize()+'.'+(', '+meta_name.strip().capitalize()+'.').join(lklist) %}
    pk_name = '{{ lkstr }}'
    {% if list_display|trim|length >0 %}
    {% set ldlist = list_display.split(',') %}
    {% set ldliststr = meta_name.strip().capitalize() + '.' + (', ' + meta_name.strip().capitalize() + '.').join(ldlist) %}
    list_display = [{{ ldliststr }}]
    {% endif %}
    {% if search_fields|trim|length >0 %}
    {% set sflist = search_fields.split(',') %}
    {% set sfliststr = meta_name.strip().capitalize() + '.' + (', ' + meta_name.strip().capitalize() + '.').join(sflist) %}
    search_fields = [{{ sfliststr }}]
    {% endif %}

    async def get_list_columns(self, request: Request) -> List[TableColumn]:
        c_list = await super().get_list_columns(request)
        for column in c_list:
            column.quickEdit = None
        return c_list
