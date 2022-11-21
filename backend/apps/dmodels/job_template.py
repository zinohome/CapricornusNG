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

class Job_template(BaseSQLModel, table=True):
    __tablename__ = 'job_template'
    job_template_id: Optional[int] = models.Field(default=None, title=_('job_template_id'), primary_key=True, amis_form_item='', amis_table_column='')
    name: str = models.Field(default=None, title=_('name'), nullable=False, amis_form_item='', amis_table_column='')
    description: Optional[str] = models.Field(default=None, title=_('description'), nullable=True, amis_form_item='', amis_table_column='')
    job_type: Optional[str] = models.Field(default=None, title=_('job_type'), nullable=True, amis_form_item='', amis_table_column='')
    inventory_id: Optional[int] = models.Field(default=None, title=_('inventory_id'), nullable=True, amis_form_item='', amis_table_column='')
    project_id: Optional[int] = models.Field(default=None, title=_('project_id'), nullable=True, amis_form_item='', amis_table_column='')
    playbook: Optional[str] = models.Field(default=None, title=_('playbook'), nullable=True, amis_form_item='', amis_table_column='')
    scm_branch: Optional[str] = models.Field(default=None, title=_('scm_branch'), nullable=True, amis_form_item='', amis_table_column='')
    forks: Optional[int] = models.Field(default=None, title=_('forks'), nullable=True, amis_form_item='', amis_table_column='')
    limit: Optional[str] = models.Field(default=None, title=_('limit'), nullable=True, amis_form_item='', amis_table_column='')
    verbosity: Optional[int] = models.Field(default=None, title=_('verbosity'), nullable=True, amis_form_item='', amis_table_column='')
    job_tags: Optional[str] = models.Field(default=None, title=_('job_tags'), nullable=True, amis_form_item='', amis_table_column='')
    timeout: Optional[int] = models.Field(default=None, title=_('timeout'), nullable=True, amis_form_item='', amis_table_column='')
    job_slice_count: Optional[int] = models.Field(default=None, title=_('job_slice_count'), nullable=True, amis_form_item='', amis_table_column='')
    awx_job_template_id: Optional[int] = models.Field(default=None, title=_('awx_job_template_id'), nullable=True, amis_form_item='', amis_table_column='')
    extra_vars: Optional[str] = models.Field(default=None, title=_('extra_vars'), nullable=True, amis_form_item='', amis_table_column='')
    created: Optional[str] = models.Field(default=None, title=_('created'), nullable=True, amis_form_item='', amis_table_column='')
    modified: Optional[str] = models.Field(default=None, title=_('modified'), nullable=True, amis_form_item='', amis_table_column='')
    last_job_run: Optional[str] = models.Field(default=None, title=_('last_job_run'), nullable=True, amis_form_item='', amis_table_column='')
    last_job_failed: Optional[int] = models.Field(default=None, title=_('last_job_failed'), nullable=True, amis_form_item='', amis_table_column='')
    next_job_run: Optional[str] = models.Field(default=None, title=_('next_job_run'), nullable=True, amis_form_item='', amis_table_column='')
    status: Optional[str] = models.Field(default=None, title=_('status'), nullable=True, amis_form_item='', amis_table_column='')
    type: Optional[str] = models.Field(default=None, title=_('type'), nullable=True, amis_form_item='', amis_table_column='')
    level: Optional[int] = models.Field(default=None, title=_('level'), nullable=True, amis_form_item='', amis_table_column='')
