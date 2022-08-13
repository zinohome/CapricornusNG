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


class Sqlite_sequence(BaseSQLModel, table=True):
    __tablename__ = 'sqlite_sequence'
    name: Optional[str] = models.Field(default='None', title='name', nullable=True)
    seq: Optional[str] = models.Field(default='None', title='seq', nullable=True)
