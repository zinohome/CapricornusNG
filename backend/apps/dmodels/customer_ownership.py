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


class Customer_ownership(BaseSQLModel, table=True):
    __tablename__ = 'Customer_Ownership'
    purchase_date: date = models.Field(default='None', title='purchase_date', nullable=False)
    purchase_price: int = models.Field(default='None', title='purchase_price', nullable=False)
    warantee_expire_date: Optional[date] = models.Field(default='None', title='warantee_expire_date', nullable=True)
    dealer_id: int = models.Field(default='None', title='dealer_id', nullable=False)
    customer_id: Optional[int] = models.Field(default='None', title='customer_id', primary_key=True)
    vin: Optional[int] = models.Field(default='None', title='vin', primary_key=True)
