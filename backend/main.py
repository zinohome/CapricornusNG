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

from asgi_correlation_id import CorrelationIdMiddleware
from sqlalchemy_database import Database
from sqlmodel import SQLModel, create_engine
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi_utils.timing import add_timing_middleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

from apps.admin.models.datasourceconfig import DatasourceConfig
from core.adminsite import site
from core.dsengine import DSEngine
from core.dbmeta import DBMeta
from core.dsconfig import DSConfig
from core.settings import settings
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from util.log import log as log
from util.toolkit import sync_uri
from core import i18n as _

from jaeger_client import Config as jaeger_config
from opentracing.scope_managers.contextvars import ContextVarsScopeManager
from opentracing_instrumentation.client_hooks import install_all_patches

from starlette_opentracing import StarletteTracingMiddleWare

# Initialize Tables
asyncurl = str(site.db.engine.sync_engine.url)
syncurl = sync_uri(asyncurl)
syncengine = create_engine(syncurl, echo=False)
metatables = DatasourceConfig.metadata.tables
Database(syncengine).run_sync(SQLModel.metadata.create_all, tables=[metatables['auth_user_roles'],metatables['auth_user_groups'],metatables['auth_group_roles'],metatables['auth_role_permissions'],metatables['auth_user'],metatables['auth_role'],metatables['auth_group'],metatables['auth_permission'],metatables['capricornus_datasource_config'],metatables['auth_token'],metatables['capricornus_datasource'],metatables['capricornus_meta'],metatables['capricornus_page']], is_session=False)
syncengine.dispose()

# dsconfig & dsengine
dsconfig = DSConfig(settings.app_profile)
apiengine = DSEngine(dsconfig)

# API prefix
prefix = dsconfig.Application_Config.app_prefix
if prefix.startswith('/'):
    pass
else:
    prefix = '/' + prefix
app = FastAPI(debug=settings.debug,
              title=dsconfig.Application_Config.app_name,
              description=dsconfig.Application_Config.app_description,
              version=dsconfig.Application_Config.app_version,
              openapi_url=prefix + "/openapi.json",
              docs_url=None,
              redoc_url=None
              )
# fastapi_utils.timing profiling
add_timing_middleware(app, record=log.debug, prefix="app", exclude="untimed")
# asgi-correlation-id
app.add_middleware(CorrelationIdMiddleware)
# starlette_exporter
app.add_middleware(
    PrometheusMiddleware,
    app_name="CapricornusNG",
    prefix='admin',
    labels={
        "server_name": os.getenv("HOSTNAME"),
    },
    group_paths=True,
    buckets=[0.1, 0.25, 0.5],
    skip_paths=['/health'],
    always_use_int_status=False)
app.add_route("/metrics", handle_metrics)

# jaeger_tracer
opentracing_config = jaeger_config(
    config={
        "sampler": {"type": "const", "param": 1},
        "logging": True,
        "local_agent": {"reporting_host": "192.168.32.120"},
    },
    scope_manager=ContextVarsScopeManager(),
    service_name="CapricornusNG",
)
jaeger_tracer = opentracing_config.initialize_tracer()
install_all_patches()
app.add_middleware(StarletteTracingMiddleWare, tracer=jaeger_tracer)


# 自动生成model和admin
dbmeta = DBMeta(dsconfig, apiengine)
if dsconfig.Application_Config.app_force_generate_meta:
    dbmeta.load_metadata()
    dbmeta.gen_schema()
    dbmeta.load_schema()
    dbmeta.gen_models()
    dbmeta.gen_admins()
else:
    dbmeta.load_schema()

# setup app
from apps import admin
admin.setup(app)

# mount admin app
site.mount_app(app)


@app.on_event("startup")
async def startup():

    from core.adminsite import auth
    #metatables = DatasourceConfig.metadata.tables
    #log.debug(metatables.keys())
    #await site.db.async_run_sync(SQLModel.metadata.create_all, tables=[metatables['auth_user_roles'],metatables['auth_user_groups'],metatables['auth_group_roles'],metatables['auth_role_permissions'],metatables['auth_user'],metatables['auth_role'],metatables['auth_group'],metatables['auth_permission'],metatables['capricornus_datasource_config'],metatables['auth_token'],metatables['capricornus_datasource'],metatables['capricornus_meta'],metatables['capricornus_page']], is_session=False)
    await auth.create_role_user(role_key='admin')
    await auth.create_role_user(role_key='writer')
    await auth.create_role_user(role_key='reader')

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

# 3.配置 Swagger UI CDN
from fastapi.openapi.docs import get_swagger_ui_html
@app.get("/apidocs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_favicon_url="/static/favicon.ico",
        swagger_css_url="/static/swagger-ui-dist@4/swagger-ui.css",
    )
@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

# 4.配置 Redoc CDN
@app.get("/apiredoc", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.ico",
        with_google_fonts=False,
    )
