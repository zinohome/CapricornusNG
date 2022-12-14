#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

import ast
import operator
import re
from urllib import parse
import simplejson as json
import sqlalchemy.types as satypes
from sqlalchemy.engine.url import URL
from core.settings import settings
from utils.log import log as log
from datetime import datetime

type_sql2py_dict = {}
for key in satypes.__dict__['__all__']:
    sqltype = getattr(satypes, key)
    if 'python_type' in dir(sqltype) and not sqltype.__name__.startswith('Type'):
        try:
            typeinst = sqltype()
        except TypeError as e: #List/array wants inner-type
            typeinst = sqltype(None)
        try:
            type_sql2py_dict[sqltype.__name__] = typeinst.python_type
        except NotImplementedError:
            pass

type_py2sql_dict = {}
for key, val in type_sql2py_dict.items():
    if not val in type_py2sql_dict:
        type_py2sql_dict[val] = [key]
    else:
        type_py2sql_dict[val].append(key)

def is_dict(dictstr):
    if isinstance(dictstr, dict):
        return True
    else:
        try:
            ast.literal_eval(dictstr)
        except ValueError:
            return False
        return True


def to_dict(dictstr):
    if isinstance(dictstr, dict):
        return dictstr
    elif is_dict(dictstr):
        return ast.literal_eval(dictstr)
    else:
        return None


def is_json(jsonstr):
    try:
        json.loads(jsonstr)
    except ValueError:
        return False
    return True


def to_json(jsonstr):
    if is_json(jsonstr):
        return json.loads(jsonstr)
    else:
        return None

def jsonstrsort(jsonstr):
    jsonobj = json.loads(jsonstr)
    return json.dumps(jsonobj,sort_keys=True)


def is_list(lststr):
    try:
        re.split(r'[\s\,\;]+', lststr)
    except TypeError:
        return False
    return True


def to_list(lststr):
    if is_list(lststr):
        return re.split(r'[\s\,\;]+', lststr)
    else:
        return [lststr]


def is_fvcol(lststr):
    try:
        ast.literal_eval(lststr)
    except SyntaxError:
        return False
    return True


def to_fvcol(lststr):
    if is_fvcol(lststr):
        return ast.literal_eval(lststr)
    else:
        return None

def getpytype(sqltype):
    pytype = None
    if type_sql2py_dict.__contains__(sqltype):
        pytype = type_sql2py_dict[sqltype]
    return pytype

def convertSQLObject(vol, tableschema):
    cvol = vol.copy()
    for key in cvol.keys():
        if getpytype(tableschema.getColumnType(key)) is None:
            cvol[key] = cvol[key]
        else:
            if getpytype(tableschema.getColumnType(key)).__name__ == 'int':
                cvol[key] = int(cvol[key])
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'str':
                cvol[key] = str(cvol[key])
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'float':
                cvol[key] = float(cvol[key])
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'Decimal':
                cvol[key] = float(cvol[key])
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'datetime':
                cvol[key] = datetime.strptime(cvol[key], "%Y-%m-%d %H:%M:%S")
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'bytes':
                cvol[key] = bytes(cvol[key], encoding ="utf8")
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'bool':
                cvol[key] = json.loads(cvol[key].lower())
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'date':
                cvol[key] = datetime.strptime(cvol[key], "%Y-%m-%d")
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'time':
                cvol[key] = datetime.strptime(cvol[key], "%H:%M:%S")
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'timedelta':
                cvol[key] = cvol[key]
                #TODO:Add string to timedelta
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'list':
                cvol[key] = ast.literal_eval(cvol[key])
            elif getpytype(tableschema.getColumnType(key)).__name__ == 'dict':
                cvol[key] = ast.literal_eval(cvol[key])
            else:
                cvol[key] = cvol[key]
    return cvol

def validQueryJson(jsonstr):
    return True
    #TODO valid jsonstr from query parameter

def sync_uri(uri):
    db_sub, dialect_sub, drv_sub = uri.split(':')[0].split('+')[0].strip(), uri.split(':')[0].split('+')[1].strip(), '/'+uri.split(':/')[1].strip()
    sync_dialect_sub = ''
    if db_sub == 'sqlite':
        sync_dialect_sub = 'pysqlite'
    elif db_sub == 'mysql':
        sync_dialect_sub = 'pymysql'
    elif db_sub == 'oracle':
        sync_dialect_sub = 'cx_oracle'
    elif db_sub == 'postgresql':
        sync_dialect_sub = 'psycopg2'
    else:
        sync_dialect_sub = None
    if sync_dialect_sub is None:
        return None
    else:
        syncuri = f'{db_sub}+{sync_dialect_sub}:{drv_sub}'
    return syncuri

def get_db_type_from_uri(uri):
    db_sub = uri.split(':')[0].split('+')[0].strip()
    return db_sub

def get_db_dialect_from_uri(uri):
    db_sub = uri.split(':')[0].split('+')[1].strip()
    return db_sub

def get_first_primarykey(primarykeystr, logicprimarykeystr):
    pk = None
    if len(primarykeystr) > 0:
        pk = primarykeystr.split(',')[0]
    else:
        if len(logicprimarykeystr) >0:
            pk = logicprimarykeystr.split(',')[0]
        else:
            pk = None
    return pk

def get_updated_colums(updatecolumns, oldcolumns):
    rtncolumns = updatecolumns.copy()
    for column in rtncolumns:
        cmpcolumn = next((itm for (index, itm) in enumerate(oldcolumns) if itm['name'] == column['name']), None)
        if not cmpcolumn is None:
            if not operator.eq(column,cmpcolumn):
                column['title'] = cmpcolumn['title']
                column['amis_form_item'] = cmpcolumn['amis_form_item']
                column['amis_table_column'] = cmpcolumn['amis_table_column']
    return rtncolumns



if __name__ == '__main__':
    upcolumns = [{'name': 'dealer_name', 'type': 'VARCHAR(50)', 'nullable': 'False', 'default': 'None', 'autoincrement': 'auto', 'primary_key': 0, 'pythonType': 'str', 'title': 'dealer_name', 'amis_form_item': '', 'amis_table_column': ''}, {'name': 'dealer_address', 'type': 'VARCHAR(100)', 'nullable': 'True', 'default': 'None', 'autoincrement': 'auto', 'primary_key': 0, 'pythonType': 'str', 'title': 'dealer_address', 'amis_form_item': '', 'amis_table_column': ''}, {'name': 'dealer_id', 'type': 'INTEGER', 'nullable': 'True', 'default': 'None', 'autoincrement': 'auto', 'primary_key': 1, 'pythonType': 'int', 'title': 'dealer_id', 'amis_form_item': '', 'amis_table_column': ''}]
    oldcolumns = [{'name': 'dealer_name', 'type': 'VARCHAR(50)', 'nullable': 'False', 'default': 'None', 'autoincrement': 'auto', 'primary_key': 0, 'pythonType': 'str', 'title': 'dddd', 'amis_form_item': '', 'amis_table_column': ''}, {'name': 'dealer_address', 'type': 'VARCHAR(100)', 'nullable': 'True', 'default': 'None', 'autoincrement': 'auto', 'primary_key': 0, 'pythonType': 'str', 'title': 'dealer_address', 'amis_form_item': '', 'amis_table_column': ''}, {'name': 'dealer_id', 'type': 'INTEGER', 'nullable': 'True', 'default': 'None', 'autoincrement': 'auto', 'primary_key': 1, 'pythonType': 'int', 'title': 'dealer_id', 'amis_form_item': '', 'amis_table_column': ''}]
    rtn = get_updated_colums(upcolumns,oldcolumns)
    log.debug(rtn)
    '''
    str1 = "{'name': 'productDescription', 'type': TEXT(), 'default': None, 'comment': None, 'nullable': False}"
    print(to_json(str1))
    
    print(uappendlist(['id', 'name', 'phone']))

    print(uappend('id'))
    print(gen_dburi().__class__)
    
    test = '{"id":3,"name":"sdf"}'
    testl = '{"id":3,"name":"sdf","phone":"234243"},' \
            '{"id":3,"name":"sdf","phone":"234243"},' \
            '{"id":3,"name":"sdf","phone":"234243"}'
    teddd = '{\'name\': \'yourname\',\'phone\':\'241124\'}'
    print(to_fvcol(teddd))
    print(to_fvcol(testl))
    pstr = [{'name': 'zhjjj'}, {'id': 12}, {'phone': '12345'}]
    fstr = 'name=:name and id = :id or phone =  :phone '
    print(str(gen_dburi()))
    print(gen_dburi().__class__)
    print(is_dict("{'aa','ddd'}"))
    print(is_dict("{aa,ddd}"))
    print(to_dict("{'aa','ddd'}"))
    print(type(to_dict("{'aa','ddd'}")))
    print(isinstance("{'id':3,'name':'sdf'}", dict))
    print(is_json(test))
    print(to_json(test).__class__)
    s_comma = 'one,two,three,four,five'
    print(is_list(s_comma ))
    print(type(to_list(s_comma)))
    '''
