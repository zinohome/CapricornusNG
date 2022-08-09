#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
from types import SimpleNamespace
import asyncio
import weakref
import simplejson as json
from async_class import AsyncClass
from sqlalchemy import select
from apps.admin.models import DBConnection, DBConfig
from core.adminsite import site
from core.config import config
from util.log import log as log

class CachedDSConfig:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_config(self, name):
        if name not in self._cache:
            temp = DSConfig._new(name)
            self._cache[name] = temp
        else:
            temp = self._cache[name]
        return temp

    def clear(self):
        self._cache.clear()

class DSConfig:
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Can't instantiate directly")

    # Alternate constructor
    @classmethod
    def _new(cls, name):
        self = cls.__new__(cls)
        self.name = name
        self.Application_Config = None
        self.Schema_Config = None
        self.Query_Config = None
        self.Security_Config = None
        self.Database_Config = None
        self.Connection_Config = None
        self.Admin_Config = None
        self.readconfig(name)
        return self

    async def readconfig(self,name):
        connstmt = select(DBConnection).where(
            DBConnection.name == name)
        connresult = await site.db.async_scalars_all(connstmt)
        if len(connresult) > 0:
            self.Database_Config = SimpleNamespace(**json.loads(connresult[0].json()))
            log.debug('Database_Config: %s' % self.Database_Config)
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
                log.debug('Application_Config: %s' % self.Application_Config)
                log.debug('Schema_Config: %s' % self.Schema_Config)
                log.debug('Query_Config: %s' % self.Query_Config)
                log.debug('Security_Config: %s' % self.Security_Config)
                log.debug('Connection_Config: %s' % self.Connection_Config)
                log.debug('Admin_Config: %s' % self.Admin_Config)


if __name__ == '__main__':
    name = config('app_profile', default='default-datasource')
    dsconfig = CachedDSConfig().get_config(name)

'''
class DSConfig(AsyncClass):
    async def __ainit__(self):
        self.Application_Config = None
        self.Schema_Config = None
        self.Query_Config = None
        self.Security_Config = None
        self.Database_Config = None
        self.Connection_Config = None
        self.Admin_Config = None
        connstmt = select(DBConnection).where(
            DBConnection.name == config('app_profile', default='default-datasource'))
        connresult = await site.db.async_scalars_all(connstmt)
        if len(connresult) >  0:
            self.Database_Config = SimpleNamespace(**json.loads(connresult[0].json()))
            log.debug('Database_Config: %s' % self.Database_Config)
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
                log.debug('Application_Config: %s' % self.Application_Config)
                log.debug('Schema_Config: %s' % self.Schema_Config)
                log.debug('Query_Config: %s' % self.Query_Config)
                log.debug('Security_Config: %s' % self.Security_Config)
                log.debug('Connection_Config: %s' % self.Connection_Config)
                log.debug('Admin_Config: %s' % self.Admin_Config)

async def async_main():
    dsconfig = await DSConfig()
    
asyncio.run(async_main())

'''


if __name__ == '__main__':
    pass