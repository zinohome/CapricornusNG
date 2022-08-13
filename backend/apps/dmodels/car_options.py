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


class Car_options(BaseSQLModel, table=True):
    __tablename__ = 'Car_Options'
    model_id: Optional[int] = models.Field(default='None', title='model_id', nullable=True)
    engine_id: int = models.Field(default='None', title='engine_id', nullable=False)
    transmission_id: int = models.Field(default='None', title='transmission_id', nullable=False)
    chassis_id: int = models.Field(default='None', title='chassis_id', nullable=False)
    premium_sound_id: Optional[int] = models.Field(default='None', title='premium_sound_id', nullable=True)
    color: str = models.Field(default='None', title='color', nullable=False)
    option_set_price: int = models.Field(default='None', title='option_set_price', nullable=False)
    option_set_id: Optional[int] = models.Field(default='None', title='option_set_id', primary_key=True)
