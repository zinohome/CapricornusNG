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
from apps.admin.models.basesqlmodel import BaseSQLModel
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _
from sqlmodel import Relationship, Column, JSON
from .tabletype import TableType

if TYPE_CHECKING:
    from .dbconnection import DBConnection

default_column_defile="{\"column_name\":{\"name\": \"column_name\", \"type\": \"INTEGER\", \"nullable\": \"False\", \"default\": \"None\", \"autoincrement\": \"auto\", \"primary_key\": 0, \"pythonType\": \"int\"}}"

class TableMeta(BaseSQLModel, table=True):
    __tablename__ = 'capricornus_table_meta'
    meta_id: int = models.Field(default=None, title='ID', primary_key=True, nullable=False)
    name: str = models.Field(
        title='Table Name',
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=False, index=True, nullable=False),
                amis_form_item = amis.InputText(disabled = True)
    )
    table_schema: Optional[str] = models.Field(default='', title='Schema', max_length=256,
                                            amis_form_item=amis.InputText(disabled = True))
    table_type: TableType = models.Field(TableType.table, title='Type',amis_form_item = amis.InputText(disabled = True))
    primarykeys: Optional[str] = models.Field(default='', title='PrimaryKey', max_length=256,
                                                         amis_form_item=amis.InputText(disabled = True))
    indexes: Optional[str] = models.Field(default='', title='Indexes', max_length=256,
                                                         amis_form_item=amis.InputText(disabled = True))
    columns: Optional[List[dict]] = models.Field(index=False, default=json.loads(default_column_defile),
                                           sa_column=Column(JSON), title='Columns',
                                                   amis_form_item=amis.Combo(type='combo', items=[amis.InputText(name='name', label='Name', unique='true', disabled=True),
                                                                                                  amis.InputText(name='type', label='Type', disabled=True),
                                                                                                  amis.InputText(name='nullable', label='Nullable', disabled=True),
                                                                                                  amis.InputText(name='default', label='Default', disabled=True),
                                                                                                  amis.InputText(name='autoincrement', label='Autoincrement', disabled=True),
                                                                                                  amis.InputText(name='primary_key', label='Primarykey', disabled=True),
                                                                                                  amis.InputText(name='pythonType', label='PythonType', disabled=True)],
                                                                            canAccessSuperData=True, tabsMode=True, tabsStyle='line', multiLine=True, multiple=True, tabsLabelTpl='${columns[${index}].name}'),
                                           amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    dbconn_id: int = models.Field(title='Connection ID', nullable=False, foreign_key="capricornus_db_connection.conn_id")
    tmdbconnection: "DBConnection" = Relationship(back_populates="tablemetas")
