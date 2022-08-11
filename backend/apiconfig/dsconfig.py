#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
import asyncio
import weakref
from types import SimpleNamespace
import simplejson as json
import uvloop
from asgiref.sync import async_to_sync
from sqlalchemy import select

from apiconfig.config import config
from apps.admin.models import DBConnection, DBConfig, TableMeta
from core.adminsite import site
from util.log import log as log


class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj

class DSConfig(metaclass=Cached):
    def __init__(self, name=config('app_profile', default='default-datasource')):
        self.name = name
        self.db_schema_existed = False
        self.Application_Config = None
        self.Schema_Config = None
        self.Query_Config = None
        self.Security_Config = None
        self.Database_Config = None
        self.Connection_Config = None
        self.Admin_Config = None
        #async_to_sync(self.readconfig)()

    async def readconfig(self):
        connstmt = select(DBConnection).where(
            DBConnection.name == self.name)
        connresult = await site.db.async_scalars_all(connstmt)
        if len(connresult) > 0:
            self.Database_Config = SimpleNamespace(**json.loads(connresult[0].json()))
            #log.debug('Database_Config: %s' % self.Database_Config)
            confstmt = select(DBConfig).where(
                DBConfig.id == self.Database_Config.db_conf_id)
            confresult = await site.db.async_scalars_all(confstmt)
            if len(confresult) > 0:
                self.Application_Config = SimpleNamespace(**confresult[0].application_params)
                self.Schema_Config = SimpleNamespace(**confresult[0].schema_params)
                self.Query_Config = SimpleNamespace(**confresult[0].query_params)
                self.Security_Config = SimpleNamespace(**confresult[0].security_params)
                self.Connection_Config = SimpleNamespace(**confresult[0].connection_params)
                self.Admin_Config = SimpleNamespace(**confresult[0].admin_params)
                #log.debug('Application_Config: %s' % self.Application_Config)
                #log.debug('Schema_Config: %s' % self.Schema_Config)
                #log.debug('Query_Config: %s' % self.Query_Config)
                #log.debug('Security_Config: %s' % self.Security_Config)
                #log.debug('Connection_Config: %s' % self.Connection_Config)
                #log.debug('Admin_Config: %s' % self.Admin_Config)
            tablestmt = select(TableMeta).where(TableMeta.dbconn_id == self.Database_Config.id)
            tableresult = await site.db.async_scalars_all(tablestmt)
            if len(tableresult) > 0:
                self.db_schema_existed = True

if __name__ == '__main__':
    dsconfig = DSConfig(config('app_profile', default='default-datasource'))
    async_to_sync(dsconfig.readconfig)()
    log.debug(config('app_mode', default='worker'))
    #log.debug(dsconfig.Admin_Config)
    log.debug('Application_Config: %s' % dsconfig.Application_Config)
    log.debug('Schema_Config: %s' % dsconfig.Schema_Config)
    log.debug('Query_Config: %s' % dsconfig.Query_Config)
    log.debug('Security_Config: %s' % dsconfig.Security_Config)
    log.debug('Connection_Config: %s' % dsconfig.Connection_Config)
    log.debug('Admin_Config: %s' % dsconfig.Admin_Config)
    log.debug('Database_Config: %s' % dsconfig.Database_Config)
    log.debug('db_schema_existed: %s' % dsconfig.db_schema_existed)
