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

class Car_vins(BaseSQLModel, table=True):
    __tablename__ = 'Car_Vins'
    model_id: int = models.Field(default=None, title='model_id', nullable=False, amis_form_item='', amis_table_column='')
    option_set_id: int = models.Field(default=None, title='option_set_id', nullable=False, amis_form_item='', amis_table_column='')
    manufactured_date: date = models.Field(default=None, title='manufactured_date', nullable=False, amis_form_item='', amis_table_column='')
    manufactured_plant_id: int = models.Field(default=None, title='manufactured_plant_id', nullable=False, amis_form_item='', amis_table_column='')
    vin: Optional[int] = models.Field(default=None, title='vin', primary_key=True, amis_form_item='', amis_table_column='')
