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
import sqlmodel

class BaseSQLModel(sqlmodel.SQLModel):
    class Config:
        use_enum_values = True
        orm_mode = True
        arbitrary_types_allowed = True

class Manufacture_plant(BaseSQLModel, table=True):
    __tablename__ = 'Manufacture_Plant'
    plant_name: str = models.Field(default=None, title='plant_name', nullable=False, amis_form_item='', amis_table_column='')
    plant_type: Optional[str] = models.Field(default=None, title='plant_type', nullable=True, amis_form_item='', amis_table_column='')
    plant_location: Optional[str] = models.Field(default=None, title='plant_location', nullable=True, amis_form_item='', amis_table_column='')
    company_owned: Optional[int] = models.Field(default=None, title='company_owned', nullable=True, amis_form_item='', amis_table_column='')
    manufacture_plant_id: Optional[int] = models.Field(default=None, title='manufacture_plant_id', primary_key=True, amis_form_item='', amis_table_column='')
