#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

import sqlmodel

from utils.amis_admin import amis,models
from typing import TYPE_CHECKING,Optional, List
from apps.admin.models.basesqlmodel import BaseSQLModel
from core import i18n as _
from sqlmodel import Relationship

if TYPE_CHECKING:
    from .datasourceconfig import DatasourceConfig

if TYPE_CHECKING:
    from .dsmeta import DatasourceMeta

if TYPE_CHECKING:
    from .dspage import DatasourcePage

# Datasource Model
class Datasource(BaseSQLModel, table=True):
    __tablename__ = 'capricornus_datasource'
    ds_id: int = models.Field(default=None, title=_('DatasourceID'), primary_key=True, nullable=False)
    ds_name: str = models.Field(
        title=_('DatasourceName'),
        max_length=100,
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=True, index=True, nullable=False)
    )
    ds_uri: str = models.Field(title=_('URI'), max_length=256,
                               sa_column=sqlmodel.Column(sqlmodel.String(256), unique=False, index=False, nullable=False),
                               amis_form_item=amis.InputText(placeholder='mysql+aiomysql://root:bgt56yhn@127.0.0.1:3306/capricornus?charset=utf8mb4'))
    ds_schema: Optional[str] = models.Field(default='', title=_('Schema'), max_length=256, amis_form_item=amis.InputText(requiredOn='this.db_useschema==true'))
    ds_exclude_tablespaces: Optional[str] = models.Field(default='', title=_('ExcludedTableSpace'), max_length=256, amis_form_item=amis.InputText())
    ds_config_id: Optional[int] = models.Field(default=None, title=_('DatasourceConfigID'), foreign_key="capricornus_datasource_config.ds_config_id")
    datasourceconfig: "DatasourceConfig" = Relationship(back_populates="datasource")
    datasourcemetas: List["DatasourceMeta"] = Relationship(back_populates="dmdatasource")
    datasourcepages: List["DatasourcePage"] = Relationship(back_populates="dpdatasource")