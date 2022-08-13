#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
import importlib

from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.admin import AdminApp

from apps.dadmins.car_partsadmin import Car_partsAdmin
from core.apitable import ApiTable
from main import dsconfig, apiengine, dbmeta

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
        alltables = dbmeta.get_tables() + dbmeta.get_views()
        if len(alltables)>0:
            for tbl in alltables:
                dtable = dbmeta.gettable(tbl)
                log.debug(dtable.primarykeys)
                if len(dtable.primarykeys.strip()) > 0:
                    adminmodel = importlib.import_module('apps.dadmins.' + tbl.strip().lower() + 'admin')
                    adminclass = getattr(adminmodel, tbl.strip().capitalize() + 'Admin')
                    self.register_admin(adminclass)
        else:
            self.register_admin(Car_partsAdmin)






