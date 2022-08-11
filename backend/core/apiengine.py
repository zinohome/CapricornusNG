#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #  -- metastore & pagedef
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
import weakref

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

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
    def __init__(self, dsconfig):
        self.dsconfig = dsconfig
        self.name = dsconfig.Database_Config.name
        uri = self.dsconfig.Database_Config.db_uri
        log.debug('Connect use uri [ %s ]' % uri)
        syncuri = toolkit.sync_uri(uri)
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

    def connect(self):
        return self.__engine

    def async_connect(self):
        return self.__async_engine

if __name__ == '__main__':
    pass