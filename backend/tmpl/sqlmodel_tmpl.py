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
from utils.amis_admin import models
from typing import Optional
import sqlmodel

class BaseSQLModel(sqlmodel.SQLModel):
    class Config:
        use_enum_values = True
        orm_mode = True
        arbitrary_types_allowed = True

class {{ meta_name|trim|capitalize }}(BaseSQLModel, table=True):
    __tablename__ = '{{ meta_name }}'
{% for column_define in meta_columns %}
{% if meta_primarykeys|trim|length >0 %}
    {% if column_define.nullable == 'True' %}
        {% if column_define.primary_key | int > 0 %}
    {{column_define.name}}: Optional[{{column_define.pythonType}}] = models.Field(default={{column_define.default}}, title='{{column_define.title}}', primary_key=True, amis_form_item='{{column_define.amis_form_item}}', amis_table_column='{{column_define.amis_table_column}}')
        {% else %}
    {{column_define.name}}: Optional[{{column_define.pythonType}}] = models.Field(default={{column_define.default}}, title='{{column_define.title}}', nullable=True, amis_form_item='{{column_define.amis_form_item}}', amis_table_column='{{column_define.amis_table_column}}')
        {% endif %}
    {% else %}
        {% if column_define.primary_key | int > 0 %}
    {{column_define.name}}: Optional[{{column_define.pythonType}}] = models.Field(default={{column_define.default}}, title='{{column_define.title}}', primary_key=True, amis_form_item='{{column_define.amis_form_item}}', amis_table_column='{{column_define.amis_table_column}}')
        {% else %}
    {{column_define.name}}: {{column_define.pythonType}} = models.Field(default={{column_define.default}}, title='{{column_define.title}}', nullable=False, amis_form_item='{{column_define.amis_form_item}}', amis_table_column='{{column_define.amis_table_column}}')
        {% endif %}
    {% endif %}
{% else %}
{% set lklist = page_logicprimarykeys.split(',') %}
{% if column_define.nullable == 'True' %}
        {% if column_define.name|trim in lklist %}
    {{column_define.name}}: Optional[{{column_define.pythonType}}] = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', primary_key=True)
        {% else %}
    {{column_define.name}}: Optional[{{column_define.pythonType}}] = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', nullable=True)
        {% endif %}
    {% else %}
        {% if column_define.name|trim in lklist %}
    {{column_define.name}}: Optional[{{column_define.pythonType}}] = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', primary_key=True)
        {% else %}
    {{column_define.name}}: {{column_define.pythonType}} = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', nullable=False)
        {% endif %}
    {% endif %}
{% endif %}
{% endfor %}