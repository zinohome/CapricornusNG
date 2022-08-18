from asgiref.sync import sync_to_async
from fastapi import APIRouter, Depends
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import create_async_engine
import traceback

from apps.admin.models.dbconnection import DBConnection
from apps.admin.models.dburimodel import DBURIModel
from apps.admin.models.tablepage import TablePage
from core.apiengine import APIEngine
from core.dsconfig import DSConfig
from core.adminsite import site, auth
from core.dbmeta import DBMeta
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _

router = APIRouter(prefix='/admin', tags=['admin'], dependencies=[Depends(auth.requires()())])

@router.get('/get_column_options/{page_id}',
         tags=["admin"],
         summary="Get column options list.",
         description="Return column options list",
         include_in_schema=True)
async def get_column_options(page_id: int):
    try:
        returndict = {'status':1,'msg':_("Get column options Error")}
        result = await site.db.async_get(TablePage, page_id)
        if result.columns:
            clsname = result.name.strip().capitalize()
            datalist = []
            for column in result.columns:
                datalist.append({'label':column['name'],'value':clsname + '.' + column['name']})
            returndict['status'] = 0
            returndict['msg'] = 'Success'
            returndict['data'] = datalist
        return returndict
            
    except Exception as e:
        log.error('Get column options Error !')
        traceback.print_exc()
        return {"status": 1, "msg": _("Get column options Error")}

@router.post('/db_connection_test',
         tags=["admin"],
         summary="Test database connection.",
         description="Return database connection test result",
         include_in_schema=True)
async def db_connection_test(dburi: DBURIModel) -> str:
    log.debug('Try to test db connection with dburi : %s' % dburi.db_uri)
    engine = create_async_engine(dburi.db_uri,echo=False,pool_pre_ping=True)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            log.debug('Test excute result: %s' % result.fetchall())
            log.debug('Database Connected !')
            return {"status":0,"msg":_("DataBase Connected")}
    except Exception as e:
        log.error('Database Test Connected Error !')
        traceback.print_exc()
        return {"status":1,"msg":_("DataBase Connect Error")}

@router.post('/db_sync_schema',
         tags=["admin"],
         summary="Synchronize database schema.",
         description="Synchronize database schema",
         include_in_schema=True)
async def db_sync_schema(dbconnection: DBConnection) -> str:
    log.debug('Try to synchronize database schema dburi : %s' % dbconnection.db_uri)
    log.debug('Database Connection infomation is : %s' % dbconnection.json())
    try:
        sycdsconfig = DSConfig(dbconnection.name)
        syncapiengine = APIEngine(sycdsconfig)
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
