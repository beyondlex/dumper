
import os
# import pymysql
import time
from config import config
# pymysql.install_as_MySQLdb()

backup = os.system('')

def mydumper_data(db_name):
    t1 = time.time()

    host = config['RDS_HOST']
    user = config['RDS_USER']
    pwd = config['RDS_PWD']

    log_file = '/home/phper/deploy-test/dump-rds.log'
    dump_dir = '/home/phper/deploy-test/dumps/'

    dumper = '/home/phper/mydumper-0.9.1/mydumper'

    fo = open(log_file, "w")

    for i in range(1, 2):
        db_name = 'curato' + str(i)

        cmd = dumper +" -h " + host + " -u " + user + " -p '" + pwd + "' -B " + db_name + " -o " + dump_dir + db_name + "/"
        # backup = os.system(cmd)
        t2 = time.time()
        t = round(t2 - t1)
        print cmd
        print "%s Cost Time %s" % (db_name, t)

        fo.write("%s : %d seconds\n" % (db_name, t))


if __name__ == '__main__':
    db_name = raw_input('Input database name:')
    mydumper_data(db_name)



