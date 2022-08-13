#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.admin import AdminApp

from apps.dadmins.car_partsadmin import Car_partsAdmin
from core.apitable import ApiTable
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
            self.register_admin(Car_partsAdmin)
        else:
            self.register_admin(Car_partsAdmin)






