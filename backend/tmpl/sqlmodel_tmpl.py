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
from fastapi_amis_admin import models
from typing import Optional
from apps.dmodels.basesqlmodel import BaseSQLModel


class {{ name|trim|capitalize }}(BaseSQLModel, table=True):
    __tablename__ = '{{ name }}'
{% for column_name, column_define in columns.items() %}
{% if primarykeys|trim|length >0 %}
    {% if column_define.nullable == 'True' %}
        {% if column_define.primary_key | int > 0 %}
    {{column_name}}: Optional[{{column_define.pythonType}}] = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', primary_key=True)
        {% else %}
    {{column_name}}: Optional[{{column_define.pythonType}}] = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', nullable=True)
        {% endif %}
    {% else %}
        {% if column_define.primary_key | int > 0 %}
    {{column_name}}: Optional[{{column_define.pythonType}}] = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', primary_key=True)
        {% else %}
    {{column_name}}: {{column_define.pythonType}} = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', nullable=False)
        {% endif %}
    {% endif %}
{% else %}
{% set lklist = logicprimarykeys.split(',') %}
{% if column_define.nullable == 'True' %}
        {% if column_define.name|trim in lklist %}
    {{column_name}}: Optional[{{column_define.pythonType}}] = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', primary_key=True)
        {% else %}
    {{column_name}}: Optional[{{column_define.pythonType}}] = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', nullable=True)
        {% endif %}
    {% else %}
        {% if column_define.name|trim in lklist %}
    {{column_name}}: Optional[{{column_define.pythonType}}] = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', primary_key=True)
        {% else %}
    {{column_name}}: {{column_define.pythonType}} = models.Field(default='{{column_define.default}}', title='{{column_define.title}}', nullable=False)
        {% endif %}
    {% endif %}
{% endif %}
{% endfor %}