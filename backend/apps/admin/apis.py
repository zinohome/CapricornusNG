#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

from asgiref.sync import sync_to_async
from fastapi import APIRouter, Depends
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import create_async_engine
import traceback
import simplejson as json

from apps.admin.models.datasource import Datasource
from apps.admin.models.dsquerymodel import DSQueryModel
from apps.admin.models.dsurimodel import DSURIModel
from apps.admin.models.dspage import DatasourcePage
from core.dsengine import DSEngine
from core.dsconfig import DSConfig
from core.adminsite import site, auth
from core.dbmeta import DBMeta
from util.log import log as log
from core import i18n as _

router = APIRouter(prefix='/admin', tags=['admin'], dependencies=[Depends(auth.requires()())])

@router.get('/get_column_options/{meta_id}',
         tags=["admin"],
         summary="Get column options list.",
         description="Return column options list",
         include_in_schema=False)
async def get_column_options(meta_id: int):
    try:
        returndict = {'status':1,'msg':_("Get column options Error")}
        result = await site.db.async_get(DatasourcePage, meta_id)
        if result.meta_columns:
            clsname = result.meta_name.strip().capitalize()
            datalist = []
            for column in result.meta_columns:
                datalist.append({'label':column['name'],'value':clsname + '.' + column['name']})
            returndict['status'] = 0
            returndict['msg'] = 'Success'
            returndict['data'] = datalist
        return returndict
    except Exception as e:
        log.error('Get column options Error !')
        traceback.print_exc()
        return returndict

@router.get('/get_ds_select_options',
         tags=["admin"],
         summary="Get datasource select options list.",
         description="Return datasource select options list",
         include_in_schema=False)
async def get_ds_select_options():
    try:
        returndict = {'status':1,'msg':_("Get datasource select options Error")}
        stmt = select(Datasource)
        result = await site.db.async_scalars_all(stmt)
        if len(result) > 0:
            datalist = []
            for ds in result:
                datalist.append({'label':ds.ds_name,'value':ds.ds_uri,'uri':ds.ds_uri})
            returndict['status'] = 0
            returndict['msg'] = 'Success'
            returndict['data'] = datalist
        return returndict
    except Exception as e:
        log.error('Get datasource select options Error !')
        traceback.print_exc()
        return returndict

@router.post('/db_connection_test',
         tags=["admin"],
         summary="Test database connection.",
         description="Return database connection test result",
         include_in_schema=False)
async def db_connection_test(ds_uri: DSURIModel) -> str:
    log.debug('Try to test db connection with dburi : %s' % ds_uri.ds_uri)
    try:
        engine = create_async_engine(ds_uri.ds_uri,echo=False,pool_pre_ping=True)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            #log.debug('Test excute result: %s' % result.fetchall())
            #log.debug('Database Connected !')
            await engine.dispose()
            return {"status":0,"msg":_("DataBase Connected")}
    except Exception as e:
        log.error('Database Test Connected Error !')
        traceback.print_exc()
        return {"status":1,"msg":_("DataBase Connect Error")}

@router.post('/sql_query',
         tags=["admin"],
         summary="SQL Query.",
         description="Return SQL query result",
         include_in_schema=False)
async def sql_query(dsquery: DSQueryModel) -> str:
    try:
        if len(dsquery.ds_uri)>0:
            log.debug('Try to sql query with dburi : %s' % dsquery.ds_uri)
            engine = create_async_engine(dsquery.ds_uri,echo=False,pool_pre_ping=True)
            async with engine.connect() as conn:
                result = await conn.execute(text(dsquery.query_sql))
                rows = result.fetchall()
                columnslist = []
                for key in result.keys():
                    columnslist.append({'label':key,'name':key})
                items = [{**row}for row in rows]
                await engine.dispose()
                returnobj = {"status":0,"msg":_("SQL query complete"),"data":{"rows":items,"columns":columnslist}}
                #log.debug(returnobj)
                return returnobj
        else:
            return {"status":0,"msg":_("SQL query complete"),"data":{"rows":[]}}
    except Exception as e:
        log.error('SQL query Error !')
        traceback.print_exc()
        return {"status":1,"msg":_("SQL query Error")}

@router.post('/db_sync_schema',
         tags=["admin"],
         summary="Synchronize database schema.",
         description="Synchronize database schema",
         include_in_schema=False)
async def db_sync_schema(datasource: Datasource) -> str:
    log.debug('Try to synchronize database schema dburi : %s' % datasource.ds_uri)
    log.debug('Database Connection infomation is : %s' % datasource.json())
    try:
        sycdsconfig = DSConfig(datasource.ds_name)
        syncapiengine = DSEngine(sycdsconfig)
        dbmeta = await sync_to_async(func=DBMeta)(sycdsconfig, syncapiengine)
        log.debug('[Step 0/8] Meta synchronize initialized')
        await sync_to_async(func=dbmeta.load_metadata)()
        log.debug('[Step 1/8] Metadata loaded')
        await sync_to_async(func=dbmeta.gen_schema)()
        log.debug('[Step 2/8] Schema generated')
        await sync_to_async(func=dbmeta.load_schema)()
        log.debug('[Step 3/8] Schema loaded')
        await sync_to_async(func=dbmeta.gen_dbdirgramcanvas)()
        log.debug('[Step 4/8] DB Dirgramcanvas generated')
        await sync_to_async(func=dbmeta.gen_ddl)()
        log.debug('[Step 5/8] DDL generated')
        await sync_to_async(func=dbmeta.gen_models)()
        log.debug('[Step 6/8] DataModels generated')
        await sync_to_async(func=dbmeta.gen_admins)()
        log.debug('[Step 7/8] DataPages generated')
        log.debug('[Step 8/8] Service reloaded')
        return {"status":0,"msg":_("DataBase synchronized")}
    except Exception as e:
        traceback.print_exc()
        return {"status":1,"msg":_("DataBase synchronized Error")}
