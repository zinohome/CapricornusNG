#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus


class MetaSchema(object):
    def __init__(self, meta_id, meta_name, meta_type):
        self._meta_id = meta_id
        self._meta_name = meta_name
        self._meta_type = meta_type
        self._ds_id = None
        self._meta_schema = None
        self._meta_primarykeys = None
        self._meta_indexes = None
        self._meta_columns = None

    @property
    def meta_id(self):
        return self._meta_id

    @meta_id.setter
    def meta_id(self, value):
        self._meta_id = value

    @property
    def ds_id(self):
        return self._ds_id

    @ds_id.setter
    def ds_id(self, value):
        self._ds_id = value

    @property
    def meta_name(self):
        return self._meta_name

    @meta_name.setter
    def meta_name(self, value):
        self._meta_name = value

    @property
    def meta_type(self):
        return self._meta_type

    @meta_type.setter
    def meta_type(self, value):
        self._meta_type = value

    @property
    def meta_schema(self):
        return self._meta_schema

    @meta_schema.setter
    def meta_schema(self, value):
        self._meta_schema = value

    @property
    def meta_primarykeys(self):
        return self._meta_primarykeys

    @meta_primarykeys.setter
    def meta_primarykeys(self, value):
        self._meta_primarykeys = value

    @property
    def meta_indexes(self):
        return self._meta_indexes

    @meta_indexes.setter
    def meta_indexes(self, value):
        self._meta_indexes = value

    @property
    def meta_columns(self):
        return self._meta_columns

    @meta_columns.setter
    def meta_columns(self, value):
        self._meta_columns = value

    @property
    def json(self):
        return {
            'meta_id': self._meta_id,
            'ds_id': self._ds_id,
            'meta_name': self._meta_name,
            'meta_type': self._meta_type,
            'meta_schema': self._meta_schema,
            'meta_primarykeys': self._meta_primarykeys,
            'meta_indexes': self._meta_indexes,
            'meta_columns': self._meta_columns
        }

    def getColumnType(self, Columename):
        rType = 'None'
        for column in self.meta_columns.values():
            if column['name'] == Columename:
                rType = column['type']
                rType = rType[:rType.find("(")] if rType.find("(") > -1 else rType
                return rType

