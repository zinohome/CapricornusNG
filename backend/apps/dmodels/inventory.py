#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

from datetime import date
from decimal import Decimal
from utils.amis_admin import models
from typing import Optional
import sqlmodel
from core import i18n as _

class BaseSQLModel(sqlmodel.SQLModel):
    class Config:
        use_enum_values = True
        orm_mode = True
        arbitrary_types_allowed = True

class Inventory(BaseSQLModel, table=True):
    __tablename__ = 'inventory'
    inventory_id: Optional[int] = models.Field(default=None, title=_('inventory_id'), primary_key=True, amis_form_item='', amis_table_column='')
    type: Optional[str] = models.Field(default=None, title=_('type'), nullable=True, amis_form_item='', amis_table_column='')
    url: Optional[str] = models.Field(default=None, title=_('url'), nullable=True, amis_form_item='', amis_table_column='')
    created: Optional[str] = models.Field(default=None, title=_('created'), nullable=True, amis_form_item='', amis_table_column='')
    modified: Optional[str] = models.Field(default=None, title=_('modified'), nullable=True, amis_form_item='', amis_table_column='')
    name: str = models.Field(default=None, title=_('name'), nullable=False, amis_form_item='', amis_table_column='')
    description: Optional[str] = models.Field(default=None, title=_('description'), nullable=True, amis_form_item='', amis_table_column='')
    organization_id: Optional[int] = models.Field(default=None, title=_('organization_id'), nullable=True, amis_form_item='', amis_table_column='')
    kind: Optional[str] = models.Field(default=None, title=_('kind'), nullable=True, amis_form_item='', amis_table_column='')
    host_filter: Optional[str] = models.Field(default=None, title=_('host_filter'), nullable=True, amis_form_item='', amis_table_column='')
    variables: Optional[str] = models.Field(default=None, title=_('variables'), nullable=True, amis_form_item='', amis_table_column='')
    has_active_failures: Optional[int] = models.Field(default=None, title=_('has_active_failures'), nullable=True, amis_form_item='', amis_table_column='')
    total_hosts: Optional[int] = models.Field(default=None, title=_('total_hosts'), nullable=True, amis_form_item='', amis_table_column='')
    hosts_with_active_failures: Optional[int] = models.Field(default=None, title=_('hosts_with_active_failures'), nullable=True, amis_form_item='', amis_table_column='')
    total_groups: Optional[int] = models.Field(default=None, title=_('total_groups'), nullable=True, amis_form_item='', amis_table_column='')
    has_inventory_sources: Optional[int] = models.Field(default=None, title=_('has_inventory_sources'), nullable=True, amis_form_item='', amis_table_column='')
    total_inventory_sources: Optional[int] = models.Field(default=None, title=_('total_inventory_sources'), nullable=True, amis_form_item='', amis_table_column='')
    inventory_sources_with_failures: Optional[int] = models.Field(default=None, title=_('inventory_sources_with_failures'), nullable=True, amis_form_item='', amis_table_column='')
