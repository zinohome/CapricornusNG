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
    type: Optional[str] = models.Field(default=None, title=_('type'), nullable=True, amis_form_item='', amis_table_column='')
    url: Optional[str] = models.Field(default=None, title=_('url'), nullable=True, amis_form_item='', amis_table_column='')
    created: Optional[str] = models.Field(default=None, title=_('created'), nullable=True, amis_form_item='', amis_table_column='')
    modified: Optional[str] = models.Field(default=None, title=_('modified'), nullable=True, amis_form_item='', amis_table_column='')
    name: Optional[str] = models.Field(default=None, title=_('name'), nullable=True, amis_form_item='', amis_table_column='')
    description: Optional[str] = models.Field(default=None, title=_('description'), nullable=True, amis_form_item='', amis_table_column='')
    job_type: Optional[str] = models.Field(default=None, title=_('job_type'), nullable=True, amis_form_item='', amis_table_column='')
    inventory_id: Optional[int] = models.Field(default=None, title=_('inventory_id'), nullable=True, amis_form_item='', amis_table_column='')
    project_id: Optional[int] = models.Field(default=None, title=_('project_id'), nullable=True, amis_form_item='', amis_table_column='')
    playbook: Optional[str] = models.Field(default=None, title=_('playbook'), nullable=True, amis_form_item='', amis_table_column='')
    scm_branch: Optional[str] = models.Field(default=None, title=_('scm_branch'), nullable=True, amis_form_item='', amis_table_column='')
    forks: Optional[int] = models.Field(default=None, title=_('forks'), nullable=True, amis_form_item='', amis_table_column='')
    limit: Optional[str] = models.Field(default=None, title=_('limit'), nullable=True, amis_form_item='', amis_table_column='')
    verbosity: Optional[str] = models.Field(default=None, title=_('verbosity'), nullable=True, amis_form_item='', amis_table_column='')
    extra_vars: Optional[str] = models.Field(default=None, title=_('extra_vars'), nullable=True, amis_form_item='', amis_table_column='')
    job_tags: Optional[str] = models.Field(default=None, title=_('job_tags'), nullable=True, amis_form_item='', amis_table_column='')
    force_handlers: Optional[int] = models.Field(default=None, title=_('force_handlers'), nullable=True, amis_form_item='', amis_table_column='')
    skip_tags: Optional[str] = models.Field(default=None, title=_('skip_tags'), nullable=True, amis_form_item='', amis_table_column='')
    start_at_task: Optional[str] = models.Field(default=None, title=_('start_at_task'), nullable=True, amis_form_item='', amis_table_column='')
    timeout: Optional[int] = models.Field(default=None, title=_('timeout'), nullable=True, amis_form_item='', amis_table_column='')
    use_fact_cache: Optional[int] = models.Field(default=None, title=_('use_fact_cache'), nullable=True, amis_form_item='', amis_table_column='')
    organization_id: Optional[int] = models.Field(default=None, title=_('organization_id'), nullable=True, amis_form_item='', amis_table_column='')
    last_job_run: Optional[str] = models.Field(default=None, title=_('last_job_run'), nullable=True, amis_form_item='', amis_table_column='')
    last_job_failed: Optional[int] = models.Field(default=None, title=_('last_job_failed'), nullable=True, amis_form_item='', amis_table_column='')
    next_job_run: Optional[str] = models.Field(default=None, title=_('next_job_run'), nullable=True, amis_form_item='', amis_table_column='')
    status: Optional[str] = models.Field(default=None, title=_('status'), nullable=True, amis_form_item='', amis_table_column='')
    host_config_key: Optional[str] = models.Field(default=None, title=_('host_config_key'), nullable=True, amis_form_item='', amis_table_column='')
    ask_scm_branch_on_launch: Optional[int] = models.Field(default=None, title=_('ask_scm_branch_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    ask_diff_mode_on_launch: Optional[int] = models.Field(default=None, title=_('ask_diff_mode_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    ask_variables_on_launch: Optional[int] = models.Field(default=None, title=_('ask_variables_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    ask_limit_on_launch: Optional[int] = models.Field(default=None, title=_('ask_limit_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    ask_tags_on_launch: Optional[int] = models.Field(default=None, title=_('ask_tags_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    ask_skip_tags_on_launch: Optional[int] = models.Field(default=None, title=_('ask_skip_tags_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    ask_job_type_on_launch: Optional[int] = models.Field(default=None, title=_('ask_job_type_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    ask_verbosity_on_launch: Optional[int] = models.Field(default=None, title=_('ask_verbosity_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    ask_inventory_on_launch: Optional[int] = models.Field(default=None, title=_('ask_inventory_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    ask_credential_on_launch: Optional[int] = models.Field(default=None, title=_('ask_credential_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    survey_enabled: Optional[int] = models.Field(default=None, title=_('survey_enabled'), nullable=True, amis_form_item='', amis_table_column='')
    become_enabled: Optional[int] = models.Field(default=None, title=_('become_enabled'), nullable=True, amis_form_item='', amis_table_column='')
    diff_mode: Optional[int] = models.Field(default=None, title=_('diff_mode'), nullable=True, amis_form_item='', amis_table_column='')
    allow_simultaneous: Optional[int] = models.Field(default=None, title=_('allow_simultaneous'), nullable=True, amis_form_item='', amis_table_column='')
    custom_virtualenv: Optional[str] = models.Field(default=None, title=_('custom_virtualenv'), nullable=True, amis_form_item='', amis_table_column='')
    job_slice_count: Optional[int] = models.Field(default=None, title=_('job_slice_count'), nullable=True, amis_form_item='', amis_table_column='')
    webhook_service: Optional[str] = models.Field(default=None, title=_('webhook_service'), nullable=True, amis_form_item='', amis_table_column='')
    webhook_credential: Optional[int] = models.Field(default=None, title=_('webhook_credential'), nullable=True, amis_form_item='', amis_table_column='')
