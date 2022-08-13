#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #  -- metastore & pagedef
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
import asyncio

from asgiref.sync import async_to_sync
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from sqlmodel import SQLModel
from starlette.staticfiles import StaticFiles

from core.adminsite import site
from core.apiengine import APIEngine
from core.dbmeta import DBMeta
from core.dsconfig import DSConfig
from core.settings import settings
from util.log import log as log

app = FastAPI(debug=settings.debug)
dsconfig = DSConfig(settings.app_profile)
apiengine = APIEngine(dsconfig)

# 自动生成model和admin
dbmeta = DBMeta(dsconfig, apiengine)
if dsconfig.Application_Config.app_force_generate_meta:
    dbmeta.load_metadata()
    dbmeta.gen_schema()
dbmeta.load_schema()
dbmeta.gen_models()
dbmeta.gen_admins()

# 安装应用
from apps import admin
admin.setup(app)

# 挂载后台管理系统
site.mount_app(app)


@app.on_event("startup")
async def startup():

    from core.adminsite import auth
    await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)
    await auth.create_role_user(role_key='admin')
    await auth.create_role_user(role_key='vip')
    await auth.create_role_user(role_key='test')

    #from core.adminsite import scheduler
    #scheduler.start()



@app.get('/')
async def index():
    return RedirectResponse(url=site.router_path)


# 1.配置 CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)

# 2. 配置静态资源目录
app.mount("/static", StaticFiles(directory="apps/static"), name="static")

# # 3.配置 Swagger UI CDN
# from fastapi.openapi.docs import get_swagger_ui_html
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title=f"{app.title} - Swagger UI",
#         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         swagger_js_url="https://unpkg.com/swagger-ui-dist@4/swagger-ui-bundle.js",
#         swagger_css_url="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css",
#     )
