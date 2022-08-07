from typing import Dict, Any, Optional, List

from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.crud import BaseApiOut
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.adminsite import site
from starlette.requests import Request

from .models import Category, DBConnection, DBConfig
from fastapi_amis_admin.amis import Page, PageSchema, Form, Action, ActionType, LevelEnum, DisplayModeEnum
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _

@site.register_admin
class AdminApp(admin.AdminApp):
    page_schema = amis.PageSchema(label='Admin', icon='fa fa-tools')
    router_prefix = '/admin'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(DBConnectionAdmin, DBConfigAdmin, CategoryAdmin)

# Register your models here.

# DBConnection Admin
class DBConnectionAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Database Connection', icon='fa fa-database')
    model = DBConnection
    list_display = [DBConnection.id, DBConnection.db_Type, DBConnection.db_profilename, DBConnection.db_Dialect, DBConnection.db_useschema, DBConnection.db_schema]
    search_fields = [DBConnection.db_profilename]

    async def get_create_action(self, request: Request, bulk: bool = False) -> Action:
        c_action = await super().get_create_action(request, bulk)
        if not bulk:
            drawer = c_action.drawer
            actions = []
            api = {
                'url':'/admin/db_connection_test',
                'method':'post',
                'data':{
                    'db_uri':'${db_uri}'
                        },
                'cache':10000
                    }
            actions.append(Action(actionType='cancel', label=_('Cancel'), level=LevelEnum.default))
            actions.append(ActionType.Ajax(label=_('Test Connection'), required=['db_profilename','db_uri'], level=LevelEnum.secondary, api=api))
            actions.append(Action(actionType='submit', label=_('Submit'), level=LevelEnum.primary))
            drawer.actions = actions
        return c_action

    async def get_update_action(self, request: Request, bulk: bool = False) -> Action:
        u_action = await super().get_update_action(request)
        drawer = u_action.drawer
        actions = []
        api = {
            'url':'/admin/db_connection_test',
            'method':'post',
            'data':{
                'db_uri':'${db_uri}'
                    },
            'cache':10000
                }
        actions.append(Action(actionType='cancel', label=_('Cancel'), level=LevelEnum.default))
        actions.append(ActionType.Ajax(label=_('Test Connection'), required=['db_profilename','db_uri'], level=LevelEnum.secondary, api=api))
        actions.append(Action(actionType='submit', label=_('Submit'), level=LevelEnum.primary))
        drawer.actions = actions
        return u_action

# DBConfig Admin
class DBConfigAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Database Config', icon='fa fa-wrench')
    model = DBConfig

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
        u_form = await super().get_update_form(request)
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

class CategoryAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='分类管理', icon='fa fa-tasks')
    model = Category
    search_fields = [Category.name]
