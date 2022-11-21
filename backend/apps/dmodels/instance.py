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

class Instance(BaseSQLModel, table=True):
    __tablename__ = 'instance'
    instance_id: Optional[int] = models.Field(default=None, title=_('instance_id'), primary_key=True, amis_form_item='', amis_table_column='')
    type: Optional[str] = models.Field(default=None, title=_('type'), nullable=True, amis_form_item='', amis_table_column='')
    url: Optional[str] = models.Field(default=None, title=_('url'), nullable=True, amis_form_item='', amis_table_column='')
    uuid: Optional[str] = models.Field(default=None, title=_('uuid'), nullable=True, amis_form_item='', amis_table_column='')
    hostname: Optional[str] = models.Field(default=None, title=_('hostname'), nullable=True, amis_form_item='', amis_table_column='')
    created: Optional[str] = models.Field(default=None, title=_('created'), nullable=True, amis_form_item='', amis_table_column='')
    modified: Optional[str] = models.Field(default=None, title=_('modified'), nullable=True, amis_form_item='', amis_table_column='')
    capacity_adjustment: Optional[Decimal] = models.Field(default=None, title=_('capacity_adjustment'), nullable=True, amis_form_item='', amis_table_column='')
    version: Optional[str] = models.Field(default=None, title=_('version'), nullable=True, amis_form_item='', amis_table_column='')
    capacity: Optional[int] = models.Field(default=None, title=_('capacity'), nullable=True, amis_form_item='', amis_table_column='')
    jobs_running: Optional[int] = models.Field(default=None, title=_('jobs_running'), nullable=True, amis_form_item='', amis_table_column='')
    jobs_total: Optional[int] = models.Field(default=None, title=_('jobs_total'), nullable=True, amis_form_item='', amis_table_column='')
    cpu: Optional[int] = models.Field(default=None, title=_('cpu'), nullable=True, amis_form_item='', amis_table_column='')
    memory: Optional[int] = models.Field(default=None, title=_('memory'), nullable=True, amis_form_item='', amis_table_column='')
    cpu_capacity: Optional[int] = models.Field(default=None, title=_('cpu_capacity'), nullable=True, amis_form_item='', amis_table_column='')
    mem_capacity: Optional[int] = models.Field(default=None, title=_('mem_capacity'), nullable=True, amis_form_item='', amis_table_column='')
    enabled: Optional[int] = models.Field(default=None, title=_('enabled'), nullable=True, amis_form_item='', amis_table_column='')
    managed_by_policy: Optional[int] = models.Field(default=None, title=_('managed_by_policy'), nullable=True, amis_form_item='', amis_table_column='')
