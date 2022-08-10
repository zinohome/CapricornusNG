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
    def __init__(self, conn_id, table_name, table_type):
        self._conn_id = conn_id
        self._name = table_name
        self._table_Type = table_type
        self._table_schema = 'N/A'
        self._primarykeys = 'N/A'
        self._logicprimarykeys = 'N/A'
        self._indexes = 'N/A'
        self._columns = 'N/A'
        self._pagedefine = 'N/A'

    @property
    def conn_id(self):
        return self._conn_id

    @conn_id.setter
    def conn_id(self, value):
        self._conn_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def table_Type(self):
        return self._table_Type

    @table_Type.setter
    def table_Type(self, value):
        self._table_Type = value

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
        self._primarykeys = 'N/A'

    @property
    def logicprimarykeys(self):
        return self._logicprimarykeys

    @logicprimarykeys.setter
    def logicprimarykeys(self, value):
        self._logicprimarykeys = value

    @logicprimarykeys.deleter
    def logicprimarykeys(self):
        self._logicprimarykeys = 'N/A'

    @property
    def indexes(self):
        return self._indexes

    @indexes.setter
    def indexes(self, value):
        self._indexes = value

    @indexes.deleter
    def indexes(self):
        self._indexes = 'N/A'

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value

    @columns.deleter
    def columns(self):
        self._columns = 'N/A'

    @property
    def pagedefine(self):
        return self._pagedefine

    @pagedefine.setter
    def pagedefine(self, value):
        self._pagedefine = value

    @pagedefine.deleter
    def pagedefine(self):
        self._pagedefine = 'N/A'

    @property
    def json(self):
        return {
            'conn_id': self.conn_id,
            'name': self._name,
            'table_type': self._table_type,
            'table_schema': self._table_schema,
            'primarykeys': self._primarykeys,
            'logicprimarykeys': self._logicprimarykeys,
            'indexes': self._indexes,
            'columns': self._columns,
            'pagedefine': self._pagedefine
        }

    def getColumnType(self, Columename):
        rType = 'None'
        for column in self.columns:
            if column['name'] == Columename:
                rType = column['type']
                rType = rType[:rType.find("(")] if rType.find("(") > -1 else rType
                return rType
