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

import simplejson as json
from fastapi_amis_admin import amis,models
from typing import TYPE_CHECKING,Optional, Dict, Any, List
from apps.admin.models.basesqlmodel import BaseSQLModel
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _
from sqlmodel import Relationship

if TYPE_CHECKING:
    from .dbconfig import DBConfig

if TYPE_CHECKING:
    from .tablemeta import TableMeta

if TYPE_CHECKING:
    from .tablepage import TablePage

# DBConnection Model
class DBConnection(BaseSQLModel, table=True):
    __tablename__ = 'capricornus_db_connection'
    conn_id: int = models.Field(default=None, title='ID', primary_key=True, nullable=False)
    name: str = models.Field(
        title='ConnectName',
        max_length=100,
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=True, index=True, nullable=False)
    )
    db_uri: str = models.Field(title='URI', max_length=256,
                               sa_column=sqlmodel.Column(sqlmodel.String(256), unique=False, index=False, nullable=False),
                               amis_form_item=amis.InputText(placeholder='mysql+aiomysql://root:bgt56yhn@127.0.0.1:3306/capricornus?charset=utf8mb4'))
    db_useschema: bool = models.Field(default=False, title='UseSchema')
    db_schema: Optional[str] = models.Field(default='', title='Schema', max_length=256, amis_form_item=amis.InputText(requiredOn='this.db_useschema==true'))
    db_exclude_tablespaces: Optional[str] = models.Field(default='', title='ExcludedTableSpace', max_length=256, amis_form_item=amis.InputText())
    db_conf_id: int = models.Field(title='Config', nullable=False, foreign_key="capricornus_db_config.config_id")
    dbconfig: "DBConfig" = Relationship(back_populates="dbconnection")
    tablemetas: List["TableMeta"] = Relationship(back_populates="tmdbconnection")
    tablepages: List["TablePage"] = Relationship(back_populates="tpdbconnection")