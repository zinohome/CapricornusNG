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


class Car_parts(BaseSQLModel, table=True):
    __tablename__ = 'Car_Parts'
    part_name: str = models.Field(default='None', title='part_name', nullable=False, amis_form_item='', amis_table_column='')
    manufacture_plant_id: int = models.Field(default='None', title='manufacture_plant_id', nullable=False, amis_form_item='', amis_table_column='')
    manufacture_start_date: date = models.Field(default='None', title='manufacture_start_date', nullable=False, amis_form_item='', amis_table_column='')
    manufacture_end_date: Optional[date] = models.Field(default='None', title='manufacture_end_date', nullable=True, amis_form_item='', amis_table_column='')
    part_recall: Optional[int] = models.Field(default='0', title='part_recall', nullable=True, amis_form_item='', amis_table_column='')
    part_id: Optional[int] = models.Field(default='None', title='part_id', primary_key=True, amis_form_item='', amis_table_column='')
