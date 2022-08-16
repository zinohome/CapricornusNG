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
from sqlmodel import Relationship, Column, JSON

default_application_params = "{\"app_name\": \"Capricornus\", \"app_version\": \"v2.1.5\", \"app_description\": \"REST API for RDBMS\", \"app_prefix\": \"/api/v2\", \"app_cors_origins\": \"'*'\", \"app_service_model\": \"Standalone\", \"app_param_prefix\": \"up_b_\", \"app_force_generate_meta\": false, \"app_log_level\": \"INFO\", \"app_user_func\": true, \"app_exception_detail\": true, \"app_admin_use_https\": false, \"app_confirm_key\": \"Confirmed\", \"app_http_port\": 8880, \"app_https_port\": 8843, \"app_http_timeout\": 10, \"app_load_metadat_on_load\": true, \"app_clear_metadat_on_startup\": true, \"app_clear_metadat_on_shutdown\": true}"
default_connection_params = "{\"con_pool_size\": 20, \"con_max_overflow\": 5, \"con_pool_use_lifo\": true, \"con_pool_pre_ping\": true, \"con_pool_recycle\": 3600}"
default_schema_params = "{\"schema_cache_enabled\": true, \"schema_model_refresh\": true, \"schema_cache_filename\": \"capricornus_metadata\", \"schema_db_metafile\": \"metadata.json\", \"schema_db_logicpkfile\": \"logicpk.json\", \"schema_db_logicpkneedfile\": \"logicpk-need.json\", \"schema_fetch_all_table\": true, \"schema_fetch_tables\": \"table1, table2\"}"
default_query_params = "{\"query_limit_upset\": 2000, \"query_default_limit\": 10, \"query_default_offset\": 0}"
default_admin_params = "{\"DEBUG\": true, \"SECRET_KEY\": \"bgt56yh@Passw0rd\", \"SESSION_COOKIE_HTTPONLY\": true, \"REMEMBER_COOKIE_HTTPONLY\": true, \"REMEMBER_COOKIE_DURATION\": 3600, \"admin_ignore_primary_key\": false}"
default_security_params = "{\"security_key\": \"47051d5e3bafcfcba3c80d6d1119a7adf78d2967a8972b00af1ea231ca61f589\", \"security_algorithm\": \"HS256\", \"access_token_expire_minutes\": 30}"

if TYPE_CHECKING:
    from .dbconnection import DBConnection

# DBConfig Model
class DBConfig(BaseSQLModel, table=True):
    __tablename__ = 'capricornus_db_config'
    config_id: int = models.Field(default=None, title='ID', primary_key=True, nullable=False)
    name: str = models.Field(
        title='ConfigName',
        max_length=100,
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=True, index=True, nullable=False)
    )
    application_params: Optional[dict] = models.Field(index=False, default=json.loads(default_application_params),sa_column=Column(JSON),
                                                     title='ApplicationParams',
                                                     amis_form_item=amis.Combo(type='combo', items=[amis.InputText(name='app_name', label='app_name', disabled=True),
                                                                                                 amis.InputText(name='app_version', label='app_version', disabled=True),
                                                                                                 amis.InputText(name='app_description', label='app_description', disabled=True),
                                                                                                 amis.InputText(name='app_prefix', label='app_prefix'),
                                                                                                 amis.InputText(name='app_cors_origins', label='app_cors_origins'),
                                                                                                 amis.InputText(name='app_service_model', label='app_service_model', type='list-select', options=[{'label':'Standalone','value':'Standalone'},{'label':'OpenReader','value':'OpenReader'},{'label':'OpenWriter','value':'OpenWriter'}]),
                                                                                                 amis.InputText(name='app_param_prefix', label='app_param_prefix'),
                                                                                                 amis.InputText(name='app_force_generate_meta', label='app_force_generate_meta', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='app_log_level', label='app_log_level', type='list-select', options=[{'label':'DEBUG','value':'DEBUG'},{'label':'INFO','value':'INFO'},{'label':'ERROR','value':'ERROR'}]),
                                                                                                 amis.InputText(name='app_user_func', label='app_user_func', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='app_exception_detail', label='app_exception_detail', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='app_admin_use_https', label='app_admin_use_https', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='app_confirm_key', label='app_confirm_key'),
                                                                                                 amis.InputNumber(name='app_http_port', label='app_http_port'),
                                                                                                 amis.InputNumber(name='app_https_port', label='app_https_port'),
                                                                                                 amis.InputNumber(name='app_http_timeout', label='app_http_timeout'),
                                                                                                 amis.InputText(name='app_load_metadat_on_load', label='app_load_metadat_on_load', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='app_clear_metadat_on_startup', label='app_clear_metadat_on_startup', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='app_clear_metadat_on_shutdown', label='app_clear_metadat_on_shutdown', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}])],
                                                                            canAccessSuperData=True, tabsMode=True, multiLine=True),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    connection_params: Optional[dict] = models.Field(index=False, default=json.loads(default_connection_params),sa_column=Column(JSON),
                                                    title='ConnectionParams',
                                                    amis_form_item=amis.Combo(type='combo', items=[amis.InputNumber(name='con_pool_size', label='con_pool_size'),
                                                                                                 amis.InputNumber(name='con_max_overflow', label='con_max_overflow'),
                                                                                                 amis.InputText(name='con_pool_use_lifo', label='con_pool_use_lifo', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='con_pool_pre_ping', label='con_pool_pre_ping', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputNumber(name='con_pool_recycle', label='con_pool_recycle')],
                                                                            canAccessSuperData=True, tabsMode=True, multiLine=True),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    schema_params: Optional[dict] = models.Field(index=False, default=json.loads(default_schema_params),sa_column=Column(JSON),
                                                title='SchemaParams',
                                                amis_form_item=amis.Combo(type='combo', items=[amis.InputText(name='schema_cache_enabled', label='schema_cache_enabled', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='schema_model_refresh', label='schema_model_refresh', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='schema_cache_filename', label='schema_cache_filename', disabled=True),
                                                                                                 amis.InputText(name='schema_db_metafile', label='schema_db_metafile', disabled=True),
                                                                                                 amis.InputText(name='schema_db_logicpkfile', label='schema_db_logicpkfile', disabled=True),
                                                                                                 amis.InputText(name='schema_db_logicpkneedfile', label='schema_db_logicpkneedfile', disabled=True),
                                                                                                 amis.InputText(name='schema_fetch_all_table', label='schema_fetch_all_table', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='schema_fetch_tables', label='schema_fetch_tables', validations={"matchRegexp":"^[^\s,]+(?:,\s*[^\s,]+)*$"}, validationErrors={'matchRegexp':_("Please enter the comma-separated table name")})],
                                                                            canAccessSuperData=True, tabsMode=True, multiLine=True),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    query_params: Optional[dict] = models.Field(index=False, default=json.loads(default_query_params),sa_column=Column(JSON),
                                               title='QueryParams',
                                               amis_form_item=amis.Combo(type='combo', items=[amis.InputNumber(name='query_limit_upset', label='query_limit_upset'),
                                                                                                 amis.InputNumber(name='query_default_limit', label='query_default_limit'),
                                                                                                 amis.InputNumber(name='query_default_offset', label='query_default_offset')],
                                                                            canAccessSuperData=True, tabsMode=True, multiLine=True),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    admin_params: Optional[dict] = models.Field(index=False, default=json.loads(default_admin_params),sa_column=Column(JSON),
                                               title='AdminParams',
                                               amis_form_item=amis.Combo(type='combo', items=[amis.InputText(name='DEBUG', label='DEBUG', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='SECRET_KEY', label='SECRET_KEY'),
                                                                                                 amis.InputText(name='SESSION_COOKIE_HTTPONLY', label='SESSION_COOKIE_HTTPONLY', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputText(name='REMEMBER_COOKIE_HTTPONLY', label='REMEMBER_COOKIE_HTTPONLY', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}]),
                                                                                                 amis.InputNumber(name='REMEMBER_COOKIE_DURATION', label='REMEMBER_COOKIE_DURATION'),
                                                                                                 amis.InputText(name='admin_ignore_primary_key', label='admin_ignore_primary_key', type='list-select', options=[{'label':'True','value':True},{'label':'False','value':False}])],
                                                                            canAccessSuperData=True, tabsMode=True, multiLine=True),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    security_params: Optional[dict] = models.Field(index=False, default=json.loads(default_security_params),sa_column=Column(JSON),
                                                  title='SecurityParams',
                                                  amis_form_item=amis.Combo(type='combo', items=[amis.InputText(name='security_key', label='security_key'),
                                                                                                 amis.InputText(name='security_algorithm', label='security_algorithm', disabled=True),
                                                                                                 amis.InputNumber(name='access_token_expire_minutes', label='access_token_expire_minutes')],
                                                                            canAccessSuperData=True, tabsMode=True, multiLine=True),
                                                     amis_table_column=amis.TableColumn(type='json', levelExpand=0))
    dbconnection: "DBConnection" = Relationship(back_populates="dbconfig")
