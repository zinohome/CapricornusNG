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
from utils.amis_admin import amis,models
from typing import TYPE_CHECKING,Optional, List
from apps.admin.models.basesqlmodel import BaseSQLModel
from core import i18n as _
from sqlmodel import Relationship, Column, JSON

if TYPE_CHECKING:
    from .datasource import Datasource

default_column_defile="{\"column_name\":{\"name\": \"column_name\", \"type\": \"INTEGER\", \"nullable\": \"False\", \"default\": \"None\", \"autoincrement\": \"auto\", \"primary_key\": 0, \"pythonType\": \"int\"}}"

class DatasourceMeta(BaseSQLModel, table=True):
    __tablename__ = 'capricornus_meta'
    meta_id: int = models.Field(default=None, title=_('MetaID'), primary_key=True, nullable=False)
    meta_name: str = models.Field(
        title=_('Name'),
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=False, index=True, nullable=False),
                amis_form_item = amis.InputText(disabled = True)
    )
    meta_schema: Optional[str] = models.Field(default='', title=_('Schema'), max_length=256,
                                            amis_form_item=amis.InputText(disabled = True))
    meta_type: Optional[str] = models.Field(default='table', title=_('Type'),amis_form_item = amis.InputText(disabled = True))
    meta_primarykeys: Optional[str] = models.Field(default='', title=_('PrimaryKey'), max_length=256,
                                                         amis_form_item=amis.InputText(disabled = True))
    meta_indexes: Optional[str] = models.Field(default='', title=_('Indexes'), max_length=256,
                                                         amis_form_item=amis.InputText(disabled = True))
    meta_columns: Optional[List[dict]] = models.Field(index=False, default=json.loads(default_column_defile),
                                           sa_column=Column(JSON), title=_('Columns'),
                                                   amis_form_item=amis.Combo(type='combo', items=[amis.InputText(name='name', label=_('Name'), unique='true', disabled=True),
                                                                                                  amis.InputText(name='type', label=_('Type'), disabled=True),
                                                                                                  amis.InputText(name='nullable', label=_('Nullable'), disabled=True),
                                                                                                  amis.InputText(name='default', label=_('Default'), disabled=True),
                                                                                                  amis.InputText(name='autoincrement', label=_('Autoincrement'), disabled=True),
                                                                                                  amis.InputText(name='primary_key', label=_('Primarykey'), disabled=True),
                                                                                                  amis.InputText(name='pythonType', label=_('PythonType'), disabled=True)],
                                                                            canAccessSuperData=True, tabsMode=True, tabsStyle='line', multiLine=True, multiple=True, tabsLabelTpl='${meta_columns[${index}].name}'),
                                           amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    ds_id: Optional[int] = models.Field(default=None, title=_('DatasourceID'), foreign_key="capricornus_datasource.ds_id")
    dmdatasource: "Datasource" = Relationship(back_populates="datasourcemetas")
