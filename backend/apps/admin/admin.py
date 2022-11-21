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

from amis import Editor, Divider, Table, Drawer, Alert, Button, CRUD
from utils.amis_admin import amis,admin
from utils.amis_admin.admin import AdminApp
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

from utils.amis_admin.amis import Page, PageSchema, Form, Action, ActionType, LevelEnum, DisplayModeEnum, TableCRUD
from utils.log import log as log
from core import i18n as _

from main import dsconfig, apiengine, dbmeta


# HomeAdmin
@site.register_admin
class HomeAdmin(admin.PageAdmin):
    group_schema = None
    page_schema = PageSchema(label=_('Home'), icon='fa fa-home', url='/home', isDefaultPage=True, sort=100)
    page_path = '/home'
    page = Page.parse_obj(
        {
            "type": "page",
            "title": _("Home"),
            "body":{
                "type": "service",
                "api": "/admin/get_home_statis",
                "body": [
                    {
                        "type": "cards",
                        "source": "${items}",
                        "columnsCount": 4,
                        "card": {
                            "type": "card",
                            "className": "m-b-none",
                            "header": {
                                "avatarText": "${avatarTX}",
                                "avatarTextBackground": [
                                    "#FFB900",
                                    "#D83B01",
                                    "#B50E0E",
                                    "#E81123",
                                    "#B4009E",
                                    "#5C2D91",
                                    "#0078D7",
                                    "#00B4FF",
                                    "#008272"
                                ],
                                "title": "${title}",
                                "subTitle": "${subtitle}"
                            },
                            "body": [
                                {
                                    "name": "usenum",
                                    "id": "u:114a9393eaa4",
                                    "label": _("Current:")
                                },
                                {
                                    "name": "sysnum",
                                    "id": "u:beb3b22ee4bc",
                                    "label": _("All:")
                                }
                            ],
                            "actions": [
                                {
                                    "label": "",
                                    "type": "button",
                                    "id": "u:d26c2b0d730c"
                                }
                            ],
                            "toolbar": [
                              {
                                "type": "tpl",
                                "tpl": "${tag}",
                                "className": "label label-warning"
                              }
                            ],
                            "id": "u:ec25ab7b71bb"
                        },
                        "id": "u:c3ad6665eb77",
                        "placeholder": _("No Data Found"),
                        "title": ""
                    },
                    {
                        "type": "tpl",
                        "tpl": _("<p>Capricornus DataSource Wizard</p>"),
                        "inline": True,
                        "id": "u:e5a109572034"
                    },
                    {
                        "type": "wizard",
                        "steps": [
                            {
                                "title": _("Step 1: Create DataSource"),
                                "body": [
                                    {
                                        "type": "input-text",
                                        "label": _("DataSource Name"),
                                        "name": "ds_name",
                                        "id": "ds_name",
                                        "mode": "horizontal",
                                        "required": "true",
                                        "value": "myDataSource"
                                    },
                                    {
                                        "type": "input-text",
                                        "label": _("DataSource URI"),
                                        "name": "ds_uri",
                                        "id": "ds_uri",
                                        "mode": "horizontal",
                                        "required": "true",
                                        "value": "mysql+aiomysql://root:password@127.0.0.1:3306/mydb?charset=utf8mb4"
                                    },
                                    {
                                        "type": "input-text",
                                        "label": _("Schema"),
                                        "name": "ds_schema",
                                        "id": "ds_schema",
                                        "mode": "horizontal"
                                    },
                                    {
                                        "type": "input-text",
                                        "label": _("Exclude Tablespaces"),
                                        "name": "ds_exclude_tablespaces",
                                        "id": "ds_exclude_tablespaces",
                                        "mode": "horizontal"
                                    }
                                ],
                                "id": "u:f48efff08050",
                                "mode": "normal",
                                "api": {
                                    "method": "post",
                                    "url": "/admin/dswizard",
                                    "data": {
                                        "ds_name": "${ds_name}",
                                        "ds_uri": "${ds_uri}",
                                        "ds_schema": "${ds_schema}",
                                        "ds_exclude_tablespaces": "${ds_exclude_tablespaces}",
                                        "step":"1"
                                    },
                                    "cache": 1000
                                }
                            },
                            {
                                "title": _("Step 2: Synchronize Data Structure"),
                                "body": [
                                    {
                                        "type": "input-text",
                                        "label": _("DataSource Name"),
                                        "name": "confirm_ds_name",
                                        "id": "confirm_ds_name",
                                        "mode": "horizontal",
                                        "required": "true",
                                        "value": "${ds_name}",
                                        "readOnly": "true"
                                    }
                                ],
                                "mode": "normal",
                                "api": {
                                    "method": "post",
                                    "url": "/admin/dswizard",
                                    "data": {
                                        "ds_name": "${confirm_ds_name}",
                                        "ds_uri": "",
                                        "ds_schema": "",
                                        "ds_exclude_tablespaces": "",
                                        "step":"2"
                                    },
                                    "cache": 1000
                                }
                            },
                            {
                                "title": _("Step 3: Enjoy Your REST API"),
                                "body": [
                                    {
                                        "type": "tpl",
                                        "tpl": _("<p>Good Job ! Now, enjoy your REST API by change the APP_PROFILE in your Environment variables to your DataSource Name.</p>"),
                                        "inline": True,
                                        "id": "u:e5a109572123"
                                    }
                                ],
                                "mode": "normal",
                                "api": {
                                    "method": "post",
                                    "url": "/admin/dswizard",
                                    "data": {
                                        "ds_name": "",
                                        "ds_uri": "",
                                        "ds_schema": "",
                                        "ds_exclude_tablespaces": "",
                                        "step":"3"
                                    },
                                    "cache": 1000
                                }
                            }
                        ],
                        "id": "u:4f418f772bc1",
                        "mode": "horizontal",
                        "onEvent": {
                        }
                    }
                ]
            },
            "id": "u:05f50d832729",
            "messages": {
            },
            "pullRefresh": {
            },
            "regions": [
                "body"
            ]
        }
    )

# DataApp
@site.register_admin
class DataApp(admin.AdminApp):
    page_schema = amis.PageSchema(label=_('Data Explore'), title='Capricornus - '+_('Data Explore'), icon='fa fa-table', sort=99)
    router_prefix = '/data'
    engine = apiengine.async_connect()

    def __init__(self, app: "DataApp"):
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
    page = Page(title=_('Data Explore'), body='')



# QueryApp
@site.register_admin
class QueryApp(admin.AdminApp):
    page_schema = amis.PageSchema(label=_('Data Query'), icon='fa fa-laptop', sort=98)
    router_prefix = '/query'

    def __init__(self, app: "QueryApp"):
        super().__init__(app)
        self.register_admin(DataQueryAdmin)

class DataQueryAdmin(admin.PageAdmin):
    group_schema = None
    page_schema = PageSchema(label=_('Data Query'), icon='fa fa-laptop')
    # 通过page类属性直接配置页面信息;
    queryform_submit_api = {
                'url':'/admin/sql_query',
                'method':'post',
                'data':{
                    'ds_uri':'${ds_uri}',
                    'query_sql':'${query_sql}'
                        },
                'cache':1000
                    }
    # query form
    form = Form(type='form', title='',
                name='queryform', id='queryform',
                submitText=_('> Run'), preventEnterSubmit=True,
                persistData='app.data.sqlqueryform',
                target='resultform.sqlresult')
    formbodylist = []
    formbodylist.append(amis.Select(type='select', label=_('Select DataSource'),
                                    name='ds_uri', id='ds_uri',
                                    multiple=False, selectMode='table',
                                    columns=[{'name':'label','label':_('DSName')},{'name':'uri','label':_('DSURI')}],
                                    source='/admin/get_ds_select_options'))
    formbodylist.append(Editor(type='editor', label=_('SQL Editor'), name='query_sql', id='query_sql', language='sql', size='md', allowFullscreen=False))
    form.body = formbodylist
    actions = []
    actions.append(Action(actionType='submit', label=_('> Run'), level=LevelEnum.secondary))
    form.actions = actions
    # result form
    resultform = Form(type='form', title='',
                name='resultform', id='resultform', preventEnterSubmit=True)
    resultformbodylist = []
    resultformbodylist.append(CRUD(type='crud', id='sqlresult', name='sqlresult',
                                   api=queryform_submit_api,
                                   headerToolbar=['export-csv'],
                                   syncLocation=False,
                                   loadDataOnce=True,
                                   loadDataOnceFetchOnFilter=False))
    resultform.body = resultformbodylist
    resultform.actions = []
    # page body
    pagebodylist = []
    pagebodylist.append(form)
    pagebodylist.append(Divider(type='divider', visible=True))
    pagebodylist.append(resultform)
    page = Page(body=pagebodylist)

# AdminApp
@site.register_admin
class AdminApp(admin.AdminApp):
    page_schema = amis.PageSchema(label=_('Data Source'), icon='fa fa-cogs', sort=97)
    router_prefix = '/admin'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(DBConnectionAdmin, DBConfigAdmin, TableMetaAdmin, TablePageAdmin)


# Datasource Admin
class DBConnectionAdmin(admin.ModelAdmin):
    group_schema = None
    page_schema = PageSchema(label=_('DataSources'), icon='fa fa-database')
    model = Datasource
    pk_name = 'ds_id'
    pk_label = 'ds_name'
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
    pk_label = 'ds_config_name'
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
    pk_label = 'meta_name'
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
    pk_label = 'meta_name'
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
    page_schema = PageSchema(label=_('Docs'), icon='fa fa-file-code')
    #src = '/apidocs'
    @property
    def src(self):
        return f'{self.app.site.settings.site_url}/apidocs'


@site.register_admin
class ReDocsAdmin(admin.IframeAdmin):
    group_schema = PageSchema(label=_('APIDocs'), icon='fa fa-book', sort=-100)
    page_schema = PageSchema(label=_('Redocs'), icon='fa fa-file-code')
    # 设置跳转链接
    @property
    def src(self):
        return f'{self.app.site.settings.site_url}/apiredoc'

@site.register_admin
class AmisDocAdmin(admin.IframeAdmin):
    group_schema = PageSchema(label=_('APIDocs'), icon='fa fa-book', sort=-100)
    page_schema = PageSchema(label='AmisDocument', icon='fa fa-file-image')
    src = 'https://aisuda.bce.baidu.com/amis/zh-CN/components/html'

@site.register_admin
class AmisEditorAdmin(admin.IframeAdmin):
    group_schema = PageSchema(label=_('APIDocs'), icon='fa fa-book', sort=-100)
    page_schema = PageSchema(label='AmisEditor', icon='fa fa-edit')
    src = 'https://aisuda.github.io/amis-editor-demo/'