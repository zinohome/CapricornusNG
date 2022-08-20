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


class Customers(BaseSQLModel, table=True):
    __tablename__ = 'Customers'
    first_name: str = models.Field(default=None, title='first_name', nullable=False, amis_form_item='', amis_table_column='')
    last_name: str = models.Field(default=None, title='last_name', nullable=False, amis_form_item='', amis_table_column='')
    gender: Optional[str] = models.Field(default=None, title='gender', nullable=True, amis_form_item='', amis_table_column='')
    household_income: Optional[int] = models.Field(default=None, title='household_income', nullable=True, amis_form_item='', amis_table_column='')
    birthdate: date = models.Field(default=None, title='birthdate', nullable=False, amis_form_item='', amis_table_column='')
    phone_number: int = models.Field(default=None, title='phone_number', nullable=False, amis_form_item='', amis_table_column='')
    email: Optional[str] = models.Field(default=None, title='email', nullable=True, amis_form_item='', amis_table_column='')
    customer_id: Optional[int] = models.Field(default=None, title='customer_id', primary_key=True, amis_form_item='', amis_table_column='')
