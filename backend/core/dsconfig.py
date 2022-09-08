#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
import os
import random
import string
import traceback
import weakref
from types import SimpleNamespace

from sqlalchemy import select, create_engine, insert
import simplejson as json
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_database import Database, AsyncDatabase

from apps.admin.models.datasourceconfig import DatasourceConfig
from apps.admin.models.datasource import Datasource
from apps.admin.models.dsmeta import DatasourceMeta
from core.settings import settings
from util import toolkit
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
    def __init__(self, ds_name=settings.app_profile):
        self.ds_name = ds_name
        self.db_schema_existed = False
        self.Application_Config = None
        self.Schema_Config = None
        self.Query_Config = None
        self.Security_Config = None
        self.Database_Config = None
        self.Connection_Config = None
        self.Admin_Config = None
        self.engine = None
        self.db = None
        self.asyncengine = None
        self.asyncdb = None
        self.connect()
        self.init_sysdb()
        self.loaddefault()
        self.readconfig()

    def connect(self):
        self.engine = create_engine(url=toolkit.sync_uri(settings.database_url_async), echo=settings.debug, future=True)
        self.db = Database(self.engine)
        self.asyncengine = create_async_engine(url=settings.database_url_async, echo=settings.debug, future=True)
        self.asyncdb = AsyncDatabase(self.engine)

    def init_sysdb(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DB_DIR = os.path.join(BASE_DIR, "data")
        dbpath = os.path.join(DB_DIR, "sample.db")
        ds_uri = 'sqlite+aiosqlite:///' + dbpath + '?check_same_thread=False'
        Database_Config_dict = {'ds_name': 'sample-datasource',
                                'ds_uri': ds_uri,
                                'ds_exclude_tablespaces': None, 'ds_id': 2, 'ds_schema': None, 'ds_config_id': 2}
        Application_Config_dict = {'app_name': 'Capricornus', 'app_version': 'v2.1.5',
                                   'app_description': 'REST API for RDBMS', 'app_prefix': '/api/v2',
                                   'app_cors_origins': "'*'", 'app_service_model': 'Standalone',
                                   'app_param_prefix': 'up_b_', 'app_force_generate_meta': True,
                                   'app_log_level': 'INFO', 'app_user_func': True, 'app_exception_detail': True,
                                   'app_admin_use_https': False, 'app_confirm_key': 'Confirmed', 'app_http_port': 8880,
                                   'app_https_port': 8843, 'app_http_timeout': 10, 'app_jaeger_host': 'jaeger', 'app_load_metadat_on_load': True,
                                   'app_clear_metadat_on_startup': True, 'app_clear_metadat_on_shutdown': True}
        Schema_Config_dict = {'schema_cache_enabled': True, 'schema_model_refresh': True,
                              'schema_cache_filename': 'capricornus_metadata', 'schema_db_metafile': 'metadata.json',
                              'schema_db_logicpkfile': 'logicpk.json', 'schema_db_logicpkneedfile': 'logicpk-need.json',
                              'schema_fetch_all_table': True, 'schema_fetch_tables': 'table1, table2'}
        Query_Config_dict = {'query_limit_upset': 2000, 'query_default_limit': 10, 'query_default_offset': 0}
        Security_Config_dict = {'security_key': '47051d5e3bafcfcba3c80d6d1119a7adf78d2967a8972b00af1ea231ca61f589',
                                'security_algorithm': 'HS256', 'access_token_expire_minutes': 30}
        Connection_Config_dict = {'con_pool_size': 20, 'con_max_overflow': 5, 'con_pool_use_lifo': True,
                                  'con_pool_pre_ping': True, 'con_pool_recycle': 3600}
        Admin_Config_dict = {'DEBUG': True, 'SECRET_KEY': 'bgt56yh@Passw0rd', 'SESSION_COOKIE_HTTPONLY': True,
                             'REMEMBER_COOKIE_HTTPONLY': True, 'REMEMBER_COOKIE_DURATION': 3600,
                             'admin_ignore_primary_key': False}
        try:
            dsname = self.ds_name
            connstmt = select(Datasource).where(Datasource.ds_name == dsname)
            connresult = self.db.scalars_all(connstmt)
            if len(connresult) == 0:
                dsconfigname = dsname + '-config-' + ''.join(random.sample(string.ascii_letters + string.digits, 8))
                log.debug('Initialize the system configration for DataSource: %s' % dsconfigname)
                configdict = {
                    'ds_config_name':''+dsconfigname,
                    'application_params':Application_Config_dict,
                    'schema_params':Schema_Config_dict,
                    'query_params':Query_Config_dict,
                    'security_params':Security_Config_dict,
                    'connection_params':Connection_Config_dict,
                    'admin_params':Admin_Config_dict
                }
                dscfgstmt = insert(DatasourceConfig).values(configdict)
                dscfgresult = self.db.execute(dscfgstmt)
                configid = dscfgresult.lastrowid
                if configid > 0 :
                    log.debug('Initialize the system configration for DataSource: %s' % dsname)
                    dsdict = {
                        'ds_name':dsname,
                        'ds_config_id':configid,
                        'ds_uri':ds_uri ,
                        'ds_schema':'',
                        'ds_exclude_tablespaces':''
                    }
                    dsstmt = insert(Datasource).values(dsdict)
                    dsresult = self.db.execute(dsstmt)
                    log.debug(dsresult.lastrowid)
                else:
                    raise RuntimeError('DataSource Configration Initialize Error !')
        except Exception as exp:
            log.error('Exception at DSConfig.readconfig() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    def loaddefault(self):
        Database_Config_dict = {'ds_name': 'sample-datasource', 'ds_uri': 'sqlite+aiosqlite:////opt/CapricornusNG/backend/data/sample.db?check_same_thread=False', 'ds_exclude_tablespaces': None, 'ds_id': 2, 'ds_schema': None, 'ds_config_id': 2}
        Application_Config_dict = {'app_name': 'Capricornus', 'app_version': 'v2.1.5', 'app_description': 'REST API for RDBMS', 'app_prefix': '/api/v2', 'app_cors_origins': "'*'", 'app_service_model': 'Standalone', 'app_param_prefix': 'up_b_', 'app_force_generate_meta': True, 'app_log_level': 'INFO', 'app_user_func': True, 'app_exception_detail': True, 'app_admin_use_https': False, 'app_confirm_key': 'Confirmed', 'app_http_port': 8880, 'app_https_port': 8843, 'app_http_timeout': 10, 'app_jaeger_host': 'jaeger','app_load_metadat_on_load': True, 'app_clear_metadat_on_startup': True, 'app_clear_metadat_on_shutdown': True}
        Schema_Config_dict = {'schema_cache_enabled': True, 'schema_model_refresh': True, 'schema_cache_filename': 'capricornus_metadata', 'schema_db_metafile': 'metadata.json', 'schema_db_logicpkfile': 'logicpk.json', 'schema_db_logicpkneedfile': 'logicpk-need.json', 'schema_fetch_all_table': True, 'schema_fetch_tables': 'table1, table2'}
        Query_Config_dict = {'query_limit_upset': 2000, 'query_default_limit': 10, 'query_default_offset': 0}
        Security_Config_dict = {'security_key': '47051d5e3bafcfcba3c80d6d1119a7adf78d2967a8972b00af1ea231ca61f589', 'security_algorithm': 'HS256', 'access_token_expire_minutes': 30}
        Connection_Config_dict = {'con_pool_size': 20, 'con_max_overflow': 5, 'con_pool_use_lifo': True, 'con_pool_pre_ping': True, 'con_pool_recycle': 3600}
        Admin_Config_dict = {'DEBUG': True, 'SECRET_KEY': 'bgt56yh@Passw0rd', 'SESSION_COOKIE_HTTPONLY': True, 'REMEMBER_COOKIE_HTTPONLY': True, 'REMEMBER_COOKIE_DURATION': 3600, 'admin_ignore_primary_key': False}
        self.Database_Config = SimpleNamespace(**Database_Config_dict)
        self.Application_Config = SimpleNamespace(**Application_Config_dict)
        self.Schema_Config = SimpleNamespace(**Schema_Config_dict)
        self.Query_Config = SimpleNamespace(**Query_Config_dict)
        self.Security_Config = SimpleNamespace(**Security_Config_dict)
        self.Connection_Config = SimpleNamespace(**Connection_Config_dict)
        self.Admin_Config = SimpleNamespace(**Admin_Config_dict)

    def readconfig(self):
        try:
            connstmt = select(Datasource).where(
                Datasource.ds_name == self.ds_name)
            connresult = self.db.scalars_all(connstmt)
            if len(connresult) > 0:
                self.Database_Config = SimpleNamespace(**json.loads(connresult[0].json()))
                self.Database_Config.ds_useschema = False
                if (not self.Database_Config.ds_schema is None) and (len(self.Database_Config.ds_schema.strip()) > 0):
                    self.Database_Config.ds_useschema = True
                #log.debug('Database_Config: %s' % self.Database_Config)
                confstmt = select(DatasourceConfig).where(
                    DatasourceConfig.ds_config_id == self.Database_Config.ds_config_id)
                confresult = self.db.scalars_all(confstmt)
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
                tablestmt = select(DatasourceMeta).where(DatasourceMeta.ds_id == self.Database_Config.ds_id)
                tableresult = self.db.scalars_all(tablestmt)
                if len(tableresult) > 0:
                    self.db_schema_existed = True
        except Exception as exp:
            log.error('Exception at DSConfig.readconfig() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

if __name__ == '__main__':
    dsconfig = DSConfig(settings.app_profile)
    #log.debug(dsconfig.Query_Config)
    log.debug('Database_Config: %s' % dsconfig.Database_Config)
    log.debug('Application_Config: %s' % dsconfig.Application_Config)
    log.debug('Schema_Config: %s' % dsconfig.Schema_Config)
    log.debug('Query_Config: %s' % dsconfig.Query_Config)
    log.debug('Security_Config: %s' % dsconfig.Security_Config)
    log.debug('Connection_Config: %s' % dsconfig.Connection_Config)
    log.debug('Admin_Config: %s' % dsconfig.Admin_Config)
    log.debug('db_schema_existed: %s' % dsconfig.db_schema_existed)

