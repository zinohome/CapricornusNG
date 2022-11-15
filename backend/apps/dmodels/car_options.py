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

class Car_options(BaseSQLModel, table=True):
    __tablename__ = 'Car_Options'
    model_id: Optional[int] = models.Field(default=None, title='model_id', nullable=True, amis_form_item='', amis_table_column='')
    engine_id: int = models.Field(default=None, title='engine_id', nullable=False, amis_form_item='', amis_table_column='')
    transmission_id: int = models.Field(default=None, title='transmission_id', nullable=False, amis_form_item='', amis_table_column='')
    chassis_id: int = models.Field(default=None, title='chassis_id', nullable=False, amis_form_item='', amis_table_column='')
    premium_sound_id: Optional[int] = models.Field(default=None, title='premium_sound_id', nullable=True, amis_form_item='', amis_table_column='')
    color: str = models.Field(default=None, title='color', nullable=False, amis_form_item='', amis_table_column='')
    option_set_price: int = models.Field(default=None, title='option_set_price', nullable=False, amis_form_item='', amis_table_column='')
    option_set_id: Optional[int] = models.Field(default=None, title='option_set_id', primary_key=True, amis_form_item='', amis_table_column='')
