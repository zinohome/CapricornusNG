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
    type: Optional[str] = models.Field(default=None, title=_('type'), nullable=True, amis_form_item='', amis_table_column='')
    url: Optional[str] = models.Field(default=None, title=_('url'), nullable=True, amis_form_item='', amis_table_column='')
    created: Optional[str] = models.Field(default=None, title=_('created'), nullable=True, amis_form_item='', amis_table_column='')
    modified: Optional[str] = models.Field(default=None, title=_('modified'), nullable=True, amis_form_item='', amis_table_column='')
    name: Optional[str] = models.Field(default=None, title=_('name'), nullable=True, amis_form_item='', amis_table_column='')
    description: Optional[str] = models.Field(default=None, title=_('description'), nullable=True, amis_form_item='', amis_table_column='')
    unified_job_template: Optional[int] = models.Field(default=None, title=_('unified_job_template'), nullable=True, amis_form_item='', amis_table_column='')
    launch_type: Optional[str] = models.Field(default=None, title=_('launch_type'), nullable=True, amis_form_item='', amis_table_column='')
    status: Optional[str] = models.Field(default=None, title=_('status'), nullable=True, amis_form_item='', amis_table_column='')
    failed: Optional[int] = models.Field(default=None, title=_('failed'), nullable=True, amis_form_item='', amis_table_column='')
    started: Optional[str] = models.Field(default=None, title=_('started'), nullable=True, amis_form_item='', amis_table_column='')
    finished: Optional[str] = models.Field(default=None, title=_('finished'), nullable=True, amis_form_item='', amis_table_column='')
    canceled_on: Optional[str] = models.Field(default=None, title=_('canceled_on'), nullable=True, amis_form_item='', amis_table_column='')
    elapsed: Optional[Decimal] = models.Field(default=None, title=_('elapsed'), nullable=True, amis_form_item='', amis_table_column='')
    job_explanation: Optional[str] = models.Field(default=None, title=_('job_explanation'), nullable=True, amis_form_item='', amis_table_column='')
    execution_node: Optional[str] = models.Field(default=None, title=_('execution_node'), nullable=True, amis_form_item='', amis_table_column='')
    controller_node: Optional[str] = models.Field(default=None, title=_('controller_node'), nullable=True, amis_form_item='', amis_table_column='')
    job_type: Optional[str] = models.Field(default=None, title=_('job_type'), nullable=True, amis_form_item='', amis_table_column='')
    inventory_id: Optional[int] = models.Field(default=None, title=_('inventory_id'), nullable=True, amis_form_item='', amis_table_column='')
    project: Optional[int] = models.Field(default=None, title=_('project'), nullable=True, amis_form_item='', amis_table_column='')
    playbook: Optional[str] = models.Field(default=None, title=_('playbook'), nullable=True, amis_form_item='', amis_table_column='')
    scm_branch: Optional[str] = models.Field(default=None, title=_('scm_branch'), nullable=True, amis_form_item='', amis_table_column='')
    forks: Optional[int] = models.Field(default=None, title=_('forks'), nullable=True, amis_form_item='', amis_table_column='')
    limit: Optional[str] = models.Field(default=None, title=_('limit'), nullable=True, amis_form_item='', amis_table_column='')
    verbosity: Optional[int] = models.Field(default=None, title=_('verbosity'), nullable=True, amis_form_item='', amis_table_column='')
    extra_vars: Optional[str] = models.Field(default=None, title=_('extra_vars'), nullable=True, amis_form_item='', amis_table_column='')
    job_tags: Optional[str] = models.Field(default=None, title=_('job_tags'), nullable=True, amis_form_item='', amis_table_column='')
    force_handlers: Optional[int] = models.Field(default=None, title=_('force_handlers'), nullable=True, amis_form_item='', amis_table_column='')
    skip_tags: Optional[str] = models.Field(default=None, title=_('skip_tags'), nullable=True, amis_form_item='', amis_table_column='')
    start_at_task: Optional[str] = models.Field(default=None, title=_('start_at_task'), nullable=True, amis_form_item='', amis_table_column='')
    timeout: Optional[int] = models.Field(default=None, title=_('timeout'), nullable=True, amis_form_item='', amis_table_column='')
    use_fact_cache: Optional[int] = models.Field(default=None, title=_('use_fact_cache'), nullable=True, amis_form_item='', amis_table_column='')
    organization_id: Optional[int] = models.Field(default=None, title=_('organization_id'), nullable=True, amis_form_item='', amis_table_column='')
    job_template_id: Optional[int] = models.Field(default=None, title=_('job_template_id'), nullable=True, amis_form_item='', amis_table_column='')
