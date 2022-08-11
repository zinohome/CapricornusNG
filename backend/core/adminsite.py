import asyncio
import weakref
from types import SimpleNamespace

from asgiref.sync import async_to_sync, sync_to_async
from fastapi_amis_admin import admin
from sqlalchemy import select, create_engine
import simplejson as json
from sqlalchemy.ext.asyncio import create_async_engine

from apiconfig.config import config
from apps.admin.models import DBConnection, DBConfig, TableMeta
from core.settings import settings
from fastapi_user_auth.site import AuthAdminSite
from util import toolkit
from util.log import log as log
from fastapi import FastAPI
from fastapi_amis_admin.admin import Settings, AdminSite
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi_user_auth.auth import Auth

class ZinoAdminSite(AuthAdminSite):
    def __init__(self, settings: Settings, fastapi: FastAPI = None, engine: AsyncEngine = None, auth: Auth = None):
        super().__init__(settings,fastapi,engine,auth)
        self.dsconfig = None
        self.apiengine = None

    async def get_dsconfig(self):
        self.dsconfig = DSConfig(config('app_profile', default='default-datasource'))
        await self.dsconfig.readconfig()
        self.apiengine = APIEngine(site.dsconfig)

site = ZinoAdminSite(settings)
auth = site.auth
site.unregister_admin(admin.HomeAdmin)

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
        #self.loaddefault()

    def loaddefault(self):
        Database_Config_dict = {'name': 'sample-datasource', 'db_uri': 'sqlite+aiosqlite:////Users/zhangjun/PycharmProjects/CapricornusNG/backend/data/sample.db?check_same_thread=False', 'db_Type': 'sqlite', 'db_useschema': False, 'db_exclude_tablespaces': None, 'id': 2, 'db_Dialect': 'aiosqlite', 'db_schema': None, 'db_conf_id': 2}
        Application_Config_dict = {'app_name': 'Capricornus', 'app_version': 'v2.1.5', 'app_description': 'REST API for RDBMS', 'app_prefix': '/api/v2', 'app_cors_origins': "'*'", 'app_service_model': 'Standalone', 'app_param_prefix': 'up_b_', 'app_force_generate_meta': True, 'app_log_level': 'INFO', 'app_user_func': True, 'app_exception_detail': True, 'app_admin_use_https': False, 'app_confirm_key': 'Confirmed', 'app_http_port': 8880, 'app_https_port': 8843, 'app_http_timeout': 10, 'app_load_metadat_on_load': True, 'app_clear_metadat_on_startup': True, 'app_clear_metadat_on_shutdown': True}
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

class APIEngine(metaclass=Cached):
    def __init__(self, dsconfig):
        self.dsconfig = dsconfig
        self.name = dsconfig.Database_Config.name
        uri = self.dsconfig.Database_Config.db_uri
        log.debug('Connect use uri [ %s ]' % uri)
        syncuri = self.__sync_uri(uri)
        if syncuri is None:
            raise RuntimeError("Can't create Engine, please check uri")
        if self.dsconfig.Database_Config.db_Type.lower() == 'oracle':
            self.__async_engine = create_async_engine(uri,
                                                echo=False,
                                                pool_size=self.dsconfig.Connection_Config.con_pool_size,
                                                max_overflow=self.dsconfig.Connection_Config.con_max_overflow,
                                                pool_use_lifo=self.dsconfig.Connection_Config.con_pool_use_lifo,
                                                pool_pre_ping=self.dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=self.dsconfig.Connection_Config.con_pool_recycle,
                                                exclude_tablespaces=toolkit.to_list(
                                                    self.dsconfig.Database_Config.db_exclude_tablespaces)
                                                )
            self.__engine = create_engine(syncuri,
                                                echo=False,
                                                pool_size=self.dsconfig.Connection_Config.con_pool_size,
                                                max_overflow=self.dsconfig.Connection_Config.con_max_overflow,
                                                pool_use_lifo=self.dsconfig.Connection_Config.con_pool_use_lifo,
                                                pool_pre_ping=self.dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=self.dsconfig.Connection_Config.con_pool_recycle,
                                                exclude_tablespaces=toolkit.to_list(
                                                    self.dsconfig.Database_Config.db_exclude_tablespaces)
                                                )
        elif self.dsconfig.Database_Config.db_Type.lower() == 'sqlite':
            self.__async_engine = create_async_engine(uri,
                                                echo=False,
                                                pool_pre_ping=self.dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=self.dsconfig.Connection_Config.con_pool_recycle
                                                )
            self.__engine = create_engine(syncuri,
                                                echo=False,
                                                pool_pre_ping=self.dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=self.dsconfig.Connection_Config.con_pool_recycle
                                                )
        else:
            self.__async_engine = create_async_engine(uri,
                                                echo=False,
                                                pool_size=self.dsconfig.Connection_Config.con_pool_size,
                                                max_overflow=self.dsconfig.Connection_Config.con_max_overflow,
                                                pool_use_lifo=self.dsconfig.Connection_Config.con_pool_use_lifo,
                                                pool_pre_ping=self.dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=self.dsconfig.Connection_Config.con_pool_recycle
                                                )
            self.__engine = create_engine(syncuri,
                                                echo=False,
                                                pool_size=self.dsconfig.Connection_Config.con_pool_size,
                                                max_overflow=self.dsconfig.Connection_Config.con_max_overflow,
                                                pool_use_lifo=self.dsconfig.Connection_Config.con_pool_use_lifo,
                                                pool_pre_ping=self.dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=self.dsconfig.Connection_Config.con_pool_recycle
                                                )

    def __sync_uri(self, uri):
        db_sub, dialect_sub, drv_sub = uri.split(':')[0].split('+')[0].strip(), uri.split(':')[0].split('+')[1].strip(), uri.split(':')[1].strip()
        sync_dialect_sub = ''
        if db_sub == 'sqlite':
            sync_dialect_sub = 'pysqlite'
        elif db_sub == 'mysql':
            sync_dialect_sub = 'pymysql'
        elif db_sub == 'oracle':
            sync_dialect_sub = 'cx_oracle'
        elif db_sub == 'postgresql':
            sync_dialect_sub = 'psycopg2'
        else:
            sync_dialect_sub = None
        if sync_dialect_sub is None:
            return None
        else:
            syncuri = f'{db_sub}+{sync_dialect_sub}:{drv_sub}'
        return syncuri

    def connect(self):
        return self.__engine

    def async_connect(self):
        return self.__async_engine


#from fastapi_scheduler import SchedulerAdmin

#scheduler = SchedulerAdmin.bind(site)

