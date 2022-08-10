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
import pickle
import traceback
import weakref

from sqlalchemy import inspect, Table

from apiconfig.config import config
from sqlalchemy.schema import MetaData,CreateTable

from apiconfig.dsconfig import dsconfig
from core.apiengine import apiengine
from core.apitable import ApiTable
from util import toolkit
from util.log import log as log

# cache file define
metadata_pickle_filename = dsconfig.Schema_Config.schema_cache_filename
cache_path = os.path.join(os.path.expanduser("~"), ".capricornus_cache")

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

class DBMeta(metaclass=Cached):
    def __init__(self, name):
        self.name = name
        self._useschema = dsconfig.Database_Config.db_useschema
        self._schema = dsconfig.Database_Config.db_schema
        self._tableCount = 0
        self._tables = 'N/A'
        self._viewCount = 0
        self._metadata = None
        self.load_metadata()
        if dsconfig.Application_Config.app_force_generate_meta:
            log.debug('Generate Schema file from database ...')
            self.gen_schema()
        else:
            if dsconfig.db_schema_existed:
                log.debug('Schema exists, now load it to application ...')
            else:
                log.debug('Schema does not exists, generate it from database ...')
                self.gen_schema()
        #self.load_schema()
        #self.gen_dbdirgramcanvas()
        #self.gen_ddl()

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value

    @property
    def tablecount(self):
        return self._tableCount

    @property
    def tables(self):
        return self._tables

    @property
    def viewcount(self):
        return self._viewCount

    @property
    def metadata(self):
        if self._metadata is not None:
            return self._metadata
        else:
            return None

    def load_metadata(self):
        engine = apiengine.connect()
        cached_metadata = None
        if dsconfig.Schema_Config.schema_cache_enabled == True:
            if os.path.exists(os.path.join(cache_path, metadata_pickle_filename)):
                try:
                    with open(os.path.join(cache_path, metadata_pickle_filename), 'rb') as cache_file:
                        cached_metadata = pickle.load(file=cache_file)
                        log.debug('Metadata cache exists, load meta from cache '
                                         'file [ %s ]' % os.path.join(cache_path, metadata_pickle_filename))
                except IOError:
                    # cache file not found - no problem, reflect as usual
                    log.debug('Metadata cache does not exists, will generate it from database ...')
            if cached_metadata:
                cached_metadata.bind = engine
                self._metadata = cached_metadata
            else:
                metadata = MetaData(bind=engine)
                if self._useschema:
                    metadata = MetaData(bind=engine, schema=self._schema)
                if dsconfig.Schema_Config.schema_fetch_all_table == True:
                    metadata.reflect(views=True)
                else:
                    metadata.reflect(views=True, only=toolkit.to_list(dsconfig.Schema_Config.schema_fetch_tables))
                self._metadata = metadata
                try:
                    if not os.path.exists(cache_path):
                        os.makedirs(cache_path)
                    with open(os.path.join(cache_path, metadata_pickle_filename), 'wb') as cache_file:
                        pickle.dump(self._metadata, cache_file)
                        log.debug('Metadata cache save to '
                                         '[ %s ] ' % os.path.join(cache_path, metadata_pickle_filename))
                except:
                    # couldn't write the file for some reason
                    log.debug('Metadata save Error '
                                     '[ %s ] ' % os.path.join(cache_path, metadata_pickle_filename))
        else:
            metadata = MetaData(bind=engine)
            if self._useschema:
                metadata = MetaData(bind=engine, schema=self._schema)
            if dsconfig.Schema_Config.schema_fetch_all_table == True:
                metadata.reflect(views=True)
            else:
                metadata.reflect(views=True, only=toolkit.to_list(dsconfig.Schema_Config.schema_fetch_tables))
            self._metadata = metadata

    def gen_schema(self):
        engine = apiengine.connect()
        inspector = inspect(engine)
        metadata = self.metadata
        try:
            if metadata is not None:
                log.debug("Generate Schema from : [ %s ] with db schema [ %s ]" % (dsconfig.Database_Config.db_uri, self._schema))
                jmeta = {}
                jmeta['Schema'] = dsconfig.Database_Config.db_schema
                jtbls = {}
                jmeta['Tables'] = jtbls
                table_list_set = set(toolkit.to_list(dsconfig.Schema_Config.schema_fetch_tables))
                # gen schema for tables
                table_names = inspector.get_table_names()
                if self._useschema:
                    table_names = inspector.get_table_names(schema=self._schema)
                for table_name in table_names:
                    persist_table = False
                    if dsconfig.Schema_Config.schema_fetch_all_table:
                        persist_table = True
                    else:
                        if table_name in table_list_set:
                            persist_table = True
                    if persist_table:
                        user_table = Table(table_name, metadata, autoload_with=engine)
                        cptypedict = {}
                        for c in user_table.columns:
                            if str(c.type) != 'NULL':
                                cptypedict[c.name] = c.type.python_type.__name__
                            else:
                                cptypedict[c.name] = 'str'
                        #cptypedict = dict([(c.name, c.type.python_type.__name__) for c in user_table.columns])
                        jtbl = {}
                        jtbls[table_name] = jtbl
                        jtbl['name'] = table_name
                        jtbl['dbconn_id'] = dsconfig.Database_Config.id
                        jtbl['table_schema'] = dsconfig.Database_Config.db_schema
                        jtbl['table_Type'] = 'table'
                        pk = inspector.get_pk_constraint(table_name)
                        if self._useschema:
                            pk = inspector.get_pk_constraint(table_name, schema=self._schema)
                        if len(pk['constrained_columns']) > 0:
                            jtbl['primarykeys'] = pk['constrained_columns']
                            jtbl['logicprimarykeys'] = pk['constrained_columns']
                        else:
                            jtbl['primarykeys'] = []
                            #lpk = self.get_table_logicprimarykeys(table_name)
                            lpk = None
                            jtbl['logicprimarykeys'] = [] if lpk is None else lpk
                        jtbl['indexes'] = inspector.get_indexes(table_name)
                        if self._useschema:
                            jtbl['indexes'] = inspector.get_indexes(table_name, schema=self._schema)
                        jtbl['columns'] = {}
                        jtbl['pagedefine'] = {}
                        table_columns = inspector.get_columns(table_name)
                        if self._useschema:
                            table_columns = inspector.get_columns(table_name, schema=self._schema)
                        for column in table_columns:
                            cdict={}
                            for key, value in column.items():
                                cdict[key] = value.__str__()
                            if column['name'] in jtbl['primarykeys']:
                                cdict['primary_key'] = 1
                            else:
                                cdict['primary_key'] = 0
                            cdict['pythonType'] = cptypedict[cdict['name']]
                            jtbl['columns'][cdict['name']] = cdict
                            jtbl['pagedefine'][cdict['name']] = cdict
                    log.debug('table schema is : %s' % jtbl)
                    japitable = ApiTable(jtbl['dbconn_id'], jtbl['name'])
                    japitable.loadfrom_json(jtbl)
                    japitable.create_table()
                # gen schema for views
                view_names = inspector.get_view_names()
                if self._useschema:
                    view_names = inspector.get_view_names(schema=self._schema)
                for view_name in view_names:
                    persist_view = False
                    if dsconfig.Schema_Config.schema_fetch_all_table:
                        persist_view = True
                    else:
                        if view_name in table_list_set:
                            persist_view = True
                    if persist_view:
                        user_view = Table(view_name, metadata, autoload_with=engine)
                        for c in user_table.columns:
                            if str(c.type) != 'NULL':
                                cptypedict[c.name] = c.type.python_type.__name__
                            else:
                                cptypedict[c.name] = 'str'
                        #cptypedict = dict([(c.name, c.type.python_type.__name__) for c in user_view.columns])
                        vtbl = {}
                        jtbls[view_name] = vtbl
                        vtbl['name'] = view_name
                        vtbl['dbconn_id'] = dsconfig.Database_Config.id
                        vtbl['table_schema'] = dsconfig.Database_Config.db_schema
                        vtbl['table_Type'] = 'view'
                        pk = inspector.get_pk_constraint(view_name)
                        if self._useschema:
                            pk = inspector.get_pk_constraint(view_name, schema=self._schema)
                        if len(pk['constrained_columns']) > 0:
                            vtbl['primarykeys'] = pk['constrained_columns']
                            vtbl['logicprimarykeys'] = pk['constrained_columns']
                        else:
                            vtbl['primarykeys'] = []
                            #lpk = self.get_table_logicprimarykeys(view_name)
                            vtbl['logicprimarykeys'] = [] if lpk is None else lpk
                        vtbl['indexes'] = inspector.get_indexes(view_name)
                        if self._useschema:
                            vtbl['indexes'] = inspector.get_indexes(view_name, schema=self._schema)
                        vtbl['columns'] = {}
                        vtbl['pagedefine'] = {}
                        view_columns = inspector.get_columns(view_name)
                        if self._useschema:
                            view_columns = inspector.get_columns(view_name, schema=self._schema)
                        for vcolumn in view_columns:
                            vdict = {}
                            for key, value in vcolumn.items():
                                vdict[key] = value.__str__()
                            if column['name'] in vtbl['primarykeys']:
                                vdict['primary_key'] = 1
                            else:
                                vdict['primary_key'] = 0
                            vdict['pythonType'] = cptypedict[vdict['name']]
                            vtbl['columns'][vdict['name']] = vdict
                            vtbl['pagedefine'][vdict['name']] = vdict
                    log.debug('view schema is : %s' % vtbl)
                    vapitable = ApiTable(vtbl['dbconn_id'], vtbl['name'])
                    vapitable.loadfrom_json(vtbl)
                    vapitable.create_table()
        except Exception as exp:
            log.error('Exception at dbmeta.gen_schema() %s ' % exp)
            if dsconfig.Application_Config.app_exception_detail:
                traceback.print_exc()

if __name__ == '__main__':
    dbmeta = DBMeta(config('app_profile', default='default-datasource'))
    '''
    tbl = dbmeta.gettable('Customers')
    log.debug(tbl.json)
    log.debug(dbmeta.get_table_primary_keys('Customers'))
    log.debug(dbmeta.get_table_pk_type('Customers','customer_id'))
    log.debug(dbmeta.get_table_pk_qmneed('Customers','customer_id'))
    log.debug(dbmeta.get_tables())
    log.debug(dbmeta.get_views())
    log.debug(dbmeta.response_schema())
    log.debug(dbmeta.check_table_schema('Brands'))
    log.debug(dbmeta.response_table_pagdef('Brands'))
'''
    #dbmeta.gen_models()
    #dbmeta.gen_udfmodels()
    #dbmeta.gen_services()
    #dbmeta.gen_udfservices()