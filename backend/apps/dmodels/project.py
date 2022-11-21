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

class Project(BaseSQLModel, table=True):
    __tablename__ = 'project'
    project_id: Optional[int] = models.Field(default=None, title=_('project_id'), primary_key=True, amis_form_item='', amis_table_column='')
    type: Optional[str] = models.Field(default=None, title=_('type'), nullable=True, amis_form_item='', amis_table_column='')
    url: Optional[str] = models.Field(default=None, title=_('url'), nullable=True, amis_form_item='', amis_table_column='')
    created: Optional[str] = models.Field(default=None, title=_('created'), nullable=True, amis_form_item='', amis_table_column='')
    modified: Optional[str] = models.Field(default=None, title=_('modified'), nullable=True, amis_form_item='', amis_table_column='')
    name: Optional[str] = models.Field(default=None, title=_('name'), nullable=True, amis_form_item='', amis_table_column='')
    description: Optional[str] = models.Field(default=None, title=_('description'), nullable=True, amis_form_item='', amis_table_column='')
    local_path: Optional[str] = models.Field(default=None, title=_('local_path'), nullable=True, amis_form_item='', amis_table_column='')
    scm_type: Optional[str] = models.Field(default=None, title=_('scm_type'), nullable=True, amis_form_item='', amis_table_column='')
    scm_url: Optional[str] = models.Field(default=None, title=_('scm_url'), nullable=True, amis_form_item='', amis_table_column='')
    scm_branch: Optional[str] = models.Field(default=None, title=_('scm_branch'), nullable=True, amis_form_item='', amis_table_column='')
    scm_refspec: Optional[str] = models.Field(default=None, title=_('scm_refspec'), nullable=True, amis_form_item='', amis_table_column='')
    scm_clean: Optional[int] = models.Field(default=None, title=_('scm_clean'), nullable=True, amis_form_item='', amis_table_column='')
    scm_delete_on_update: Optional[int] = models.Field(default=None, title=_('scm_delete_on_update'), nullable=True, amis_form_item='', amis_table_column='')
    credential_id: Optional[int] = models.Field(default=None, title=_('credential_id'), nullable=True, amis_form_item='', amis_table_column='')
    timeout: Optional[int] = models.Field(default=None, title=_('timeout'), nullable=True, amis_form_item='', amis_table_column='')
    scm_revision: Optional[str] = models.Field(default=None, title=_('scm_revision'), nullable=True, amis_form_item='', amis_table_column='')
    last_job_run: Optional[str] = models.Field(default=None, title=_('last_job_run'), nullable=True, amis_form_item='', amis_table_column='')
    last_job_failed: Optional[int] = models.Field(default=None, title=_('last_job_failed'), nullable=True, amis_form_item='', amis_table_column='')
    next_job_run: Optional[str] = models.Field(default=None, title=_('next_job_run'), nullable=True, amis_form_item='', amis_table_column='')
    status: Optional[str] = models.Field(default=None, title=_('status'), nullable=True, amis_form_item='', amis_table_column='')
    organization_id: Optional[int] = models.Field(default=None, title=_('organization_id'), nullable=True, amis_form_item='', amis_table_column='')
    scm_update_on_launch: Optional[int] = models.Field(default=None, title=_('scm_update_on_launch'), nullable=True, amis_form_item='', amis_table_column='')
    scm_update_cache_timeout: Optional[int] = models.Field(default=None, title=_('scm_update_cache_timeout'), nullable=True, amis_form_item='', amis_table_column='')
    allow_override: Optional[int] = models.Field(default=None, title=_('allow_override'), nullable=True, amis_form_item='', amis_table_column='')
    custom_virtualenv: Optional[str] = models.Field(default=None, title=_('custom_virtualenv'), nullable=True, amis_form_item='', amis_table_column='')
    last_update_failed: Optional[int] = models.Field(default=None, title=_('last_update_failed'), nullable=True, amis_form_item='', amis_table_column='')
    last_updated: Optional[str] = models.Field(default=None, title=_('last_updated'), nullable=True, amis_form_item='', amis_table_column='')
