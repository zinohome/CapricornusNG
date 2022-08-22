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
from typing import List

from fastapi_amis_admin import amis,admin
from fastapi_amis_admin.admin import AdminApp
from sqlmodel.sql.expression import Select

from apps.admin.models.datasourceconfig import DatasourceConfig
from apps.admin.models.datasource import Datasource
from apps.admin.models.dsmeta import DatasourceMeta
from apps.admin.models.dspage import DatasourcePage

try:
    import ujson as json
except ImportError:
    import json
from core.adminsite import site
from starlette.requests import Request

from fastapi_amis_admin.amis import Page, PageSchema, Form, Action, ActionType, LevelEnum, DisplayModeEnum, TableCRUD
from util.log import log as log
from core import i18n as _

from main import dsconfig, apiengine, dbmeta

# DataApp
@site.register_admin
class DataApp(admin.AdminApp):
    page_schema = amis.PageSchema(label=_('Data Explore'), title='Capricornus - '+_('Data Explore'), icon='fa fa-table', sort=99)
    router_prefix = '/data'
    engine = apiengine.async_connect()

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        alltables = dbmeta.get_table_pages()
        if len(alltables)>0:
            for tbl in alltables:
                dtable = dbmeta.getpage(tbl)
                if (len(dtable.meta_primarykeys.strip()) > 0) or (len(dtable.page_logicprimarykeys.strip()) > 0):
                    adminmodel = importlib.import_module('apps.dadmins.' + tbl.strip().lower() + 'admin')
                    adminclass = getattr(adminmodel, tbl.strip().capitalize() + 'Admin')
                    log.debug('Register admin model %s ……' % tbl.strip().capitalize())
                    self.register_admin(adminclass)
        else:
            self.register_admin(BlankDataPageAdmin)
# default DataPage
class BlankDataPageAdmin(admin.PageAdmin):
    page_schema = PageSchema(label=_('Data Explore'), icon='fa fa-border-all')
    # 通过page类属性直接配置页面信息;
    page = Page(title=_('Data Explor'), body='')

# Data Query Page
@site.register_admin
class DataQueryAdmin(admin.PageAdmin):
    group_schema = amis.PageSchema(label=_('Data Query'), icon='fa fa-laptop', sort=98)
    page_schema = PageSchema(label=_('Data Query'), icon='fa fa-laptop')
    # 通过page类属性直接配置页面信息;
    page = Page(title=_('Data Query'), body='')

# AdminApp
@site.register_admin
class AdminApp(admin.AdminApp):
    page_schema = amis.PageSchema(label=_('Data Source'), icon='fa fa-cogs', sort=98)
    router_prefix = '/admin'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(DBConnectionAdmin, DBConfigAdmin, TableMetaAdmin, TablePageAdmin)

# Register your models here.

# Datasource Admin
class DBConnectionAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label=_('DataSources'), icon='fa fa-database')
    model = Datasource
    pk_name = 'ds_id'
    list_display = [Datasource.ds_id, Datasource.ds_name, Datasource.ds_schema, DatasourceConfig.ds_config_name]
    search_fields = [Datasource.ds_name, DatasourceConfig.ds_config_name]
    test_connection_api = {
                'url':'/admin/db_connection_test',
                'method':'post',
                'data':{
                    'ds_uri':'${ds_uri}'
                        },
                'cache':10000
                    }
    sync_schema_api = {
                'url':'/admin/db_sync_schema',
                'method':'post',
                'data':{
                    'ds_id':'${ds_id}',
                    'ds_name':'${ds_name}',
                    'ds_uri':'${ds_uri}',
                    'ds_schema':'${ds_schema}',
                    'ds_exclude_tablespaces':'${ds_exclude_tablespaces}',
                    'ds_config_id':'${ds_config_id}'
                        },
                'cache':1000
                    }

    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        header_toolbar = await super().get_actions_on_header_toolbar(request)
        for action in header_toolbar:
            if isinstance(action, amis.components.ActionType.Drawer):
                if action.label == _('Bulk Create'):
                    action.hidden = True
        return header_toolbar

    async def get_create_action(self, request: Request, bulk: bool = False) -> Action:
        c_action = await super().get_create_action(request, bulk)
        if not bulk:
            drawer = c_action.drawer
            actions = []
            actions.append(Action(actionType='cancel', label=_('Cancel'), level=LevelEnum.default))
            actions.append(ActionType.Ajax(label=_('Test Connection'), required=['db_profilename','ds_uri'], level=LevelEnum.secondary, api=DBConnectionAdmin.test_connection_api))
            actions.append(Action(actionType='submit', label=_('Submit'), level=LevelEnum.primary))
            drawer.actions = actions
        return c_action

    async def get_update_action(self, request: Request, bulk: bool = False) -> Action:
        u_action = await super().get_update_action(request, bulk)
        if not bulk:
            drawer = u_action.drawer
            actions = []
            actions.append(Action(actionType='cancel', label=_('Cancel'), level=LevelEnum.default))
            actions.append(ActionType.Ajax(label=_('Test Connection'), required=['db_profilename','ds_uri'], level=LevelEnum.secondary, api=DBConnectionAdmin.test_connection_api))
            actions.append(ActionType.Ajax(label=_('Sync Structure'), confirmText=_('Confirm to sync all tables immediately?'), required=['ds_name','ds_uri'], level=LevelEnum.danger, api=DBConnectionAdmin.sync_schema_api))
            actions.append(Action(actionType='submit', label=_('Submit'), level=LevelEnum.primary))
            drawer.actions = actions
        return u_action

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.join(DatasourceConfig, isouter=True)

# DatasourceConfig Admin
class DBConfigAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label=_('Datasource Config'), icon='fa fa-sliders-h')
    model = DatasourceConfig
    pk_name = 'ds_config_id'
    search_fields = [DatasourceConfig.ds_config_name]

    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        header_toolbar = await super().get_actions_on_header_toolbar(request)
        for action in header_toolbar:
            if isinstance(action, amis.components.ActionType.Drawer):
                if action.label == _('Bulk Create'):
                    action.hidden = True
        return header_toolbar

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        c_form = await super().get_create_form(request, bulk)
        if not bulk:
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs=[]
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
            for item in u_form.body:
                tlabel = item.label
                item.label=False
                tabitem = amis.Tabs.Item(title=tlabel,tab=item)
                formtab.tabs.append(tabitem)
            u_form.body=formtab
        return u_form

# DatasourceMeta Admin
class TableMetaAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label=_('Table Meta'), icon='fa fa-tasks')
    model = DatasourceMeta
    pk_name = 'meta_id'
    list_display = [Datasource.ds_name, DatasourceMeta.meta_id, DatasourceMeta.meta_name, DatasourceMeta.meta_type, DatasourceMeta.meta_primarykeys, DatasourceMeta.meta_columns]
    search_fields = [DatasourceMeta.meta_name]

    async def get_select(self, request: Request) -> Select:
        g_select = await super().get_select(request)
        g_select = g_select.select_from(DatasourceMeta).join(Datasource)
        return g_select

    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        header_toolbar = await super().get_actions_on_header_toolbar(request)
        for action in header_toolbar:
            if action.type == 'button':
                if action.label == _('Bulk Create') or action.label == _('Create'):
                    action.hidden = True
        return header_toolbar

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        c_form = await super().get_create_form(request, bulk)
        if not bulk:
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs=[]
            fieldlist = []
            comboitem = None
            for item in c_form.body:
                if item.type == 'combo':
                    comboitem = item
                else:
                    fieldlist.append(item)
            basictabitem = amis.Tabs.Item(title=_('Basic Info'), tab=fieldlist)
            combotabitem = amis.Tabs.Item(title=comboitem.label, tab=comboitem)
            formtab.tabs.append(basictabitem)
            formtab.tabs.append(combotabitem)
            c_form.body=formtab
        return c_form

    async def get_update_form(self, request: Request, bulk: bool = False) -> Form:
        u_form = await super().get_update_form(request, bulk)
        if not bulk:
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs=[]
            fieldlist = []
            comboitem = None
            for item in u_form.body:
                if item.type == 'combo':
                    comboitem = item
                else:
                    fieldlist.append(item)
            basictabitem = amis.Tabs.Item(title=_('Basic Info'), tab=fieldlist)
            combotabitem = amis.Tabs.Item(title=comboitem.label, tab=comboitem)
            formtab.tabs.append(basictabitem)
            formtab.tabs.append(combotabitem)
            u_form.body=formtab
        return u_form

# DatasourcePage Admin
class TablePageAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label=_('Page Define'), icon='fa fa-file-alt')
    model = DatasourcePage
    pk_name = 'meta_id'
    list_display = [Datasource.ds_name, DatasourcePage.meta_id, DatasourcePage.meta_name, DatasourcePage.page_title, DatasourcePage.meta_primarykeys, DatasourcePage.page_logicprimarykeys, DatasourcePage.meta_columns]
    search_fields = [DatasourcePage.meta_name]

    async def get_select(self, request: Request) -> Select:
        g_select = await super().get_select(request)
        g_select = g_select.select_from(DatasourcePage).join(Datasource)
        return g_select

    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        header_toolbar = await super().get_actions_on_header_toolbar(request)
        for action in header_toolbar:
            if action.type == 'button':
                if action.label == _('Bulk Create') or action.label == _('Create') :
                    action.hidden = True
        return header_toolbar

    async def get_create_form(self, request: Request, bulk: bool = False) -> Form:
        c_form = await super().get_create_form(request, bulk)
        if not bulk:
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs=[]
            fieldlist = []
            comboitem = None
            for item in c_form.body:
                if item.type == 'combo':
                    comboitem = item
                else:
                    fieldlist.append(item)
            basictabitem = amis.Tabs.Item(title=_('Basic Info'), tab=fieldlist)
            combotabitem = amis.Tabs.Item(title=comboitem.label, tab=comboitem)
            formtab.tabs.append(basictabitem)
            formtab.tabs.append(combotabitem)
            c_form.body=formtab
        return c_form

    async def get_update_form(self, request: Request, bulk: bool = False) -> Form:
        u_form = await super().get_update_form(request, bulk)
        if not bulk:
            formtab = amis.Tabs(tabsMode='line')
            formtab.tabs=[]
            fieldlist = []
            comboitem = None
            for item in u_form.body:
                if item.type == 'combo':
                    comboitem = item
                else:
                    fieldlist.append(item)
            basictabitem = amis.Tabs.Item(title=_('Basic Info'), tab=fieldlist)
            combotabitem = amis.Tabs.Item(title=comboitem.label, tab=comboitem)
            formtab.tabs.append(basictabitem)
            formtab.tabs.append(combotabitem)
            u_form.body=formtab
        return u_form

# API docs

@site.register_admin
class DocsAdmin(admin.IframeAdmin):
    group_schema = PageSchema(label=_('APIDocs'), icon='fa fa-book', sort=-100)
    page_schema = PageSchema(label=_('Docs'), icon='fa fa-book')
    #src = '/apidocs'
    @property
    def src(self):
        return f'{self.app.site.settings.site_url}/apidocs'


@site.register_admin
class ReDocsAdmin(admin.IframeAdmin):
    group_schema = PageSchema(label=_('APIDocs'), icon='fa fa-book', sort=-100)
    page_schema = PageSchema(label=_('Redocs'), icon='fa fa-book')
    # 设置跳转链接
    @property
    def src(self):
        return f'{self.app.site.settings.site_url}/apiredoc'