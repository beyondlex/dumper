#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
# import pymysql
import time
from config import config

# pymysql.install_as_MySQLdb()

backup = os.system('')


def mydumper_data(db_name):
    t0 = time.time()

    host = config['MYSQL_HOST']
    user = config['MYSQL_USER']
    pwd = config['MYSQL_PWD']

    fo = open("/home/phper/deploy-test/load-rds.log", "ab+")

    dump_dir = '/home/phper/deploy-test/dumps/'
    loader = '/home/phper/mydumper-0.9.1/myloader'

    for i in range(1, 2):

        db_name = 'curato' + str(i)
        cmd = loader + " -h '" + host + "' -u '" + user + "' -p '" + pwd + "' -B " + db_name + " -d " + dump_dir + db_name + "/"
        print cmd
        t1 = time.time()
        backup = os.system(cmd)
        t2 = time.time()
        t = round(t2 - t1)
        print "%s Cost Time %s" % (db_name, t)

        fo.write("%s : %d seconds\n" % (db_name, t))

    fo.close()


if __name__ == '__main__':
    db_name = raw_input('Input database name:')
    mydumper_data(db_name)
