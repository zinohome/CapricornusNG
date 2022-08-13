#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

from datetime import datetime, date
import sqlmodel
from fastapi_amis_admin import amis,models
from fastapi_amis_admin.models import TextChoices
from typing import Optional, Dict, Any, List
import simplejson as json
from sqlmodel import Column, JSON
from sqlmodel import Relationship
from pydantic import BaseModel as requestBaseModel
from apps.admin.dmodels.basesqlmodel import BaseSQLModel
from util.log import log as log
from fastapi_amis_admin.utils.translation import i18n as _

class Car_Parts(BaseSQLModel, table=True):
    __tablename__ = 'Car_Parts'
    part_id: Optional[int] = models.Field(default=None, title='Part ID', primary_key=True, nullable=False)
    part_name: str = models.Field(default=None, title='Part Name', nullable=False)
    manufacture_plant_id: int = models.Field(default=None, title='Manufacture Plant ID', nullable=False)
    manufacture_start_date:  date= models.Field(default=None, title='Manufacture Start Date', nullable=False)
    manufacture_end_date: Optional[date] = models.Field(default=None, title='Manufacture End Date', nullable=True)
    part_recall: Optional[int] = models.Field(default=0, title='Part Recall', nullable=True)