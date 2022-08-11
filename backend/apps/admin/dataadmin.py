#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
from asgiref.sync import sync_to_async
from asyncer import asyncify
from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.amis import Page

from apiconfig.config import config
from apiconfig.dsconfig import DSConfig
from core.apiengine import APIEngine
from .datapages import *
from .datamodels import *
try:
    import ujson as json
except ImportError:
    import json
from core.adminsite import site
from starlette.requests import Request
from util.log import log as log

@site.register_admin
class DataApiApp(admin.AdminApp):
    page_schema = amis.PageSchema(label='Tables', icon='fa fa-tools', sort=1)
    router_prefix = '/dataexplor'
    dsconfig = asyncify(DSConfig)(config('app_profile', default='default-datasource'))
    #log.debug(dsconfig.Database_Config)
    #apiengine = APIEngine(dsconfig, config('app_profile', default='default-datasource'))
    #engine = apiengine.async_connect()

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(DataHome)

class DataHome(admin.PageAdmin):
    group_schema = None
    page_schema = 'Hello World Page'
    # 通过page类属性直接配置页面信息;
    page = Page(title='标题', body='Hello World!')