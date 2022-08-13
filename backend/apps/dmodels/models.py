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


class Models(BaseSQLModel, table=True):
    __tablename__ = 'Models'
    model_name: str = models.Field(default='None', title='model_name', nullable=False)
    model_base_price: int = models.Field(default='None', title='model_base_price', nullable=False)
    brand_id: int = models.Field(default='None', title='brand_id', nullable=False)
    model_id: Optional[int] = models.Field(default='None', title='model_id', primary_key=True)
