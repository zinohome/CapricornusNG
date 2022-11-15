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

class Dealer_brand(BaseSQLModel, table=True):
    __tablename__ = 'Dealer_Brand'
    dealer_id: Optional[int] = models.Field(default=None, title='dealer_id', primary_key=True, amis_form_item='', amis_table_column='')
    brand_id: Optional[int] = models.Field(default=None, title='brand_id', primary_key=True, amis_form_item='', amis_table_column='')
