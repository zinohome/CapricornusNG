import importlib

from fastapi import APIRouter, Request, Depends
import traceback

from sqlalchemy_database import AsyncDatabase

from apps.dmodels.brands import Brands
from apps.dmodels.car_parts import Car_parts
from core.settings import settings
from core.adminsite import site, auth
from crud import SQLModelCrud
from main import dsconfig, apiengine, dbmeta, prefix
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _

from util.toolkit import get_first_primarykey

router = APIRouter(prefix=prefix, dependencies=[Depends(auth.requires()())])

alltables = dbmeta.get_table_pages()
if len(alltables)>0:
    for tbl in alltables:
        dtable = dbmeta.getpage(tbl)
        pkname = get_first_primarykey(dtable.primarykeys.strip(), dtable.logicprimarykeys.strip())
        if not pkname is None:
            apimodel = importlib.import_module('apps.dmodels.' + tbl.strip().lower())
            apiclass = getattr(apimodel, tbl.strip().capitalize())
            apicrud = SQLModelCrud(apiclass, apiengine.async_connect(), pkname).register_crud()
            router.include_router(apicrud.router)

