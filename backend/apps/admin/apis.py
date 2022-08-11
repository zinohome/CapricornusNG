from asgiref.sync import sync_to_async
from fastapi import APIRouter, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
import traceback

from apiconfig.config import config
from apiconfig.dsconfig import DSConfig
from apps.admin.models import DBURIModel, DBConnection
from core.adminsite import auth
from core.apiengine import APIEngine
from core.dbmeta import DBMeta
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _

router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/hello', include_in_schema=False)
async def hello(name: str = '') -> str:
    return f'hello {name}'

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
async def db_connection_test(dbconnection: DBConnection) -> str:
    log.debug('Try to synchronize database schema dburi : %s' % dbconnection.db_uri)
    log.debug('Database Connection infomation is : %s' % dbconnection.json())
    try:
        dsconfig = await sync_to_async(func=DSConfig)(config('app_profile', default='default-datasource'))
        log.debug(dsconfig.Database_Config)
        apiengine = await sync_to_async(func=APIEngine)(dsconfig, config('app_profile', default='default-datasource'))
        dbmeta = await sync_to_async(func=DBMeta)(dsconfig, apiengine, config('app_profile', default='default-datasource'))
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
        log.debug('[Step 6/8] DataModels generated')
        log.debug('[Step 7/8] DataPages generated')
        log.debug('[Step 8/8] Service reloaded')
        return {"status":0,"msg":_("DataBase synchronized")}
    except Exception as e:
        traceback.print_exc()
        return {"status":1,"msg":_("DataBase synchronized Error")}

@router.get('/users',
         tags=["admin"],
         summary="Get user information.",
         description="Return user information",
         include_in_schema=True)
async def read_users_me(request: Request) -> str:
    print(dir(auth))
    return auth.authenticate_user