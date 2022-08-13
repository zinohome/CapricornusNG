import importlib
from typing import Dict, Any, Optional, List

from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.crud import BaseApiOut
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select


try:
    import ujson as json
except ImportError:
    import json
from core.adminsite import site
from starlette.requests import Request

from .models import DBConnection, DBConfig, TableMeta
from fastapi_amis_admin.amis import Page, PageSchema, Form, Action, ActionType, LevelEnum, DisplayModeEnum, TableCRUD
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _

from apps.dadmins.car_partsadmin import Car_partsAdmin
from main import dsconfig, apiengine, dbmeta

# DataApp
@site.register_admin
class DataApp(admin.AdminApp):
    page_schema = amis.PageSchema(label=_('Tables'), icon='fa fa-table', sort=99)
    router_prefix = '/data'
    engine = apiengine.async_connect()

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        alltables = dbmeta.get_tables() + dbmeta.get_views()
        if len(alltables)>0:
            for tbl in alltables:
                dtable = dbmeta.gettable(tbl)
                if (len(dtable.primarykeys.strip()) > 0) or (len(dtable.logicprimarykeys.strip()) > 0):
                    adminmodel = importlib.import_module('apps.dadmins.' + tbl.strip().lower() + 'admin')
                    adminclass = getattr(adminmodel, tbl.strip().capitalize() + 'Admin')
                    log.debug('Register admin model %s ……' % tbl.strip().capitalize())
                    self.register_admin(adminclass)
            self.register_admin(BlankDataPageAdmin)
        else:
            self.register_admin(BlankDataPageAdmin)
# default DataPage
class BlankDataPageAdmin(admin.PageAdmin):
    page_schema = PageSchema(label='Data Explor', icon='fa fa-border-all')
    # 通过page类属性直接配置页面信息;
    page = Page(title='Data Explor', body='')

# AdminApp
@site.register_admin
class AdminApp(admin.AdminApp):
    page_schema = amis.PageSchema(label=_('DataSource'), icon='fa fa-cogs', sort=98)
    router_prefix = '/admin'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(DBConnectionAdmin, DBConfigAdmin, TableMetaAdmin)

# Register your models here.

# DBConnection Admin
class DBConnectionAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Database Connection', icon='fa fa-database')
    model = DBConnection
    list_display = [DBConnection.id, DBConnection.db_Type, DBConnection.name, DBConnection.db_Dialect, DBConnection.db_useschema, DBConnection.db_schema, DBConfig.name]
    search_fields = [DBConnection.name, DBConfig.name]
    test_connection_api = {
                'url':'/admin/db_connection_test',
                'method':'post',
                'data':{
                    'db_uri':'${db_uri}'
                        },
                'cache':10000
                    }
    sync_schema_api = {
                'url':'/admin/db_sync_schema',
                'method':'post',
                'data':{
                    'id':'${id}',
                    'name':'${name}',
                    'db_Type':'${db_Type}',
                    'db_Dialect':'${db_Dialect}',
                    'db_uri':'${db_uri}',
                    'db_useschema':'${db_useschema}',
                    'db_schema':'${db_schema}',
                    'db_exclude_tablespaces':'${db_exclude_tablespaces}',
                    'db_conf_id':'${db_conf_id}'
                        },
                'cache':1000
                    }

    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        header_toolbar = await super().get_actions_on_header_toolbar(request)
        for action in header_toolbar:
            if isinstance(action, amis.components.ActionType.Drawer):
                if action.label == _('Bulk Create'):
                    action.hidden = True
                    header_toolbar.remove(action)
        return header_toolbar

    async def get_create_action(self, request: Request, bulk: bool = False) -> Action:
        c_action = await super().get_create_action(request, bulk)
        if not bulk:
            drawer = c_action.drawer
            actions = []
            actions.append(Action(actionType='cancel', label=_('Cancel'), level=LevelEnum.default))
            actions.append(ActionType.Ajax(label=_('Test Connection'), required=['db_profilename','db_uri'], level=LevelEnum.secondary, api=DBConnectionAdmin.test_connection_api))
            actions.append(Action(actionType='submit', label=_('Submit'), level=LevelEnum.primary))
            drawer.actions = actions
        return c_action

    async def get_update_action(self, request: Request, bulk: bool = False) -> Action:
        u_action = await super().get_update_action(request, bulk)
        if not bulk:
            drawer = u_action.drawer
            actions = []
            actions.append(Action(actionType='cancel', label=_('Cancel'), level=LevelEnum.default))
            actions.append(ActionType.Ajax(label=_('Test Connection'), required=['db_profilename','db_uri'], level=LevelEnum.secondary, api=DBConnectionAdmin.test_connection_api))
            actions.append(ActionType.Ajax(label=_('Sync Structure'), confirmText=_('Confirm to sync all tables immediately?'), required=['db_profilename','db_uri'], level=LevelEnum.danger, api=DBConnectionAdmin.sync_schema_api))
            actions.append(Action(actionType='submit', label=_('Submit'), level=LevelEnum.primary))
            drawer.actions = actions
        return u_action

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.join(DBConfig, isouter=True)

# DBConfig Admin
class DBConfigAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Database Config', icon='fa fa-sliders-h')
    model = DBConfig
    search_fields = [DBConfig.name]

    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        header_toolbar = await super().get_actions_on_header_toolbar(request)
        for action in header_toolbar:
            if isinstance(action, amis.components.ActionType.Drawer):
                if action.label == _('Bulk Create'):
                    action.hidden = True
                    header_toolbar.remove(action)
        return header_toolbar

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        c_form = await super().get_create_form(request, bulk)
        if not bulk:
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs=[]
            tbody = c_form.body.copy()
            for item in c_form.body:
                tlabel = item.label
                item.label=False
                tabitem = amis.Tabs.Item(title=tlabel,tab=item)
                formtab.tabs.append(tabitem)
            c_form.body=formtab
        return c_form

    async def get_update_form(self, request: Request, bulk: bool = False) -> Form:
        u_form = await super().get_update_form(request, bulk)
        if not bulk:
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs=[]
            tbody = u_form.body.copy()
            for item in u_form.body:
                tlabel = item.label
                item.label=False
                tabitem = amis.Tabs.Item(title=tlabel,tab=item)
                formtab.tabs.append(tabitem)
            u_form.body=formtab
        return u_form

# TableMeta Admin
class TableMetaAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Table Meta', icon='fa fa-tasks')
    model = TableMeta
    search_fields = [TableMeta.name]

