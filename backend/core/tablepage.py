#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus


class TablePageSchema(object):
    def __init__(self, page_id, table_name, table_type):
        self._page_id = page_id
        self._name = table_name
        self._label = None
        self._table_type = table_type
        self._dbconn_id = None
        self._table_schema = None
        self._primarykeys = None
        self._logicprimarykeys = None
        self._indexes = None
        self._list_display = None
        self._search_fields = None
        self._columns = None

    @property
    def page_id(self):
        return self._page_id

    @page_id.setter
    def page_id(self, value):
        self._page_id = value

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
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

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
    def logicprimarykeys(self):
        return self._logicprimarykeys

    @logicprimarykeys.setter
    def logicprimarykeys(self, value):
        self._logicprimarykeys = value

    @logicprimarykeys.deleter
    def logicprimarykeys(self):
        self._logicprimarykeys = None

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
    def list_display(self):
        return self._list_display

    @list_display.setter
    def list_display(self, value):
        self._list_display = value

    @list_display.deleter
    def list_display(self):
        self._list_display = None

    @property
    def search_fields(self):
        return self._search_fields

    @search_fields.setter
    def search_fields(self, value):
        self._search_fields = value

    @search_fields.deleter
    def search_fields(self):
        self._search_fields = None

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
            'page_id': self._page_id,
            'dbconn_id': self._dbconn_id,
            'name': self._name,
            'label': self._label,
            'table_type': self._table_type,
            'table_schema': self._table_schema,
            'primarykeys': self._primarykeys,
            'logicprimarykeys': self._logicprimarykeys,
            'indexes': self._indexes,
            'list_display': self._list_display,
            'search_fields': self._search_fields,
            'columns': self._columns
        }

    def getColumnType(self, Columename):
        rType = 'None'
        for column in self.columns.values():
            if column['name'] == Columename:
                rType = column['type']
                rType = rType[:rType.find("(")] if rType.find("(") > -1 else rType
                return rType

