from fastapi import APIRouter, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
import traceback

from apps.admin.models import DBURIModel
from core.adminsite import auth
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
        return {"status":0,"msg":_("DataBase Connect Error")}

@router.get('/users',
         tags=["admin"],
         summary="Get user information.",
         description="Return user information",
         include_in_schema=True)
async def read_users_me(request: Request) -> str:
    print(dir(auth))
    return auth.authenticate_user