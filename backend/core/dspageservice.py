#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

import traceback
import weakref

from sqlalchemy import select, insert, update, delete
import simplejson as json

from apps.admin.models.dspage import DatasourcePage
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

class DspageService(metaclass=Cached):
    def __init__(self, dsconfig, name):
        self.dsconfig = dsconfig
        self.meta_id = None
        self.meta_name = name
        self.ds_id = self.dsconfig.Database_Config.ds_id
        self.meta_schema = None
        self.meta_type = None
        self.meta_primarykeys = None
        self.meta_indexes = None
        self.meta_columns = None
        self.page_logicprimarykeys = None
        self.page_title = None
        self.page_list_display = None
        self.page_search_fields = None
        self.valuedict = None

    def loadfrom_json(self,jsonobj):
        if 'meta_id' in jsonobj:
            self.meta_id = jsonobj['meta_id']
        if 'meta_name' in jsonobj:
            self.meta_name = jsonobj['meta_name']
        if 'ds_id' in jsonobj:
            self.ds_id = jsonobj['ds_id']
        if 'meta_schema' in jsonobj:
            self.meta_schema = jsonobj['meta_schema']
        if 'meta_type' in jsonobj:
            self.meta_type = jsonobj['meta_type']
        if 'meta_primarykeys' in jsonobj:
            if isinstance(jsonobj['meta_primarykeys'],list):
                jsonobj['meta_primarykeys'] = ','.join(jsonobj['meta_primarykeys'])
            self.meta_primarykeys = jsonobj['meta_primarykeys']
        if 'meta_indexes' in jsonobj:
            if isinstance(jsonobj['meta_indexes'],list):
                jsonobj['meta_indexes'] = ','.join(jsonobj['meta_indexes'])
            self.meta_indexes = jsonobj['meta_indexes']
        if 'meta_columns' in jsonobj:
            self.meta_columns = jsonobj['meta_columns']
        if 'page_logicprimarykeys' in jsonobj:
            if isinstance(jsonobj['page_logicprimarykeys'],list):
                jsonobj['page_logicprimarykeys'] = ','.join(jsonobj['page_logicprimarykeys'])
            self.page_logicprimarykeys = jsonobj['page_logicprimarykeys']
        if 'page_title' in jsonobj:
            self.page_title = jsonobj['page_title']
        if 'page_list_display' in jsonobj:
            self.page_list_display = jsonobj['page_list_display']
        if 'page_search_fields' in jsonobj:
            self.page_search_fields = jsonobj['page_search_fields']
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
            log.error('Exception at DspageService.existed_table() %s ' % exp)
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
            log.error('Exception at DspageService.existed_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return False


    def query_table_byName(self):
        try:
            stmt = select(DatasourcePage).where(DatasourcePage.meta_name == self.meta_name, DatasourcePage.ds_id == self.ds_id)
            result = self.dsconfig.db.scalars(stmt).all()
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at DspageService.query_table_byName() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()


    async def async_query_table_byName(self):
        try:
            stmt = select(DatasourcePage).where(DatasourcePage.meta_name == self.meta_name, DatasourcePage.ds_id == self.ds_id)
            result = (await self.dsconfig.asyncdb.async_scalars(stmt)).all()
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at DspageService.async_query_table_byName() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


    def get_all_tables(self):
        try:
            stmt = select(DatasourcePage).where(DatasourcePage.ds_id == self.ds_id)
            result = self.dsconfig.db.scalars(stmt).all()
            return result
        except Exception as exp:
            log.error('Exception at DspageService.get_all_tables() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()


    async def async_get_all_tables(self):
        try:
            stmt = select(DatasourcePage).where(DatasourcePage.ds_id == self.ds_id)
            result = (await self.dsconfig.asyncdb.async_scalars(stmt)).all()
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at DspageService.async_get_all_tables() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


    def getall_table_Name(self):
        try:
            stmt = select(DatasourcePage).where(DatasourcePage.ds_id == self.ds_id)
            result = self.dsconfig.db.scalars(stmt).all()
            return result
        except Exception as exp:
            log.error('Exception at DspageService.getall_table_Name() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()


    async def async_getall_table_Name(self):
        try:
            stmt = select(DatasourcePage).where(DatasourcePage.ds_id == self.ds_id)
            #result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            result = (await self.dsconfig.asyncdb.async_scalars(stmt)).all()
            if len(result) > 0:
                resultlist = []
                for record in result:
                    resultlist.append(record.meta_name)
                return resultlist
            else:
                return None
        except Exception as exp:
            log.error('Exception at DspageService.async_getall_table_Name() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


    def create_table(self):
        try:
            insertdict = self.valuedict.copy()
            if 'meta_id' in insertdict:
                del insertdict['meta_id']
            stmt = insert(DatasourcePage).values(insertdict)
            result = self.dsconfig.db.execute(stmt)
            return result.lastrowid
        except Exception as exp:
            log.error('Exception at DspageService.create_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()


    async def async_create_table(self):
        try:
            insertdict = self.valuedict.copy()
            if 'meta_id' in insertdict:
                del insertdict['meta_id']
            stmt = insert(DatasourcePage).values(insertdict)
            result = await self.dsconfig.asyncdb.async_execute(stmt)
            return result.lastrowid
        except Exception as exp:
            log.error('Exception at DspageService.async_create_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


    def create_update_table(self):
        try:
            stmt = select(DatasourcePage).where(DatasourcePage.meta_name == self.meta_name, DatasourcePage.ds_id == self.ds_id)
            result = self.dsconfig.db.scalars(stmt).all()
            if len(result) > 0:
                # update ingore pagedef
                olddict = result[0].dict()
                updatedict = self.valuedict.copy()
                updatedict['page_title'] = olddict['page_title']
                self.valuedict['page_title'] = olddict['page_title']
                updatedict['page_logicprimarykeys'] = olddict['page_logicprimarykeys']
                self.valuedict['page_logicprimarykeys'] = olddict['page_logicprimarykeys']
                updatedict['page_list_display'] = olddict['page_list_display']
                self.valuedict['page_list_display'] = olddict['page_list_display']
                updatedict['page_search_fields'] = olddict['page_search_fields']
                self.valuedict['page_search_fields'] = olddict['page_search_fields']
                updatedict['meta_columns'] = toolkit.get_updated_colums(updatedict['meta_columns'],olddict['meta_columns'])
                self.valuedict['meta_columns'] = updatedict['meta_columns']
                stmt = update(DatasourcePage).where(DatasourcePage.meta_id == olddict['meta_id']).values(updatedict)
                result = self.dsconfig.db.execute(stmt)
                self.valuedict['meta_id'] = olddict['meta_id']
                return self.valuedict['meta_id']
            else:
                # insert
                insertdict = self.valuedict.copy()
                if 'meta_id' in insertdict:
                    del insertdict['meta_id']
                stmt = insert(DatasourcePage).values(insertdict)
                result = self.dsconfig.db.execute(stmt)
                return result.lastrowid
        except Exception as exp:
            log.error('Exception at DspageService.create_update_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()


    async def async_create_update_table(self):
        try:
            stmt = select(DatasourcePage).where(DatasourcePage.meta_name == self.meta_name, DatasourcePage.ds_id == self.ds_id)
            # result = await self.dsconfig.asyncdb.async_scalars_all(stmt)
            result = (await self.dsconfig.asyncdb.async_scalars(stmt)).all()
            if len(result) > 0:
                #update ingore pagedef
                olddict = result[0].dict()
                updatedict = self.valuedict.copy()
                updatedict['label'] = olddict['label']
                self.valuedict['label'] = olddict['label']
                stmt = update(DatasourcePage).where(DatasourcePage.meta_id == olddict['meta_id']).values(updatedict)
                result = await self.dsconfig.asyncdb.async_execute(stmt)
                self.valuedict['meta_id'] = olddict['meta_id']
                return self.valuedict['meta_id']
            else:
                #insert
                insertdict = self.valuedict.copy()
                if 'meta_id' in insertdict:
                    del insertdict['meta_id']
                stmt = insert(DatasourcePage).values(insertdict)
                result = await self.dsconfig.asyncdb.async_execute(stmt)
                return result.lastrowid
        except Exception as exp:
            log.error('Exception at DspageService.async_create_update_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


    def delete_table(self):
        try:
            stmt = delete(DatasourcePage).where(DatasourcePage.meta_id == self.meta_id)
            result = self.dsconfig.db.execute(stmt)
            return result.rowcount
        except Exception as exp:
            log.error('Exception at DspageService.delete_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()


    async def async_delete_table(self):
        try:
            stmt = delete(DatasourcePage).where(DatasourcePage.meta_id == self.meta_id)
            result = await self.dsconfig.asyncdb.async_execute(stmt)
            return result.rowcount
        except Exception as exp:
            log.error('Exception at DspageService.async_delete_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


if __name__ == '__main__':
    pass
    #apitable = DsmetaService(main.dsconfig,'None')
    #log.debug(apitable.get_all_tables())