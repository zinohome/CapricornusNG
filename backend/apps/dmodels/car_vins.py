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


class Car_vins(BaseSQLModel, table=True):
    __tablename__ = 'Car_Vins'
    model_id: int = models.Field(default='None', title='model_id', nullable=False)
    option_set_id: int = models.Field(default='None', title='option_set_id', nullable=False)
    manufactured_date: date = models.Field(default='None', title='manufactured_date', nullable=False)
    manufactured_plant_id: int = models.Field(default='None', title='manufactured_plant_id', nullable=False)
    vin: Optional[int] = models.Field(default='None', title='vin', primary_key=True)
