#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #  -- metastore & pagedef
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

import traceback
import weakref

from sqlalchemy import select, insert, update, delete
import simplejson as json

from apps.admin.models.tablemeta import TableMeta
from core.settings import settings
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

class ApiTable(metaclass=Cached):
    def __init__(self, dsconfig, name):
        self.dsconfig = dsconfig
        self.meta_id = None
        self.name = name
        self.dbconn_id = self.dsconfig.Database_Config.conn_id
        self.table_schema = None
        self.table_type = None
        self.primarykeys = None
        self.indexes = None
        self.columns = None
        self.valuedict = None

    def loadfrom_json(self,jsonobj):
        if 'meta_id' in jsonobj:
            self.meta_id = jsonobj['meta_id']
        if 'name' in jsonobj:
            self.name = jsonobj['name']
        if 'dbconn_id' in jsonobj:
            self.dbconn_id = jsonobj['dbconn_id']
        if 'table_schema' in jsonobj:
            self.table_schema = jsonobj['table_schema']
        if 'table_type' in jsonobj:
            self.table_type = jsonobj['table_type']
        if 'primarykeys' in jsonobj:
            if isinstance(jsonobj['primarykeys'],list):
                jsonobj['primarykeys'] = ','.join(jsonobj['primarykeys'])
            self.primarykeys = jsonobj['primarykeys']
        if 'indexes' in jsonobj:
            if isinstance(jsonobj['indexes'],list):
                jsonobj['indexes'] = ','.join(jsonobj['indexes'])
            self.indexes = jsonobj['indexes']
        if 'columns' in jsonobj:
            self.columns = jsonobj['columns']
        self.valuedict = jsonobj

    def existed_table(self):
        try:
            result = self.query_table_byName()
            if result is not None:
                if len(result) > 0:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as exp:
            log.error('Exception at ApiTable.existed_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return False

    async def async_existed_table(self):
        try:
            result = await self.async_query_table_byName()
            if result is not None:
                if len(result) > 0:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as exp:
            log.error('Exception at ApiTable.existed_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return False

    def query_table_byName(self):
        try:
            stmt = select(TableMeta).where(TableMeta.name == self.name, TableMeta.dbconn_id == self.dbconn_id)
            result = self.dsconfig.db.scalars_all(stmt)
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at ApiTable.query_table_byName() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_query_table_byName(self):
        try:
            stmt = select(TableMeta).where(TableMeta.name == self.name, TableMeta.dbconn_id == self.dbconn_id)
            result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at ApiTable.async_query_table_byName() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def get_all_tables(self):
        try:
            stmt = select(TableMeta).where(TableMeta.dbconn_id == self.dbconn_id)
            result = self.dsconfig.db.scalars_all(stmt)
            return result
        except Exception as exp:
            log.error('Exception at ApiTable.get_all_tables() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_get_all_tables(self):
        try:
            stmt = select(TableMeta).where(TableMeta.dbconn_id == self.dbconn_id)
            result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at ApiTable.async_get_all_tables() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def getall_table_Name(self):
        try:
            stmt = select(TableMeta).where(TableMeta.dbconn_id == self.dbconn_id)
            result = self.dsconfig.db.scalars_all(stmt)
            return result
        except Exception as exp:
            log.error('Exception at ApiTable.getall_table_Name() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_getall_table_Name(self):
        try:
            stmt = select(TableMeta).where(TableMeta.dbconn_id == self.dbconn_id)
            result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            if len(result) > 0:
                resultlist = []
                for record in result:
                    resultlist.append(record.name)
                return resultlist
            else:
                return None
        except Exception as exp:
            log.error('Exception at ApiTable.async_getall_table_Name() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def create_table(self):
        try:
            insertdict = self.valuedict.copy()
            if 'meta_id' in insertdict:
                del insertdict['meta_id']
            stmt = insert(TableMeta).values(insertdict)
            result = self.dsconfig.db.execute(stmt)
            return result.lastrowid
        except Exception as exp:
            log.error('Exception at ApiTable.create_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_create_table(self):
        try:
            insertdict = self.valuedict.copy()
            if 'meta_id' in insertdict:
                del insertdict['meta_id']
            stmt = insert(TableMeta).values(insertdict)
            result = await self.dsconfig.asyncdb.async_execute(stmt)
            return result.lastrowid
        except Exception as exp:
            log.error('Exception at ApiTable.async_create_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def create_update_table(self):
        try:
            stmt = select(TableMeta).where(TableMeta.name == self.name, TableMeta.dbconn_id == self.dbconn_id)
            result = self.dsconfig.db.scalars_all(stmt)
            if len(result) > 0:
                # update ingore pagedef
                olddict = result[0].dict()
                updatedict = self.valuedict.copy()
                stmt = update(TableMeta).where(TableMeta.meta_id == olddict['meta_id']).values(updatedict)
                result = self.dsconfig.db.execute(stmt)
                self.valuedict['meta_id'] = olddict['meta_id']
                return self.valuedict['meta_id']
            else:
                # insert
                insertdict = self.valuedict.copy()
                if 'meta_id' in insertdict:
                    del insertdict['meta_id']
                stmt = insert(TableMeta).values(insertdict)
                result = self.dsconfig.db.execute(stmt)
                return result.lastrowid
        except Exception as exp:
            log.error('Exception at ApiTable.create_update_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_create_update_table(self):
        try:
            stmt = select(TableMeta).where(TableMeta.name == self.name, TableMeta.dbconn_id == self.dbconn_id)
            result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            if len(result) > 0:
                #update ingore pagedef
                olddict = result[0].dict()
                updatedict = self.valuedict.copy()
                stmt = update(TableMeta).where(TableMeta.meta_id == olddict['meta_id']).values(updatedict)
                result = await self.dsconfig.asyncdb.async_execute(stmt)
                self.valuedict['meta_id'] = olddict['meta_id']
                return self.valuedict['meta_id']
            else:
                #insert
                insertdict = self.valuedict.copy()
                if 'meta_id' in insertdict:
                    del insertdict['meta_id']
                stmt = insert(TableMeta).values(insertdict)
                result = await self.dsconfig.asyncdb.async_execute(stmt)
                return result.lastrowid
        except Exception as exp:
            log.error('Exception at ApiTable.async_create_update_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def delete_table(self):
        try:
            stmt = delete(TableMeta).where(TableMeta.meta_id == self.meta_id)
            result = self.dsconfig.db.execute(stmt)
            return result.rowcount
        except Exception as exp:
            log.error('Exception at ApiTable.delete_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_delete_table(self):
        try:
            stmt = delete(TableMeta).where(TableMeta.meta_id == self.meta_id)
            result = await self.dsconfig.asyncdb.async_execute(stmt)
            return result.rowcount
        except Exception as exp:
            log.error('Exception at ApiTable.async_delete_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


if __name__ == '__main__':
    pass
    #apitable = ApiTable(main.dsconfig,'None')
    #log.debug(apitable.get_all_tables())