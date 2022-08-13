#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
from typing import List

from asgiref.sync import sync_to_async
from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.amis import Page, PageSchema, TableColumn
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.requests import Request

from apps.admin.dadmins.car_partsadmin import Car_PartsAdmin
from apps.admin.dmodels.cat_parts import Car_Parts
from core.apitable import ApiTable
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
        apitable = ApiTable(dsconfig, 'None')
        alltables = apitable.get_all_tables()
        if len(alltables)>0:
            for table in alltables:
                log.debug(table.name)
            self.register_admin(Car_PartsAdmin)
        else:
            self.register_admin(Car_PartsAdmin)






