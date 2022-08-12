#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
from asgiref.sync import sync_to_async
from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.amis import Page, PageSchema
from sqlalchemy.ext.asyncio import AsyncEngine

from apps.admin.datamodels import Car_Parts
from core.settings import settings
from main import dsconfig, apiengine
try:
    import ujson as json
except ImportError:
    import json
from core.adminsite import site
from util.log import log as log

@site.register_admin
class DataApp(admin.AdminApp):
    page_schema = amis.PageSchema(label='Tables', icon='fa fa-table', sort=1)
    router_prefix = '/data'
    engine = apiengine.async_connect()

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(Car_PartsAdmin)

class Car_PartsAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Car_Parts', icon='fa fa-folder')
    model = Car_Parts
    pk_name = 'part_id'
    search_fields = [Car_Parts.part_name]

