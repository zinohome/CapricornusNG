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
    name: str = models.Field(default=None, title=_('name'), nullable=False, amis_form_item='', amis_table_column='')
    description: Optional[str] = models.Field(default=None, title=_('description'), nullable=True, amis_form_item='', amis_table_column='')
    enabled: Optional[int] = models.Field(default=None, title=_('enabled'), nullable=True, amis_form_item='', amis_table_column='')
    ip: Optional[str] = models.Field(default=None, title=_('ip'), nullable=True, amis_form_item='', amis_table_column='')
    username: Optional[str] = models.Field(default=None, title=_('username'), nullable=True, amis_form_item='', amis_table_column='')
    password: Optional[str] = models.Field(default=None, title=_('password'), nullable=True, amis_form_item='', amis_table_column='')
    awx_host_id: Optional[int] = models.Field(default=None, title=_('awx_host_id'), nullable=True, amis_form_item='', amis_table_column='')
    created: Optional[str] = models.Field(default=None, title=_('created'), nullable=True, amis_form_item='', amis_table_column='')
    modified: Optional[str] = models.Field(default=None, title=_('modified'), nullable=True, amis_form_item='', amis_table_column='')
    tag: Optional[str] = models.Field(default=None, title=_('tag'), nullable=True, amis_form_item='', amis_table_column='')
