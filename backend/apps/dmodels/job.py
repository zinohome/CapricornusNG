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

class Job(BaseSQLModel, table=True):
    __tablename__ = 'job'
    job_id: Optional[int] = models.Field(default=None, title=_('job_id'), primary_key=True, amis_form_item='', amis_table_column='')
    name: str = models.Field(default=None, title=_('name'), nullable=False, amis_form_item='', amis_table_column='')
    description: Optional[str] = models.Field(default=None, title=_('description'), nullable=True, amis_form_item='', amis_table_column='')
    unified_job_template: Optional[int] = models.Field(default=None, title=_('unified_job_template'), nullable=True, amis_form_item='', amis_table_column='')
    launch_type: Optional[str] = models.Field(default=None, title=_('launch_type'), nullable=True, amis_form_item='', amis_table_column='')
    status: Optional[str] = models.Field(default=None, title=_('status'), nullable=True, amis_form_item='', amis_table_column='')
    failed: Optional[int] = models.Field(default=None, title=_('failed'), nullable=True, amis_form_item='', amis_table_column='')
    started: Optional[str] = models.Field(default=None, title=_('started'), nullable=True, amis_form_item='', amis_table_column='')
    finished: Optional[str] = models.Field(default=None, title=_('finished'), nullable=True, amis_form_item='', amis_table_column='')
    canceled_on: Optional[str] = models.Field(default=None, title=_('canceled_on'), nullable=True, amis_form_item='', amis_table_column='')
    elapsed: Optional[str] = models.Field(default=None, title=_('elapsed'), nullable=True, amis_form_item='', amis_table_column='')
    job_template_id: Optional[int] = models.Field(default=None, title=_('job_template_id'), nullable=True, amis_form_item='', amis_table_column='')
    awx_job_id: Optional[int] = models.Field(default=None, title=_('awx_job_id'), nullable=True, amis_form_item='', amis_table_column='')
