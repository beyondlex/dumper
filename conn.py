#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
from config import config
pymysql.install_as_MySQLdb()

class Conn:
    @staticmethod
    def conn():

        database = 'mysql'
        conn = pymysql.connect(config['MYSQL_HOST'], config['MYSQL_USER'], config['MYSQL_PWD'], database)
        print 'conn..'
        sql = '''
        DROP PROCEDURE  IF EXISTS table_exist;
        CREATE  PROCEDURE `table_exist`(IN `dbname` varchar(20),IN `tblname` varchar(50), OUT `exist` tinyint)
        BEGIN
            select count(*) from information_schema.`TABLES` where TABLE_SCHEMA=dbname and TABLE_NAME=tblname
            into exist;
        END;
        DROP PROCEDURE  IF EXISTS column_exist;
        CREATE PROCEDURE `column_exist`(IN `dbname` varchar(20),IN `tblname` varchar(50),IN `colname` varchar(20),OUT `exist` tinyint)
        BEGIN
            select count(*) from information_schema.`COLUMNS`
            where TABLE_SCHEMA = dbname
            and TABLE_NAME = tblname
            and COLUMN_NAME = colname
            into exist;
        END;
        DROP PROCEDURE  IF EXISTS db_exist;
        CREATE PROCEDURE `db_exist`(IN `dbname` varchar(20), OUT `exist` tinyint)
        BEGIN
            select count(*) from information_schema.SCHEMATA where SCHEMA_NAME=dbname
            into exist;
        END;
        '''
        cursor = conn.cursor()
        # cursor.execute(sql)
        return conn


connection = Conn.conn()
