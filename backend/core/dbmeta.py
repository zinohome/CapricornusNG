#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

import base64
import os
import pickle
import traceback
import uuid
import weakref

from jinja2 import Environment, FileSystemLoader
from sqlalchemy import inspect, Table

from core.dspageservice import DspageService
from core.settings import settings
from sqlalchemy.schema import MetaData,CreateTable
import simplejson as json

from core.dsengine import DSEngine
from core.dsmetaservice import DsmetaService
from core.dsconfig import DSConfig
from core.pageschema import PageSchema
from core.metaschema import MetaSchema
from util import toolkit
from util.log import log as log

# cache file define
cache_path = os.path.join(os.path.expanduser("~"), ".capricornus_cache")
InternalObjEnum = {
        'sqlite':['sqlite_master','sqlite_sequence','sqlite_stat1','sqlite_stat3','sqlite_stat4','sqlite_dbdata'],
        'mysql':['sqlite_master','sqlite_sequence','sqlite_stat1','sqlite_stat3','sqlite_stat4','sqlite_dbdata'],
        'postgresql':['sqlite_master','sqlite_sequence','sqlite_stat1','sqlite_stat3','sqlite_stat4','sqlite_dbdata'],
        'oracle':['sqlite_master','sqlite_sequence','sqlite_stat1','sqlite_stat3','sqlite_stat4','sqlite_dbdata']
                       }
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
    def __init__(self, dsconfig, dsengine):
        self.dsconfig = dsconfig
        self.dsengine = dsengine
        self.ds_name = dsconfig.Database_Config.ds_name
        self._useschema = self.dsconfig.Database_Config.ds_useschema
        self._schema = self.dsconfig.Database_Config.ds_schema
        self._tableCount = 0
        self._tables = None
        self._pages = None
        self._viewCount = 0
        self._metadata = None

        '''
        self.load_metadata()
        if self.dsconfig.Application_Config.app_force_generate_meta:
            log.debug('Generate Schema file from database ...')
            self.gen_schema()
        else:
            if self.dsconfig.db_schema_existed:
                log.debug('Schema exists, now load it to application ...')
            else:
                log.debug('Schema does not exists, generate it from database ...')
                self.gen_schema()
        self.load_schema()
        self.gen_dbdirgramcanvas()
        self.gen_ddl()
        '''

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
    def pages(self):
        return self._pages

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
        engine = self.dsengine.connect()
        cached_metadata = None
        metadata_pickle_filename = self.dsconfig.Schema_Config.schema_cache_filename
        if self.dsconfig.Schema_Config.schema_cache_enabled == True:
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
                if self.dsconfig.Schema_Config.schema_fetch_all_table == True:
                    metadata.reflect(views=True)
                else:
                    metadata.reflect(views=True, only=toolkit.to_list(self.dsconfig.Schema_Config.schema_fetch_tables))
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
            if self.dsconfig.Schema_Config.schema_fetch_all_table == True:
                metadata.reflect(views=True)
            else:
                metadata.reflect(views=True, only=toolkit.to_list(self.dsconfig.Schema_Config.schema_fetch_tables))
            self._metadata = metadata

    def gen_schema(self):
        engine = self.dsengine.connect()
        inspector = inspect(engine)
        metadata = self.metadata
        try:
            if metadata is not None:
                log.debug("Generate Schema from : [ %s ] with db schema [ %s ]" % (self.dsconfig.Database_Config.ds_uri, self._schema))
                jmeta = {}
                jmeta['Schema'] = self.dsconfig.Database_Config.ds_schema
                jtbls = {}
                jmeta['Tables'] = jtbls
                table_list_set = set(toolkit.to_list(self.dsconfig.Schema_Config.schema_fetch_tables))
                # gen schema for tables
                table_names = inspector.get_table_names()
                if self._useschema:
                    table_names = inspector.get_table_names(schema=self._schema)
                for table_name in table_names:
                    persist_table = False
                    if not table_name in InternalObjEnum[toolkit.get_db_type_from_uri(self.dsconfig.Database_Config.ds_uri)]:
                        if self.dsconfig.Schema_Config.schema_fetch_all_table:
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
                        jtbl['meta_name'] = table_name
                        jtbl['ds_id'] = self.dsconfig.Database_Config.ds_id
                        jtbl['meta_schema'] = self.dsconfig.Database_Config.ds_schema
                        jtbl['meta_type'] = 'table'
                        pk = inspector.get_pk_constraint(table_name)
                        if self._useschema:
                            pk = inspector.get_pk_constraint(table_name, schema=self._schema)
                        if len(pk['constrained_columns']) > 0:
                            jtbl['meta_primarykeys'] = pk['constrained_columns']
                            jtbl['page_logicprimarykeys'] = pk['constrained_columns']
                        else:
                            jtbl['meta_primarykeys'] = []
                            lpk = self.get_table_logicprimarykeys(table_name)
                            jtbl['page_logicprimarykeys'] = [] if lpk is None else lpk
                        jtbl['meta_indexes'] = inspector.get_indexes(table_name)
                        if self._useschema:
                            jtbl['meta_indexes'] = inspector.get_indexes(table_name, schema=self._schema)
                        jtbl['meta_columns'] = []
                        table_columns = inspector.get_columns(table_name)
                        if self._useschema:
                            table_columns = inspector.get_columns(table_name, schema=self._schema)
                        for column in table_columns:
                            cdict={}
                            for key, value in column.items():
                                cdict[key] = value.__str__()
                            if column['name'] in jtbl['meta_primarykeys']:
                                cdict['primary_key'] = 1
                            else:
                                cdict['primary_key'] = 0
                            cdict['pythonType'] = cptypedict[cdict['name']]
                            jtbl['meta_columns'].append(cdict)
                        log.debug('Extracting table schema for : %s ……' % jtbl['meta_name'])
                        ptbl = jtbl.copy()
                        del jtbl['page_logicprimarykeys']
                        jdsmetasvc = DsmetaService(self.dsconfig, jtbl['meta_name'])
                        jdsmetasvc.loadfrom_json(jtbl)
                        jdsmetasvc.create_update_table()
                        ptbl['page_title'] = ptbl['meta_name']
                        ptbl['page_list_display'] = ''
                        ptbl['page_search_fields'] = ''
                        for item in ptbl['meta_columns']:
                            item['title'] = item['name']
                            item['amis_form_item'] = ''
                            item['amis_table_column'] = ''
                        dspagesvc = DspageService(self.dsconfig, ptbl['meta_name'])
                        dspagesvc.loadfrom_json(ptbl)
                        dspagesvc.create_update_table()
                # gen schema for views
                view_names = inspector.get_view_names()
                if self._useschema:
                    view_names = inspector.get_view_names(schema=self._schema)
                for view_name in view_names:
                    persist_view = False
                    if not view_name in InternalObjEnum[toolkit.get_db_type_from_uri(self.dsconfig.Database_Config.ds_uri)]:
                        if self.dsconfig.Schema_Config.schema_fetch_all_table:
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
                        vtbl['meta_name'] = view_name
                        vtbl['ds_id'] = self.dsconfig.Database_Config.ds_id
                        vtbl['meta_schema'] = self.dsconfig.Database_Config.ds_schema
                        vtbl['meta_type'] = 'view'
                        pk = inspector.get_pk_constraint(view_name)
                        if self._useschema:
                            pk = inspector.get_pk_constraint(view_name, schema=self._schema)
                        if len(pk['constrained_columns']) > 0:
                            vtbl['meta_primarykeys'] = pk['constrained_columns']
                            vtbl['page_logicprimarykeys'] = pk['constrained_columns']
                        else:
                            vtbl['meta_primarykeys'] = []
                            lpk = self.get_table_logicprimarykeys(view_name)
                            vtbl['page_logicprimarykeys'] = [] if lpk is None else lpk
                        vtbl['meta_indexes'] = inspector.get_indexes(view_name)
                        if self._useschema:
                            vtbl['meta_indexes'] = inspector.get_indexes(view_name, schema=self._schema)
                        vtbl['meta_columns'] = []
                        view_columns = inspector.get_columns(view_name)
                        if self._useschema:
                            view_columns = inspector.get_columns(view_name, schema=self._schema)
                        for vcolumn in view_columns:
                            vdict = {}
                            for key, value in vcolumn.items():
                                vdict[key] = value.__str__()
                            if column['meta_name'] in vtbl['meta_primarykeys']:
                                vdict['primary_key'] = 1
                            else:
                                vdict['primary_key'] = 0
                            vdict['pythonType'] = cptypedict[vdict['name']]
                            vtbl['meta_columns'].append(vdict)
                        log.debug('Extracting view schema for : %s ……' % vtbl['meta_name'])
                        ptbl = vtbl.copy()
                        del vtbl['page_logicprimarykeys']
                        vdsmetasvc = DsmetaService(self.dsconfig, vtbl['meta_name'])
                        vdsmetasvc.loadfrom_json(vtbl)
                        vdsmetasvc.create_update_table()
                        ptbl['page_title'] = ptbl['meta_name']
                        ptbl['page_list_display'] = ''
                        ptbl['page_search_fields'] = ''
                        for item in ptbl['meta_columns']:
                            item['title'] = item['name']
                            item['amis_form_item'] = ''
                            item['amis_table_column'] = ''
                        dspagesvc = DspageService(self.dsconfig, ptbl['meta_name'])
                        dspagesvc.loadfrom_json(ptbl)
                        dspagesvc.create_update_table()
        except Exception as exp:
            log.error('Exception at dbmeta.gen_schema() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    def load_schema(self):
        log.debug('Loading schema from %s ……' % settings.app_profile)
        apitable = DsmetaService(self.dsconfig, 'None')
        metas = apitable.get_all_tables()
        apipage = DspageService(self.dsconfig, 'None')
        pages = apipage.get_all_tables()
        self._tables = []
        self._pages = []
        for meta in metas:
            table = MetaSchema(meta.meta_id, meta.meta_name, meta.meta_type)
            table.ds_id = meta.ds_id
            table.meta_schema = meta.meta_schema
            table.meta_primarykeys = meta.meta_primarykeys
            table.meta_indexes = meta.meta_indexes
            table.meta_columns = meta.meta_columns
            self._tables.append(table)
            if table.meta_type == 'table':
                self._tableCount = self._tableCount + 1
            if table.meta_type == 'view':
                self._viewCount = self._viewCount + 1
        for page in pages:
            tpage = PageSchema(page.meta_id, page.meta_name, page.meta_type)
            tpage.ds_id = page.ds_id
            tpage.page_title = page.page_title
            tpage.meta_schema = page.meta_schema
            tpage.meta_primarykeys = page.meta_primarykeys
            tpage.page_logicprimarykeys = page.page_logicprimarykeys
            tpage.meta_indexes = page.meta_indexes
            tpage.page_list_display = page.page_list_display
            tpage.page_search_fields = page.page_search_fields
            tpage.meta_columns = page.meta_columns
            self._pages.append(tpage)
        log.debug('Schema load with [ %s ] tables and [ %s ] views' % (self._tableCount, self._viewCount))


    def gettable(self, value):
        if len(self._tables) > 0:
            for table in self._tables:
                if table.meta_name == value:
                    return table
        else:
            return None

    def getpage(self, value):
        if len(self._pages) > 0:
            for page in self._pages:
                if page.meta_name == value:
                    return page
        else:
            return None

    def get_table_primary_keys(self, value):
        table = self.gettable(value)
        if table is not None:
            pks = table.primarykeys
            return pks
        else:
            return None

    def get_table_logicprimarykeys(self, table_name):
        dspagesvc = DspageService(self.dsconfig, table_name)
        tablemetas = dspagesvc.query_table_byName()
        if tablemetas is not None:
            return tablemetas[0].page_logicprimarykeys
        else:
            return None

    def table_has_null_type_column(self, table_name):
        rtn = False
        table = self.gettable(table_name)
        if table is not None:
            for column in table.meta_columns:
                if column['type'] == 'NULL':
                    rtn = True
                    break
        else:
            rtn = True
        return rtn

    def get_table_pk_type(self,tablename,pkname):
        pk_type = 'VARCHAR'
        table = self.gettable(tablename)
        pk_type = table.getColumnType(pkname)
        return pk_type

    def get_table_pk_qmneed(self, tablename, pkname):
        pk_qmneed = False
        pk_type = self.get_table_pk_type(tablename, pkname)
        if pk_type in ['CHAR', 'VARCHAR', 'TEXT', 'DATE', 'DATETIME', 'TIMESTAMP', 'YEAR', 'TIME']:
            pk_qmneed = True
        return pk_qmneed

    def get_tables(self):
        tblist = []
        for tb in self._tables:
            if tb.meta_type == 'table':
                tblist.append(tb.meta_name)
        return tblist

    def get_views(self):
        viewlist = []
        for tb in self._tables:
            if tb.meta_type == 'view':
                viewlist.append(tb.meta_name)
        return viewlist

    def get_table_pages(self):
        tplist = []
        for pg in self._pages:
                tplist.append(pg.meta_name)
        return tplist

    def response_schema(self):
        tblist = []
        for tb in self._tables:
            tblist.append(tb.meta_name)
        return tblist

    def gen_dbdirgram(self):
        try:
            basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
            apppath = os.path.abspath(os.path.join(basepath, os.pardir))
            configpath = os.path.abspath(os.path.join(apppath, 'appconfig'))
            canvasfilepath = os.path.abspath(os.path.join(configpath, "dbdiagram-canvas.json"))
            diagramfilepath = os.path.abspath(os.path.join(configpath, "dbdiagram.json"))
            dbdiagram = {}
            canvas = {}
            with open(canvasfilepath, 'r') as canvasfile:
                canvas = json.loads(canvasfile.read())
            canvas['databaseName'] = self.dsconfig.Database_Config.ds_name
            dbdiagram['canvas'] = canvas
            tables = self.get_tables()
            tbllist = []
            for tbl in tables:
                dgtable = self.gettable(tbl)
                ndgtable = {}
                ndgtable['name'] = dgtable.meta_name
                ndgtable['comment'] = ''
                ndgtable['id'] = str(uuid.uuid1())
                ndgtable['ui'] = {'active': True, 'left': 50, 'top': 50, 'zIndex': 1, 'widthName': 60,
                                  'widthComment': 60}
                ndgcolume = {}
                pks = dgtable.meta_primarykeys
                clmlist = []
                for clm in dgtable.meta_columns:
                    ndgcolume = {}
                    ndgcolume['id'] = str(uuid.uuid1())
                    ndgcolume['name'] = clm['name']
                    # ndgcolume['comment'] = '' if clm['comment'] == 'None' else clm['comment']
                    ndgcolume['dataType'] = clm['type']
                    ndgcolume['default'] = '' if clm['default'] == 'None' else clm['default']
                    ndgcolume['option'] = {"autoIncrement": False, "primaryKey": False, "unique": False,
                                           "notNull": False}
                    ndgcolume['ui'] = {"active": False, "pk": False, "fk": False, "pfk": False, "widthName": 60,
                                       "widthComment": 60, "widthDataType": 60, "widthDefault": 60}
                    if clm.__contains__('nullable'):
                        ndgcolume['option']['notNull'] = 'true' if clm['nullable'] == 'False' else 'false'
                    if clm.__contains__('autoincrement'):
                        ndgcolume['option']['autoIncrement'] = clm['autoincrement']
                    if clm['name'] in pks:
                        ndgcolume['option']['primaryKey'] = True
                        ndgcolume['ui']['pk'] = True
                    clmlist.append(ndgcolume)
                ndgtable['columns'] = clmlist
                tbllist.append(ndgtable)
            dbdiagramtable = {}
            dbdiagramtable['tables'] = tbllist
            dbdiagram['table'] = dbdiagramtable
            # log.debug(dbdiagram)
            with open(diagramfilepath, 'w', encoding='utf-8') as diagramfile:
                json.dump(dbdiagram, diagramfile, separators=(',', ':'),
                          sort_keys=False, indent=4, ensure_ascii=False, encoding='utf-8')
        except Exception as exp:
            log.error('Exception at dbmeta.gen_dbdirgram() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    def gen_dbdirgramcanvas(self):
        try:
            log.debug("Generate DB Dirgram Canvas from : [ %s ] with db schema "
                      "[ %s ]" % (self.dsconfig.Database_Config.ds_name, self._schema))
            basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
            apppath = os.path.abspath(os.path.join(basepath, os.pardir))
            configpath = os.path.abspath(os.path.join(apppath, 'appconfig'))
            canvasfilepath = os.path.abspath(os.path.join(configpath, "dbdiagram-canvas.json"))
            diagramfilepath = os.path.abspath(os.path.join(configpath, "dbdiagram.json"))
            dbdiagram = {}
            canvas = {}
            with open(canvasfilepath, 'r') as canvasfile:
                canvas = json.loads(canvasfile.read())
            canvas['databaseName'] = self.dsconfig.Database_Config.ds_name
            dbdiagram['canvas'] = canvas
            # log.debug(dbdiagram)
            with open(diagramfilepath, 'w', encoding='utf-8') as diagramfile:
                json.dump(dbdiagram, diagramfile, separators=(',', ':'),
                          sort_keys=False, indent=4, ensure_ascii=False, encoding='utf-8')
        except Exception as exp:
            log.error('Exception at dbmeta.gen_dbdirgramcanvas() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    def gen_ddl(self):
        basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        apppath = os.path.abspath(os.path.join(basepath, os.pardir))
        configpath = os.path.abspath(os.path.join(apppath, 'appconfig'))
        ddlfilepath = os.path.abspath(os.path.join(configpath, "dbddl.sql"))
        engine = self.dsengine.connect()
        inspector = inspect(engine)
        metadata = self.metadata
        ddlstr = ''
        try:
            if metadata is not None:
                log.debug("Generate DLL from : [ %s ] with db schema "
                          "[ %s ]" % (self.dsconfig.Database_Config.ds_name, self._schema))
                table_list_set = set(toolkit.to_list(self.dsconfig.Schema_Config.schema_fetch_tables))
                table_names = inspector.get_table_names()
                if self._useschema:
                    table_names = inspector.get_table_names(schema=self._schema)
                for table_name in table_names:
                    persist_table = False
                    if not table_name in InternalObjEnum[toolkit.get_db_type_from_uri(self.dsconfig.Database_Config.ds_uri)]:
                        if self.dsconfig.Schema_Config.schema_fetch_all_table:
                            persist_table = True
                        else:
                            if table_name in table_list_set:
                                persist_table = True
                    if self.table_has_null_type_column(table_name):
                        persist_table = False
                    if persist_table:
                        user_table = Table(table_name, metadata, autoload_with=engine)
                        tblcrtstr = str(CreateTable(user_table).compile(engine))
                        if not self._schema is None:
                            tblcrtstr = tblcrtstr.replace(' ' + self._schema + '.', ' ')
                        tblcrtstr = tblcrtstr.replace(' ' + table_name + ' ', ' `' + table_name + '` ')
                        table_columns = inspector.get_columns(table_name)
                        if self._useschema:
                            table_columns = inspector.get_columns(table_name, schema=self._schema)
                        for column in table_columns:
                            tblcrtstr = tblcrtstr.replace('\t' + column['name'] + ' ', '\t`' + column['name'] + '` ')
                            tblcrtstr = tblcrtstr.replace('(' + column['name'] + ')', ' `(' + column['name'] + '`) ')
                        # log.debug(tblcrtstr)
                        ddlstr = ddlstr + tblcrtstr
                view_names = inspector.get_view_names()
                if self._useschema:
                    view_names = inspector.get_view_names(schema=self._schema)
                for view_name in view_names:
                    persist_view = False
                    if not view_name in InternalObjEnum[toolkit.get_db_type_from_uri(self.dsconfig.Database_Config.ds_uri)]:
                        if self.dsconfig.Schema_Config.schema_fetch_all_table:
                            persist_view = True
                        else:
                            if view_name in table_list_set:
                                persist_view = True
                    if persist_view:
                        user_view = Table(view_name, metadata, autoload_with=engine)
                        viewcrtstr = str(CreateTable(user_view).compile(engine))
                        if not self._schema is None:
                            viewcrtstr = viewcrtstr.replace(' ' + self._schema + '.', ' ')
                        viewcrtstr = viewcrtstr.replace(' ' + view_name + ' ', ' `' + view_name + '` ')
                        view_columns = inspector.get_columns(view_name)
                        if self._useschema:
                            view_columns = inspector.get_columns(view_name, schema=self._schema)
                        for vcolumn in view_columns:
                            viewcrtstr = viewcrtstr.replace('\t' + vcolumn['name'] + ' ',
                                                            '\t`' + vcolumn['name'] + '` ')
                            viewcrtstr = viewcrtstr.replace('(' + vcolumn['name'] + ')',
                                                            ' `(' + vcolumn['name'] + '`) ')
                        # log.debug(viewcrtstr)
                        ddlstr = ddlstr + viewcrtstr
                # log.debug(ddlstr)
                with open(ddlfilepath, 'w', encoding='utf-8') as ddlfile:
                    ddlfile.write(ddlstr)
                    ddlfile.close()
            else:
                log.error('Can not get metadata at gen_ddl() ... ')
                raise Exception('Can not get metadata at gen_ddl()')
        except Exception as exp:
            log.error('Exception at dbmeta.gen_ddl() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    def gen_models(self):
        basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        apppath = os.path.abspath(os.path.join(basepath, os.pardir))
        tmplpath = os.path.abspath(os.path.join(apppath, 'tmpl'))
        modelspath = os.path.abspath(os.path.join(apppath, 'apps/dmodels'))
        try:
            tbls = self.get_table_pages()
            for tbl in tbls:
                dtable = self.getpage(tbl)
                log.debug("Generate model for table: %s" % dtable.meta_name)
                env = Environment(loader=FileSystemLoader(tmplpath), trim_blocks=True, lstrip_blocks=True)
                template = env.get_template('sqlmodel_tmpl.py')
                gencode = template.render(dtable.json)
                #log.debug(gencode)
                modelsfilepath = os.path.abspath(os.path.join(modelspath, tbl.lower() + ".py"))
                with open(modelsfilepath, 'w', encoding='utf-8') as gencodefile:
                    gencodefile.write(gencode)
                    gencodefile.close()
        except Exception as exp:
            log.error('Exception at gen_models() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    def gen_admins(self):
        basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        apppath = os.path.abspath(os.path.join(basepath, os.pardir))
        tmplpath = os.path.abspath(os.path.join(apppath, 'tmpl'))
        servicespath = os.path.abspath(os.path.join(apppath, 'apps/dadmins'))
        try:
            tbls = self.get_table_pages()
            for tbl in tbls:
                dtable = self.getpage(tbl)
                log.debug("Generate service for table: %s" % dtable.meta_name)
                env = Environment(loader=FileSystemLoader(tmplpath), trim_blocks=True, lstrip_blocks=True)
                template = env.get_template('modeladmin_tmpl.py')
                gencode = template.render(dtable.json)
                #log.debug(gencode)
                modelsfilepath = os.path.abspath(os.path.join(servicespath, tbl.lower() + "admin.py"))
                with open(modelsfilepath, 'w', encoding='utf-8') as gencodefile:
                    gencodefile.write(gencode)
                    gencodefile.close()
        except Exception as exp:
            log.error('Exception at gen_admins() %s ' % exp)
            if settings.app_exception_detail:
                traceback.print_exc()

    def response_dbdiagram(self, filename, canvasonly=False):
        basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        apppath = os.path.abspath(os.path.join(basepath, os.pardir))
        configpath = os.path.abspath(os.path.join(apppath, 'config'))
        diagramfilepath = os.path.abspath(os.path.join(configpath, filename))
        rjson = {"name":filename,
                 "type": "file",
                 "content": ""}
        with open(diagramfilepath, 'r') as diagramfile:
            rjson['content'] = base64.b64encode(diagramfile.read().encode('utf-8'))
        return rjson

    def response_table_schema(self, value):
        tb = self.gettable(value)
        if tb is not None:
            return tb.json
        else:
            return {}

    def check_table_schema(self, value):
        tb = self.gettable(value)
        if tb is not None:
            return True
        else:
            return False


if __name__ == '__main__':

    dsconfig = DSConfig(settings.app_profile)
    dsengine = DSEngine(dsconfig)
    dbmeta = DBMeta(dsconfig, dsengine)
    dbmeta.load_metadata()
    dbmeta.gen_schema()
    '''
    dbmeta.load_schema()
    dbmeta.gen_dbdirgram()
    dbmeta.gen_dbdirgramcanvas()
    dbmeta.gen_ddl()
    dbmeta.gen_models()
    dbmeta.gen_admins()
    
    
    #
    tbl = dbmeta.gettable('Customers')
    log.debug(tbl.json)
    log.debug(dbmeta.get_table_primary_keys('Customers'))
    log.debug(dbmeta.get_table_pk_type('Customers','customer_id'))
    log.debug(dbmeta.get_table_pk_qmneed('Customers','customer_id'))
    log.debug(dbmeta.get_tables())
    log.debug(dbmeta.get_views())
    log.debug(dbmeta.response_schema())
    log.debug(dbmeta.check_table_schema('Brands'))
'''

    #log.debug(dbmeta.response_table_pagdef('Brands'))

    #dbmeta.gen_models()
    #dbmeta.gen_udfmodels()
    #dbmeta.gen_services()
    #dbmeta.gen_udfservices()
