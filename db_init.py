#!/usr/bin/python
import os
from config import config

host = config['MYSQL_HOST']
user = config['MYSQL_USER']
pwd = config['MYSQL_PWD']

for i in range(1, 80):
    name = 'curato' + str(i)
    cmd = "mysql -h'"+host+"' -u'"+user+"' -p'"+pwd+"' mysql -e 'create database if not exists "+name+"'"
    os.popen(cmd)
