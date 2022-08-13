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


class Brands(BaseSQLModel, table=True):
    __tablename__ = 'Brands'
    brand_name: str = models.Field(default='None', title='brand_name', nullable=False)
    brand_id: Optional[int] = models.Field(default='None', title='brand_id', primary_key=True)
