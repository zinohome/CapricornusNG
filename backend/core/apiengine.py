#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
from sqlalchemy.ext.asyncio import create_async_engine

from apiconfig.dbconfig import dsconfig
from util import toolkit
from util.log import log as log

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class APIEngine(object):
    def __init__(self):
        uri = dsconfig.Database_Config.db_uri
        log.debug('Connect use uri [ %s ]' % uri)
        if dsconfig.Database_Config.db_Type.lower() == 'oracle':
            self.__engine = create_async_engine(uri,
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
            self.__engine = create_async_engine(uri,
                                                echo=False,
                                                pool_pre_ping=dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=dsconfig.Connection_Config.con_pool_recycle
                                                )
        else:
            self.__engine = create_async_engine(uri,
                                                echo=False,
                                                pool_size=dsconfig.Connection_Config.con_pool_size,
                                                max_overflow=dsconfig.Connection_Config.con_max_overflow,
                                                pool_use_lifo=dsconfig.Connection_Config.con_pool_use_lifo,
                                                pool_pre_ping=dsconfig.Connection_Config.con_pool_pre_ping,
                                                pool_recycle=dsconfig.Connection_Config.con_pool_recycle
                                                )
    def connect(self):
        return self.__engine

if __name__ == '__main__':
    engine = APIEngine().connect()
    log.debug(engine.__class__)
    log.debug(dsconfig.Admin_Config.DEBUG)
    log.debug(dsconfig.Application_Config.app_param_prefix)
