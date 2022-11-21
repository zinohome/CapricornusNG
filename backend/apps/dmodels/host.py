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

class Host(BaseSQLModel, table=True):
    __tablename__ = 'host'
    host_id: Optional[int] = models.Field(default=None, title=_('host_id'), primary_key=True, amis_form_item='', amis_table_column='')
    type: Optional[str] = models.Field(default=None, title=_('type'), nullable=True, amis_form_item='', amis_table_column='')
    url: Optional[str] = models.Field(default=None, title=_('url'), nullable=True, amis_form_item='', amis_table_column='')
    created: Optional[str] = models.Field(default=None, title=_('created'), nullable=True, amis_form_item='', amis_table_column='')
    modified: Optional[str] = models.Field(default=None, title=_('modified'), nullable=True, amis_form_item='', amis_table_column='')
    name: Optional[str] = models.Field(default=None, title=_('name'), nullable=True, amis_form_item='', amis_table_column='')
    description: Optional[str] = models.Field(default=None, title=_('description'), nullable=True, amis_form_item='', amis_table_column='')
    inventory_id: Optional[int] = models.Field(default=None, title=_('inventory_id'), nullable=True, amis_form_item='', amis_table_column='')
    enabled: Optional[int] = models.Field(default=None, title=_('enabled'), nullable=True, amis_form_item='', amis_table_column='')
    instance_id: Optional[int] = models.Field(default=None, title=_('instance_id'), nullable=True, amis_form_item='', amis_table_column='')
    variables: Optional[str] = models.Field(default=None, title=_('variables'), nullable=True, amis_form_item='', amis_table_column='')
    last_job: Optional[int] = models.Field(default=None, title=_('last_job'), nullable=True, amis_form_item='', amis_table_column='')
    last_job_host_summary: Optional[int] = models.Field(default=None, title=_('last_job_host_summary'), nullable=True, amis_form_item='', amis_table_column='')
    ansible_facts_modified: Optional[str] = models.Field(default=None, title=_('ansible_facts_modified'), nullable=True, amis_form_item='', amis_table_column='')
