from typing import Dict, Any, Optional, List

from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.crud import BaseApiOut
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.adminsite import site
from starlette.requests import Request

from .models import Category, DBConnection, DBConfig
from fastapi_amis_admin.amis import Page, PageSchema, Form, Action, Dialog, ActionType, LevelEnum
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
class TestConnectionAction(admin.ModelAction):
    action = ActionType.Dialog(label=_('Test Connection'), dialog=Dialog())

    async def handle(self, request: Request, item_id: List[str], data: Optional[BaseModel], session: AsyncSession,
                     **kwargs):
        # 从数据库获取用户选择的数据列表
        items = await self.fetch_item_scalars(session, item_id)
        # 执行动作处理
        ...
        # 返回动作处理结果
        return BaseApiOut(data=dict(item_id=item_id, data=data, items=list(items)))

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
            actions.append(Action(actionType='cancel', label=_('Cancel'), level=LevelEnum.default))
            action = await self.test_connection_action.get_action(request)
            action.label = _('Test Connection')
            actions.append(action.copy())
            actions.append(Action(actionType='submit', label=_('Submit'), level=LevelEnum.primary))
            drawer.actions = actions
        return c_action

    async def get_update_action(self, request: Request, bulk: bool = False) -> Action:
        u_action = await super().get_update_action(request)
        drawer = u_action.drawer
        actions = []
        actions.append(Action(actionType='cancel', label=_('Cancel'), level=LevelEnum.default))
        action = await self.test_connection_action.get_action(request)
        action.label = _('Test Connection')
        actions.append(action.copy())
        actions.append(Action(actionType='submit', label=_('Submit'), level=LevelEnum.primary))
        drawer.actions = actions
        return u_action

    def register_router(self):
        super().register_router()
        # 注册动作路由
        self.test_connection_action = TestConnectionAction(self).register_router()


# DBConfig Admin
class DBConfigAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='Database Config', icon='fa fa-wrench')
    model = DBConfig

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        c_form = await super().get_create_form(request, bulk)
        return c_form

    async def get_update_form(self, request: Request, bulk: bool = False) -> Form:
        u_form = await super().get_update_form(request)
        return u_form

class CategoryAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label='分类管理', icon='fa fa-tasks')
    model = Category
    search_fields = [Category.name]