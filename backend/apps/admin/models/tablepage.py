#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
import sqlmodel

import simplejson as json
from fastapi_amis_admin import amis,models
from typing import TYPE_CHECKING,Optional, Dict, Any, List
from sqlmodel import Column, JSON
from apps.admin.models.basesqlmodel import BaseSQLModel
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _
from sqlmodel import Relationship


if TYPE_CHECKING:
    from .dbconnection import DBConnection

default_column_page_defile="{\"column_name\":{\"name\": \"column_name\", \"type\": \"INTEGER\", \"nullable\": \"False\", \"default\": \"None\", \"autoincrement\": \"auto\", \"primary_key\": 0, \"pythonType\": \"int\", \"title\": \"column_name\", \"amis_form_item\": \"\", \"amis_table_column\": \"\"}}"


# TablePage Model
class TablePage(BaseSQLModel, table=True):
    __tablename__ = 'capricornus_table_page'
    page_id: int = models.Field(default=None, title='ID', primary_key=True, nullable=False)
    name: str = models.Field(
        title='Table Name',
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=False, index=True, nullable=False),
                amis_form_item = amis.InputText(disabled = True)
    )
    label: Optional[str] = models.Field(default='', title='Label', max_length=256,
                                            amis_form_item=amis.InputText())
    table_schema: Optional[str] = models.Field(default='', title='Schema', max_length=256,
                                            amis_form_item=amis.Hidden())
    table_type: Optional[str] = models.Field(default='table', title='Type', amis_form_item=amis.Hidden())
    primarykeys: Optional[str] = models.Field(default='', title='PrimaryKey', max_length=256,
                                                         amis_form_item=amis.InputText(disabled = True))
    logicprimarykeys: Optional[str] = models.Field(default='', title='LogicPrimaryKey', max_length=256,
                                                         amis_form_item=amis.InputText())
    indexes: Optional[str] = models.Field(default='', title='Indexes', max_length=256,
                                                         amis_form_item=amis.Hidden())
    list_display: Optional[str] = models.Field(default='', title='ListDisplay', max_length=256,
                                          amis_form_item=amis.Transfer(sortable=True, source='/admin/get_column_options/${page_id}'))
    search_fields: Optional[str] = models.Field(default='', title='SearchFields', max_length=256,
                                          amis_form_item=amis.Transfer(sortable=True, source='/admin/get_column_options/${page_id}'))
    columns: Optional[List[dict]] = models.Field(index=False, default=json.loads(default_column_page_defile),
                                                   sa_column=Column(JSON), title='Columns',
                                                   amis_form_item=amis.Combo(type='combo', id='columns', items=[amis.InputText(name='name', label='Name', unique='true', disabled=True),
                                                                                                  amis.InputText(name='title', label='Title'),
                                                                                                  amis.Hidden(name='type', label='Type'),
                                                                                                  amis.Hidden(name='nullable', label='Nullable'),
                                                                                                  amis.Hidden(name='default', label='Default'),
                                                                                                  amis.Hidden(name='autoincrement', label='Autoincrement'),
                                                                                                  amis.Hidden(name='primary_key', label='Primarykey'),
                                                                                                  amis.Hidden(name='pythonType', label='PythonType'),
                                                                                                  amis.InputText(name='amis_form_item', label='FormItem'),
                                                                                                  amis.InputText(name='amis_table_column', label='TableColumn')],
                                                                            canAccessSuperData=True, tabsMode=True, tabsStyle='line', multiLine=True, multiple=True, tabsLabelTpl='${columns[${index}].name}'),
                                           amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    dbconn_id: int = models.Field(title='Connection ID', nullable=False, foreign_key="capricornus_db_connection.conn_id")
    tpdbconnection: "DBConnection" = Relationship(back_populates="tablepages")
