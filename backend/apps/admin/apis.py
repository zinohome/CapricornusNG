from fastapi import APIRouter, Request
from core.adminsite import auth
router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/hello', include_in_schema=True)
async def hello(name: str = '') -> str:
    return f'hello {name}'

@router.get('/users')
async def read_users_me(request: Request) -> str:
    print(dir(auth))
    return auth.authenticate_user