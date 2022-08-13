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


class Manufacture_plant(BaseSQLModel, table=True):
    __tablename__ = 'Manufacture_Plant'
    plant_name: str = models.Field(default='None', title='plant_name', nullable=False)
    plant_type: Optional[str] = models.Field(default='None', title='plant_type', nullable=True)
    plant_location: Optional[str] = models.Field(default='None', title='plant_location', nullable=True)
    company_owned: Optional[int] = models.Field(default='None', title='company_owned', nullable=True)
    manufacture_plant_id: Optional[int] = models.Field(default='None', title='manufacture_plant_id', primary_key=True)
