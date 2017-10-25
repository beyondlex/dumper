#!/usr/bin/python
# -*- coding: UTF-8 -*-
from conn import connection
import pymysql
pymysql.install_as_MySQLdb()



class Tool:

    def __init__(self):
        pass

    @staticmethod
    def conn():
        return connection

        # host = 'mysql'
        # user = 'root'
        # pwd = 'root'
        # database = 'curato_base'
        # return pymysql.connect(host, user, pwd, database)

    @staticmethod
    def tblExist(dbName, tblName):
        db = Tool.conn()
        cursor = db.cursor()
        cursor.execute('use curato_base')
        sql = "call table_exist('"+dbName+"', '"+tblName+"', @e)"
        cursor.execute(sql)
        cursor.execute("select @e")
        data = cursor.fetchone()
        return data[0]

    @staticmethod
    def colExist(dbName, tblName, colName):
        db = Tool.conn()
        cursor = db.cursor()
        cursor.execute('use curato_base')
        sql = "call column_exist('"+dbName+"', '"+tblName+"', '"+colName+"', @e)"
        cursor.execute(sql)
        cursor.execute("select @e")
        data = cursor.fetchone()
        return data[0]

    @staticmethod
    def dbExist(dbName):
        db = Tool.conn()
        cursor = db.cursor()
        cursor.execute('use curato_base')
        sql = "call db_exist('" + dbName + "', @e)"
        cursor.execute(sql)
        cursor.execute("select @e")
        data = cursor.fetchone()
        return data[0]

# e = Tool.tblExist('curato1', '1_apply_config')
# e = Tool.colExist('curato1', '1_apply_config', 'id')
# e = Tool.dbExist('curato1')
# print e