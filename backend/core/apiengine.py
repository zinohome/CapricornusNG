#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
import weakref

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from apiconfig.config import config
from apiconfig.dsconfig import dsconfig
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

class APIEngine(metaclass=Cached):
    def __init__(self, name):
        self.name = name
        uri = dsconfig.Database_Config.db_uri
        log.debug('Connect use uri [ %s ]' % uri)
        syncuri = self.__sync_uri(uri)
        if syncuri is None:
            raise RuntimeError("Can't create Engine, please check uri")
        if dsconfig.Database_Config.db_Type.lower() == 'oracle':
            self.__async_engine = create_async_engine(uri,
                                                echo=False,
                                                pool_size=dsconfig.Connection_Config.con_pool_size,
                                                max_overflow=dsconfig.Connection_Config.con_max_overflow,
                                                pool_use_lifo=dsconfig.Connection_Config.con_pool_use_lifo,
                                                pool_pre_ping=dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=dsconfig.Connection_Config.con_pool_recycle,
                                                exclude_tablespaces=toolkit.to_list(
                                                    dsconfig.Database_Config.db_exclude_tablespaces)
                                                )
            self.__engine = create_engine(syncuri,
                                                echo=False,
                                                pool_size=dsconfig.Connection_Config.con_pool_size,
                                                max_overflow=dsconfig.Connection_Config.con_max_overflow,
                                                pool_use_lifo=dsconfig.Connection_Config.con_pool_use_lifo,
                                                pool_pre_ping=dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=dsconfig.Connection_Config.con_pool_recycle,
                                                exclude_tablespaces=toolkit.to_list(
                                                    dsconfig.Database_Config.db_exclude_tablespaces)
                                                )
        elif dsconfig.Database_Config.db_Type.lower() == 'sqlite':
            self.__async_engine = create_async_engine(uri,
                                                echo=False,
                                                pool_pre_ping=dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=dsconfig.Connection_Config.con_pool_recycle
                                                )
            self.__engine = create_engine(syncuri,
                                                echo=False,
                                                pool_pre_ping=dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=dsconfig.Connection_Config.con_pool_recycle
                                                )
        else:
            self.__async_engine = create_async_engine(uri,
                                                echo=False,
                                                pool_size=dsconfig.Connection_Config.con_pool_size,
                                                max_overflow=dsconfig.Connection_Config.con_max_overflow,
                                                pool_use_lifo=dsconfig.Connection_Config.con_pool_use_lifo,
                                                pool_pre_ping=dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=dsconfig.Connection_Config.con_pool_recycle
                                                )
            self.__engine = create_engine(syncuri,
                                                echo=False,
                                                pool_size=dsconfig.Connection_Config.con_pool_size,
                                                max_overflow=dsconfig.Connection_Config.con_max_overflow,
                                                pool_use_lifo=dsconfig.Connection_Config.con_pool_use_lifo,
                                                pool_pre_ping=dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=dsconfig.Connection_Config.con_pool_recycle
                                                )

    def __sync_uri(self, uri):
        db_sub, dialect_sub, drv_sub = uri.split(':')[0].split('+')[0], uri.split(':')[0].split('+')[1], uri.split(':')[1]
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

apiengine = APIEngine(config('app_profile', default='default-datasource'))

if __name__ == '__main__':
    engine = apiengine.connect()
    log.debug(engine.__class__)
    async_engine = apiengine.async_connect()
    log.debug(async_engine.__class__)
