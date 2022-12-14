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

from apps.admin.models.dsmeta import DatasourceMeta
from core.settings import settings
from utils.log import log as log
import six

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

class DsmetaService(metaclass=Cached):
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
                #log.debug(jsonobj['meta_indexes'])
                if len(jsonobj['meta_indexes']) > 0:
                    if isinstance(jsonobj['meta_indexes'][0], six.string_types):
                        jsonobj['meta_indexes'] = ','.join(jsonobj['meta_indexes'])
                    elif isinstance(jsonobj['meta_indexes'][0], dict):
                        idxcloumnlist = []
                        for idxdict in jsonobj['meta_indexes']:
                            idxcloumnlist.extend(idxdict['column_names'])
                        jsonobj['meta_indexes'] = ','.join(idxcloumnlist)
                    else:
                        jsonobj['meta_indexes'] = ''
                else:
                    jsonobj['meta_indexes'] = ''
            self.meta_indexes = jsonobj['meta_indexes']
        if 'meta_columns' in jsonobj:
            self.meta_columns = jsonobj['meta_columns']
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
            log.error('Exception at DsmetaService.existed_table() %s ' % exp)
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
            log.error('Exception at DsmetaService.existed_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return False


    def query_table_byName(self):
        try:
            stmt = select(DatasourceMeta).where(DatasourceMeta.meta_name == self.meta_name, DatasourceMeta.ds_id == self.ds_id)
            result = self.dsconfig.db.scalars(stmt).all()
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at DsmetaService.query_table_byName() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()


    async def async_query_table_byName(self):
        try:
            stmt = select(DatasourceMeta).where(DatasourceMeta.meta_name == self.meta_name, DatasourceMeta.ds_id == self.ds_id)
            result = (await self.dsconfig.asyncdb.async_scalars(stmt)).all()
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at DsmetaService.async_query_table_byName() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


    def get_all_tables(self):
        try:
            stmt = select(DatasourceMeta).where(DatasourceMeta.ds_id == self.ds_id)
            result = self.dsconfig.db.scalars(stmt).all()
            return result
        except Exception as exp:
            log.error('Exception at DsmetaService.get_all_tables() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()


    async def async_get_all_tables(self):
        try:
            stmt = select(DatasourceMeta).where(DatasourceMeta.ds_id == self.ds_id)
            result = (await self.dsconfig.asyncdb.async_scalars(stmt)).all()
            if len(result) > 0:
                return result
            else:
                return None
        except Exception as exp:
            log.error('Exception at DsmetaService.async_get_all_tables() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


    def getall_table_Name(self):
        try:
            stmt = select(DatasourceMeta).where(DatasourceMeta.ds_id == self.ds_id)
            result = self.dsconfig.db.scalars(stmt).all()
            return result
        except Exception as exp:
            log.error('Exception at DsmetaService.getall_table_Name() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()


    async def async_getall_table_Name(self):
        try:
            stmt = select(DatasourceMeta).where(DatasourceMeta.ds_id == self.ds_id)
            result = (await self.dsconfig.asyncdb.async_scalars(stmt)).all()
            if len(result) > 0:
                resultlist = []
                for record in result:
                    resultlist.append(record.meta_name)
                return resultlist
            else:
                return None
        except Exception as exp:
            log.error('Exception at DsmetaService.async_getall_table_Name() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None


    def create_table(self):
        try:
            insertdict = self.valuedict.copy()
            if 'meta_id' in insertdict:
                del insertdict['meta_id']
            stmt = insert(DatasourceMeta).values(insertdict)
            result = self.dsconfig.db.execute(stmt)
            self.dsconfig.db.commit()
            return result.lastrowid
        except Exception as exp:
            self.dsconfig.db.rollback()
            log.error('Exception at DsmetaService.create_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
        finally:
            self.dsconfig.db.close()


    async def async_create_table(self):
        try:
            insertdict = self.valuedict.copy()
            if 'meta_id' in insertdict:
                del insertdict['meta_id']
            stmt = insert(DatasourceMeta).values(insertdict)
            result = await self.dsconfig.asyncdb.async_execute(stmt)
            self.dsconfig.asyncdb.commit()
            return result.lastrowid
        except Exception as exp:
            self.dsconfig.asyncdb.rollback()
            log.error('Exception at DsmetaService.async_create_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None
        finally:
            self.dsconfig.asyncdb.close()


    def create_update_table(self):
        try:
            stmt = select(DatasourceMeta).where(DatasourceMeta.meta_name == self.meta_name, DatasourceMeta.ds_id == self.ds_id)
            result = self.dsconfig.db.scalars(stmt).all()
            if len(result) > 0:
                # update ingore pagedef
                olddict = result[0].dict()
                updatedict = self.valuedict.copy()
                stmt = update(DatasourceMeta).where(DatasourceMeta.meta_id == olddict['meta_id']).values(updatedict)
                result = self.dsconfig.db.execute(stmt)
                self.dsconfig.db.commit()
                self.valuedict['meta_id'] = olddict['meta_id']
                return self.valuedict['meta_id']
            else:
                # insert
                insertdict = self.valuedict.copy()
                if 'meta_id' in insertdict:
                    del insertdict['meta_id']
                stmt = insert(DatasourceMeta).values(insertdict)
                result = self.dsconfig.db.execute(stmt)
                self.dsconfig.db.commit()
                return result.lastrowid
        except Exception as exp:
            self.dsconfig.db.rollback()
            log.error('Exception at DsmetaService.create_update_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
        finally:
            self.dsconfig.db.close()


    async def async_create_update_table(self):
        try:
            stmt = select(DatasourceMeta).where(DatasourceMeta.meta_name == self.meta_name, DatasourceMeta.ds_id == self.ds_id)
            result = (await self.dsconfig.asyncdb.async_scalars(stmt)).all()
            if len(result) > 0:
                #update ingore pagedef
                olddict = result[0].dict()
                updatedict = self.valuedict.copy()
                stmt = update(DatasourceMeta).where(DatasourceMeta.meta_id == olddict['meta_id']).values(updatedict)
                result = await self.dsconfig.asyncdb.async_execute(stmt)
                self.dsconfig.asyncdb.commit()
                self.valuedict['meta_id'] = olddict['meta_id']
                return self.valuedict['meta_id']
            else:
                #insert
                insertdict = self.valuedict.copy()
                if 'meta_id' in insertdict:
                    del insertdict['meta_id']
                stmt = insert(DatasourceMeta).values(insertdict)
                result = await self.dsconfig.asyncdb.async_execute(stmt)
                self.dsconfig.asyncdb.commit()
                return result.lastrowid
        except Exception as exp:
            self.dsconfig.asyncdb.rollback()
            log.error('Exception at DsmetaService.async_create_update_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None
        finally:
            self.dsconfig.asyncdb.close()


    def delete_table(self):
        try:
            stmt = delete(DatasourceMeta).where(DatasourceMeta.meta_id == self.meta_id)
            result = self.dsconfig.db.execute(stmt)
            self.dsconfig.db.commit()
            return result.rowcount
        except Exception as exp:
            self.dsconfig.db.rollback()
            log.error('Exception at DsmetaService.delete_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
        finally:
            self.dsconfig.db.close()


    async def async_delete_table(self):
        try:
            stmt = delete(DatasourceMeta).where(DatasourceMeta.meta_id == self.meta_id)
            result = await self.dsconfig.asyncdb.async_execute(stmt)
            self.dsconfig.asyncdb.commit()
            return result.rowcount
        except Exception as exp:
            self.dsconfig.asyncdb.rollback()
            log.error('Exception at DsmetaService.async_delete_table() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()
            return None
        finally:
            self.dsconfig.asyncdb.close()


if __name__ == '__main__':
    pass
    #apitable = DsmetaService(main.dsconfig,'None')
    #log.debug(apitable.get_all_tables())