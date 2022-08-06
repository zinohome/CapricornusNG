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
from fastapi_amis_admin import amis,models
from fastapi_amis_admin.models import TextChoices
from typing import Optional, Dict, Any
import simplejson as json
from sqlmodel import Column, JSON
from sqlmodel import Relationship

default_application_params = "{\"app_name\": \"Capricornus\", \"app_version\": \"v2.1.5\", \"app_description\": \"REST API for RDBMS\", \"app_prefix\": \"/api/v2\", \"app_cors_origins\": \"'*'\", \"app_service_model\": \"Standalone\", \"app_param_prefix\": \"up_b_\", \"app_force_generate_meta\": true, \"app_log_level\": \"INFO\", \"app_user_func\": true, \"app_exception_detail\": true, \"app_admin_use_https\": false, \"app_confirm_key\": \"Confirmed\", \"app_http_port\": 8880, \"app_https_port\": 8843, \"app_http_timeout\": 10, \"app_load_metadat_on_load\": true, \"app_clear_metadat_on_startup\": true, \"app_clear_metadat_on_shutdown\": true}"
default_connection_params = "{\"con_pool_size\": 20, \"con_max_overflow\": 5, \"con_pool_use_lifo\": true, \"con_pool_pre_ping\": true, \"con_pool_recycle\": 3600}"
default_schema_params = "{\"schema_cache_enabled\": true, \"schema_model_refresh\": true, \"schema_cache_filename\": \"capricornus_metadata\", \"schema_db_metafile\": \"metadata.json\", \"schema_db_logicpkfile\": \"logicpk.json\", \"schema_db_logicpkneedfile\": \"logicpk-need.json\", \"schema_fetch_all_table\": true, \"schema_fetch_tables\": \"table1, table2\"}"
default_query_params = "{\"query_limit_upset\": 2000, \"query_default_limit\": 10, \"query_default_offset\": 0}"
default_admin_params = "{\"DEBUG\": true, \"SECRET_KEY\": \"bgt56yh@Passw0rd\", \"SESSION_COOKIE_HTTPONLY\": true, \"REMEMBER_COOKIE_HTTPONLY\": true, \"REMEMBER_COOKIE_DURATION\": 3600, \"admin_ignore_primary_key\": false}"
default_security_params = "{\"security_key\": \"47051d5e3bafcfcba3c80d6d1119a7adf78d2967a8972b00af1ea231ca61f589\", \"security_algorithm\": \"HS256\", \"access_token_expire_minutes\": 30}"

# Create your models here.
class BaseSQLModel(sqlmodel.SQLModel):
    id: int = models.Field(default=None, title='ID', primary_key=True, nullable=False)
    class Config:
        use_enum_values = True
        orm_mode = True


# DBConnection Model
class DataBaseType(TextChoices):
    sqlite = 'sqlite', 'SQLite'
    mysql = 'mysql', 'MySQL/MariaDB'
    oracle = 'oracle', 'Oracle'
    postgresql = 'postgresql', 'PostgreSQL'

class DataBaseDialect(TextChoices):
    aiosqlite = 'aiosqlite', 'aiosqlite'
    aiomysql = 'aiomysql', 'aiomysql'
    cx_oracle = 'cx_oracle', 'cx_oracle'
    asyncpg = 'asyncpg', 'asyncpg'


class DBConnection(BaseSQLModel, table=True):
    __tablename__ = 'capricornus_db_connection'
    db_profilename: str = models.Field(
        title='Profile',
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=True, index=True, nullable=False)
    )
    db_Type: DataBaseType = models.Field(DataBaseType.mysql, title='Type')
    db_Dialect: DataBaseDialect = models.Field(DataBaseDialect.aiomysql, title='Dialect')
    db_uri: str = models.Field(default='', title='URI', max_length=256, amis_form_item=amis.InputText(placeholder='mysql+aiomysql://root:bgt56yhn@127.0.0.1:3306/capricornus?charset=utf8mb4'))
    db_useschema: bool = models.Field(None, title='UseSchema')
    db_schema: Optional[str] = models.Field(default='', title='Schema', max_length=256, amis_form_item=amis.InputText())
    db_exclude_tablespaces: Optional[str] = models.Field(default='', title='ExcludedTableSpace', max_length=256, amis_form_item=amis.InputText())
    db_conf_id: Optional[int] = models.Field(default=None, foreign_key="capricornus_db_config.id", title='Config')
    dbconfig: Optional["DBConfig"] = Relationship(back_populates="dbconnection")

# DBConfig Model
class DBConfig(BaseSQLModel, table=True):
    __tablename__ = 'capricornus_db_config'
    dbconnection: Optional[DBConnection] = Relationship(back_populates="dbconfig")
    application_params: Optional[str] = models.Field(index=False, default=default_application_params,
                                                     title='ApplicationParams',
                                                     amis_form_item=amis.Editor(language='json', allowFullscreen=False),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    connection_params: Optional[str] = models.Field(index=False, default=default_connection_params,
                                                    title='ConnectionParams',
                                                    amis_form_item=amis.Editor(language='json', allowFullscreen=False),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    schema_params: Optional[str] = models.Field(index=False, default=default_schema_params,
                                                title='SchemaParams',
                                                amis_form_item=amis.Editor(language='json', allowFullscreen=False),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    query_params: Optional[str] = models.Field(index=False, default=default_query_params,
                                               title='QueryParams',
                                               amis_form_item=amis.Editor(language='json', allowFullscreen=False),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    admin_params: Optional[str] = models.Field(index=False, default=default_admin_params,
                                               title='AdminParams',
                                               amis_form_item=amis.Editor(language='json', allowFullscreen=False),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    security_params: Optional[str] = models.Field(index=False, default=default_security_params,
                                                  title='SecurityParams',
                                                  amis_form_item=amis.Editor(language='json', allowFullscreen=False),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))


class Category(BaseSQLModel, table=True):
    __tablename__ = 'blog_category'
    name: str = models.Field(
        title='Category Name',
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=True, index=True, nullable=False)
    )
    description: str = models.Field(default='', title='Description', amis_form_item=amis.Textarea())
    is_active: bool = models.Field(None, title='Is Active')

