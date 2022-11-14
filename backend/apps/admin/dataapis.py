#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

import importlib

from fastapi import APIRouter, Depends
from fastapi_user_auth.auth import AuthRouter

from core.adminsite import auth
from util.crud import SQLModelCrud
from main import dsconfig, apiengine, dbmeta, prefix
from util.log import log as log
from core import i18n as _

from util.toolkit import get_first_primarykey

router = APIRouter(prefix=prefix)
#router = APIRouter(prefix=prefix, dependencies=[Depends(auth.requires()())])

apiauthrouter = AuthRouter(auth)
for route in apiauthrouter.router.routes:
    if route.name == 'oauth_token':
        for depend in route.dependencies:
            if isinstance(depend.dependency, apiauthrouter.OAuth2):
                route.dependencies.remove(depend)
                route.dependencies.append(Depends(apiauthrouter.OAuth2(tokenUrl=f"{prefix}{apiauthrouter.router_path}/gettoken", auto_error=False)))
                break
        break
router.include_router(apiauthrouter.router)

alltables = dbmeta.get_table_pages()
if len(alltables)>0:
    for tbl in alltables:
        dtable = dbmeta.getpage(tbl)
        pkname = get_first_primarykey(dtable.meta_primarykeys.strip(), dtable.page_logicprimarykeys.strip())
        if not pkname is None:
            apimodel = importlib.import_module('apps.dmodels.' + tbl.strip().lower())
            apiclass = getattr(apimodel, tbl.strip().capitalize())
            apicrud = SQLModelCrud(apiclass, apiengine.async_connect(), pkname).register_crud()
            router.include_router(apicrud.router, dependencies=[Depends(auth.requires()())])
            #router.include_router(apicrud.router)

