#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus


class TableSchema(object):
    def __init__(self, id, table_name, table_type):
        self._id = id
        self._name = table_name
        self._table_type = table_type
        self._dbconn_id = None
        self._table_schema = None
        self._primarykeys = None
        self._indexes = None
        self._columns = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def dbconn_id(self):
        return self._dbconn_id

    @dbconn_id.setter
    def dbconn_id(self, value):
        self._dbconn_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def table_type(self):
        return self._table_type

    @table_type.setter
    def table_type(self, value):
        self._table_type = value

    @property
    def table_schema(self):
        return self._table_schema

    @table_schema.setter
    def table_schema(self, value):
        self._table_schema = value

    @property
    def primarykeys(self):
        return self._primarykeys

    @primarykeys.setter
    def primarykeys(self, value):
        self._primarykeys = value

    @primarykeys.deleter
    def primarykeys(self):
        self._primarykeys = None

    @property
    def indexes(self):
        return self._indexes

    @indexes.setter
    def indexes(self, value):
        self._indexes = value

    @indexes.deleter
    def indexes(self):
        self._indexes = None

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value

    @columns.deleter
    def columns(self):
        self._columns = None

    @property
    def json(self):
        return {
            '_id': self._id,
            'dbconn_id': self._dbconn_id,
            'name': self._name,
            'table_type': self._table_type,
            'table_schema': self._table_schema,
            'primarykeys': self._primarykeys,
            'indexes': self._indexes,
            'columns': self._columns
        }

    def getColumnType(self, Columename):
        rType = 'None'
        for column in self.columns.values():
            if column['name'] == Columename:
                rType = column['type']
                rType = rType[:rType.find("(")] if rType.find("(") > -1 else rType
                return rType

