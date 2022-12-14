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
from sqlmodel import Column, JSON
from apps.admin.models.basesqlmodel import BaseSQLModel
from core import i18n as _
from sqlmodel import Relationship


if TYPE_CHECKING:
    from .datasource import Datasource

default_column_page_defile="{\"column_name\":{\"name\": \"column_name\", \"type\": \"INTEGER\", \"nullable\": \"False\", \"default\": \"None\", \"autoincrement\": \"auto\", \"primary_key\": 0, \"pythonType\": \"int\", \"title\": \"column_name\", \"amis_form_item\": \"\", \"amis_table_column\": \"\"}}"


# DatasourcePage Model
class DatasourcePage(BaseSQLModel, table=True):
    __tablename__ = 'capricornus_page'
    meta_id: int = models.Field(default=None, title=_('MetaID'), primary_key=True, nullable=False)
    meta_name: str = models.Field(
        title=_('Name'),
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=False, index=True, nullable=False),
        amis_form_item=amis.InputText(disabled=True)
    )
    page_title: Optional[str] = models.Field(default='', title=_('Title'), max_length=256,
                                              amis_form_item=amis.InputText(disabled=False))
    meta_schema: Optional[str] = models.Field(default='', title=_('Schema'), max_length=256,
                                              amis_form_item=amis.InputText(disabled=True))
    meta_type: Optional[str] = models.Field(default='table', title=_('Type'),
                                            amis_form_item=amis.InputText(disabled=True))
    meta_primarykeys: Optional[str] = models.Field(default='', title=_('PrimaryKey'), max_length=256,
                                                   amis_form_item=amis.InputText(disabled=True))
    page_logicprimarykeys: Optional[str] = models.Field(default='', title=_('LogicPrimaryKey'), max_length=256,
                                                         amis_form_item=amis.InputText())
    meta_indexes: Optional[str] = models.Field(default='', title=_('Indexes'), max_length=256,
                                               amis_form_item=amis.InputText(disabled=True))
    meta_columns: Optional[List[dict]] = models.Field(index=False, default=json.loads(default_column_page_defile),
                                                      sa_column=Column(JSON), title=_('Columns'),
                                                      amis_form_item=amis.Combo(type='combo', items=[amis.InputText(name='name', label=_('Name'), unique='true', disabled=True),
                                                                                                  amis.InputText(name='title', label=_('Label')),
                                                                                                  amis.InputText(name='type', label=_('Type'), disabled=True),
                                                                                                  amis.InputText(name='nullable', label=_('Nullable'), disabled=True),
                                                                                                  amis.InputText(name='default', label=_('Default'), disabled=True),
                                                                                                  amis.InputText(name='autoincrement', label=_('Autoincrement'), disabled=True),
                                                                                                  amis.InputText(name='primary_key', label=_('Primarykey'), disabled=True),
                                                                                                  amis.InputText(name='pythonType', label=_('PythonType'), disabled=True),
                                                                                                  amis.InputText(name='amis_form_item', label=_('AMIS Form Item')),
                                                                                                  amis.InputText(name='amis_table_column', label=_('AMIS Table Column'))],
                                                                                canAccessSuperData=True, tabsMode=True,
                                                                                tabsStyle='line', multiLine=True,
                                                                                multiple=True,
                                                                                tabsLabelTpl='${meta_columns[${index}].name}'),
                                                      amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    page_list_display: Optional[str] = models.Field(default='', title=_('ListDisplay'), max_length=256,
                                          amis_form_item=amis.Transfer(sortable=True, source='/admin/get_column_options/${meta_id}'))
    page_search_fields: Optional[str] = models.Field(default='', title=_('SearchFields'), max_length=256,
                                          amis_form_item=amis.Transfer(sortable=True, source='/admin/get_column_options/${meta_id}'))
    ds_id: Optional[int] = models.Field(default=None, title=_('DatasourceID'), foreign_key="capricornus_datasource.ds_id")
    dpdatasource: "Datasource" = Relationship(back_populates="datasourcepages")
