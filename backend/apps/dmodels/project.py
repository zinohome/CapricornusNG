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
    name: str = models.Field(default=None, title=_('name'), nullable=False, amis_form_item='', amis_table_column='')
    description: Optional[str] = models.Field(default=None, title=_('description'), nullable=True, amis_form_item='', amis_table_column='')
    scm_type: Optional[str] = models.Field(default=None, title=_('scm_type'), nullable=True, amis_form_item='', amis_table_column='')
    scm_url: Optional[str] = models.Field(default=None, title=_('scm_url'), nullable=True, amis_form_item='', amis_table_column='')
    scm_branch: Optional[str] = models.Field(default=None, title=_('scm_branch'), nullable=True, amis_form_item='', amis_table_column='')
    credential_id: Optional[int] = models.Field(default=None, title=_('credential_id'), nullable=True, amis_form_item='', amis_table_column='')
    organization_id: Optional[int] = models.Field(default=None, title=_('organization_id'), nullable=True, amis_form_item='', amis_table_column='')
    allow_override: Optional[int] = models.Field(default=None, title=_('allow_override'), nullable=True, amis_form_item='', amis_table_column='')
    created: Optional[str] = models.Field(default=None, title=_('created'), nullable=True, amis_form_item='', amis_table_column='')
    modified: Optional[str] = models.Field(default=None, title=_('modified'), nullable=True, amis_form_item='', amis_table_column='')
    status: Optional[str] = models.Field(default=None, title=_('status'), nullable=True, amis_form_item='', amis_table_column='')
    awx_project_id: Optional[int] = models.Field(default=None, title=_('awx_project_id'), nullable=True, amis_form_item='', amis_table_column='')
    git_repo_id: Optional[int] = models.Field(default=None, title=_('git_repo_id'), nullable=True, amis_form_item='', amis_table_column='')
