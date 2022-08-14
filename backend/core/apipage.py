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

from core.settings import settings
from apps.admin.models import TablePage
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

class ApiPage(metaclass=Cached):
    def __init__(self, dsconfig, name):
        self.dsconfig = dsconfig
        self.id = None
        self.name = name
        self.label = None
        self.dbconn_id = self.dsconfig.Database_Config.id
        self.table_schema = None
        self.table_type = None
        self.primarykeys = None
        self.logicprimarykeys = None
        self.indexes = None
        self.list_display = None
        self.search_fields = None
        self.columns = None
        self.valuedict = None

    def loadfrom_json(self,jsonobj):
        if 'id' in jsonobj:
            self.id = jsonobj['id']
        if 'name' in jsonobj:
            self.name = jsonobj['name']
        if 'label' in jsonobj:
            self.label = jsonobj['label']
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
        if 'logicprimarykeys' in jsonobj:
            if isinstance(jsonobj['logicprimarykeys'],list):
                jsonobj['logicprimarykeys'] = ','.join(jsonobj['logicprimarykeys'])
            self.logicprimarykeys = jsonobj['logicprimarykeys']
        if 'indexes' in jsonobj:
            if isinstance(jsonobj['indexes'],list):
                jsonobj['indexes'] = ','.join(jsonobj['indexes'])
            self.indexes = jsonobj['indexes']
        if 'list_display' in jsonobj:
            self.list_display = jsonobj['list_display']
        if 'search_fields' in jsonobj:
            self.search_fields = jsonobj['search_fields']
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
            log.error('Exception at ApiPage.existed_table() %s ' % exp)
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
            log.error('Exception at ApiPage.existed_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return False

    def query_table_byName(self):
        try:
            stmt = select(TablePage).where(TablePage.name == self.name, TablePage.dbconn_id == self.dbconn_id)
            result = self.dsconfig.db.scalars_all(stmt)
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at ApiPage.query_table_byName() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_query_table_byName(self):
        try:
            stmt = select(TablePage).where(TablePage.name == self.name, TablePage.dbconn_id == self.dbconn_id)
            result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at ApiPage.async_query_table_byName() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def get_all_tables(self):
        try:
            stmt = select(TablePage).where(TablePage.dbconn_id == self.dbconn_id)
            result = self.dsconfig.db.scalars_all(stmt)
            return result
        except Exception as exp:
            log.error('Exception at ApiPage.get_all_tables() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_get_all_tables(self):
        try:
            stmt = select(TablePage).where(TablePage.dbconn_id == self.dbconn_id)
            result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at ApiPage.async_get_all_tables() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def getall_table_Name(self):
        try:
            stmt = select(TablePage).where(TablePage.dbconn_id == self.dbconn_id)
            result = self.dsconfig.db.scalars_all(stmt)
            return result
        except Exception as exp:
            log.error('Exception at ApiPage.getall_table_Name() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_getall_table_Name(self):
        try:
            stmt = select(TablePage).where(TablePage.dbconn_id == self.dbconn_id)
            result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            if len(result) > 0:
                resultlist = []
                for record in result:
                    resultlist.append(record.name)
                return resultlist
            else:
                return None
        except Exception as exp:
            log.error('Exception at ApiPage.async_getall_table_Name() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def create_table(self):
        try:
            insertdict = self.valuedict.copy()
            if 'id' in insertdict:
                del insertdict['id']
            stmt = insert(TablePage).values(insertdict)
            result = self.dsconfig.db.execute(stmt)
            return result.lastrowid
        except Exception as exp:
            log.error('Exception at ApiPage.create_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_create_table(self):
        try:
            insertdict = self.valuedict.copy()
            if 'id' in insertdict:
                del insertdict['id']
            stmt = insert(TablePage).values(insertdict)
            result = await self.dsconfig.asyncdb.async_execute(stmt)
            return result.lastrowid
        except Exception as exp:
            log.error('Exception at ApiPage.async_create_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def create_update_table(self):
        try:
            stmt = select(TablePage).where(TablePage.name == self.name, TablePage.dbconn_id == self.dbconn_id)
            result = self.dsconfig.db.scalars_all(stmt)
            if len(result) > 0:
                # update ingore pagedef
                olddict = result[0].dict()
                updatedict = self.valuedict.copy()
                updatedict['label'] = olddict['label']
                self.valuedict['label'] = olddict['label']
                stmt = update(TablePage).where(TablePage.id == olddict['id']).values(updatedict)
                result = self.dsconfig.db.execute(stmt)
                self.valuedict['id'] = olddict['id']
                return self.valuedict['id']
            else:
                # insert
                insertdict = self.valuedict.copy()
                if 'id' in insertdict:
                    del insertdict['id']
                stmt = insert(TablePage).values(insertdict)
                result = self.dsconfig.db.execute(stmt)
                return result.lastrowid
        except Exception as exp:
            log.error('Exception at ApiPage.create_update_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_create_update_table(self):
        try:
            stmt = select(TablePage).where(TablePage.name == self.name, TablePage.dbconn_id == self.dbconn_id)
            result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            if len(result) > 0:
                #update ingore pagedef
                olddict = result[0].dict()
                updatedict = self.valuedict.copy()
                updatedict['label'] = olddict['label']
                self.valuedict['label'] = olddict['label']
                stmt = update(TablePage).where(TablePage.id == olddict['id']).values(updatedict)
                result = await self.dsconfig.asyncdb.async_execute(stmt)
                self.valuedict['id'] = olddict['id']
                return self.valuedict['id']
            else:
                #insert
                insertdict = self.valuedict.copy()
                if 'id' in insertdict:
                    del insertdict['id']
                stmt = insert(TablePage).values(insertdict)
                result = await self.dsconfig.asyncdb.async_execute(stmt)
                return result.lastrowid
        except Exception as exp:
            log.error('Exception at ApiPage.async_create_update_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None

    def delete_table(self):
        try:
            stmt = delete(TablePage).where(TablePage.id == self.id)
            result = self.dsconfig.db.execute(stmt)
            return result.rowcount
        except Exception as exp:
            log.error('Exception at ApiPage.delete_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    async def async_delete_table(self):
        try:
            stmt = delete(TablePage).where(TablePage.id == self.id)
            result = await self.dsconfig.asyncdb.async_execute(stmt)
            return result.rowcount
        except Exception as exp:
            log.error('Exception at ApiPage.async_delete_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


if __name__ == '__main__':
    pass
    #apitable = ApiTable(main.dsconfig,'None')
    #log.debug(apitable.get_all_tables())