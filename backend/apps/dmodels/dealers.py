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


class Dealers(BaseSQLModel, table=True):
    __tablename__ = 'Dealers'
    dealer_name: str = models.Field(default='None', title='dealer_name', nullable=False)
    dealer_address: Optional[str] = models.Field(default='None', title='dealer_address', nullable=True)
    dealer_id: Optional[int] = models.Field(default='None', title='dealer_id', primary_key=True)
