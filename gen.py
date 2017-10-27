#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
# rds2
import time
from Tool import Tool
from conn import connection
from conn import config
import pymysql

pymysql.install_as_MySQLdb()


def getExtraSql(start, end):
    dbIndex = None
    if start == end:
        dbIndex = start

    dbs = getDbs(dbIndex)

    sqls = ''

    for d in dbs:
        companyId = str(d[1])
        index = str(d[3])
        dbName = "curato" + index
        if not Tool.dbExist(dbName):
            continue
        tblName = dbName + '.' + companyId + '_report_read_info'

        sql = '''
        ALTER TABLE %s
        MODIFY COLUMN `id`  int(11) NOT NULL AUTO_INCREMENT FIRST ;
        '''
        sql = sql % tblName

        sqls += sql

    return sqls


def getClearSql(start, end):
    dbIndex = None
    if start == end:
        dbIndex = start

    dbs = getDbs(dbIndex)

    sqls = ''

    for d in dbs:
        companyId = str(d[1])
        index = str(d[3])
        dbName = "curato" + index
        if not Tool.dbExist(dbName):
            continue
        tblName = dbName + '.' + companyId + '_apply_config'

        sql = '''
        DELETE FROM %s;
        INSERT INTO %s (type,company,apply_name,process_type,status,create_time) VALUES
        (1,1, '请假申请',1, 1,NOW()),
        (2,1, '加班申请',1, 1,NOW()),
        (3,1, '外勤申请',1, 1,NOW()),
        (4,1, '补签申请',1, 1,NOW()),
        (5,1, '通用申请',1, 1,NOW());
        '''
        sql = sql % (tblName, tblName)

        sqls += sql

    return sqls


def getDbs(dbIndex=None):
    if dbIndex:
        sql = "select * from t_database where dbname='%s'" % dbIndex
    else:
        sql = "select * from t_database"
    db = connection
    cursor = db.cursor()
    cursor.execute("use curato_base")
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def getCreateSql(dbName, sn):
    sn = str(sn)
    creates = []

    tblName = sn + "_attendance_rule"
    sql = '''
    CREATE TABLE `%s` (
      `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
      `rule_name` varchar(255) NOT NULL COMMENT '规则名称',
      `schedule_id` varchar(255) NOT NULL COMMENT '关联的班次时间段id，可多个',
      `rule_type` tinyint(4) NOT NULL COMMENT '班制类型。1固定2多班3自由',
      `week_day` varchar(255) DEFAULT NULL COMMENT '工作日，周一到周日，数字表示',
      `s_record_time` smallint(6) NULL DEFAULT NULL COMMENT '上班前多久打卡有效',
      `e_record_time` smallint(6) NULL DEFAULT NULL COMMENT '下班后多久内打卡有效',
      `late_least_time` smallint(6) NULL DEFAULT NULL COMMENT '迟到起算时间（超过才算迟到）',
      `late_max_time` smallint(6) NULL DEFAULT NULL COMMENT '迟到上限时间（超过算旷工）',
      `leave_least_time` smallint(6) NULL DEFAULT NULL COMMENT '早退起算时间（超过才算早退）',
      `leave_max_time` smallint(6) NULL DEFAULT NULL COMMENT '早退上限时间（超过即旷工）',
      `ot_least_time` smallint(6) NULL DEFAULT NULL COMMENT '加班起算时间（超过才可申请加班）',
      `record_way` varchar(255) DEFAULT NULL COMMENT '允许打卡的方式，人脸、二维码、外勤签到',
      `department_id` varchar(255) DEFAULT NULL COMMENT '适用的部门id',
      `user_id` varchar(255) DEFAULT NULL COMMENT '适用的用户id',
      `rule_work_time` smallint(6) NULL DEFAULT NULL COMMENT '自由班制的工作时间',
      `record_limit_time`  time NULL DEFAULT NULL COMMENT '自由班制的最晚打卡时间' ,
      `attendance_apply` varchar(255) DEFAULT NULL COMMENT '关联可影响考勤的申请，可多个',
      `status` tinyint(1) DEFAULT '1' COMMENT '状态',
      `create_time` datetime DEFAULT NULL COMMENT '创建时间',
      `create_from` tinyint(1) DEFAULT NULL COMMENT '创建操作来源，1web2移动',
      `create_by` int(11) DEFAULT NULL COMMENT '创建者id',
      `update_time` datetime DEFAULT NULL COMMENT '修改时间',
      `update_from` tinyint(1) DEFAULT NULL COMMENT '修改操作来源，1web2移动',
      `update_by` int(11) DEFAULT NULL COMMENT '修改者id',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='考勤规则表';
    '''

    sql = sql % (tblName)
    creates.append(sql)

    tblName = sn + "_attendance_user_rule"
    sql = '''
    CREATE TABLE `%s` (
    `id`  int NOT NULL AUTO_INCREMENT,
    `user_id`  int NULL COMMENT '已有规则的员工id' ,
    `rule_id`  int NULL COMMENT '考勤规则id' ,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='规则用户配置表';
    '''
    sql = sql % (tblName)
    creates.append(sql)

    tblName = sn + "_report_read_info"
    sql = '''
    CREATE TABLE `%s` (
    `id`  int(11) NOT NULL ,
    `report_id`  int(11) NOT NULL COMMENT '日报ID' ,
    `accepter`  int(11) NOT NULL COMMENT '接受者ID' ,
    `status`  tinyint(2) NULL DEFAULT 0 COMMENT '状态，0未读1已读' ,
    `create_time`  datetime NULL ,
    PRIMARY KEY (`id`)
    );
    '''
    sql = sql % (tblName)
    creates.append(sql)

    tblName = sn + "_notice_info"
    sql = '''
     CREATE TABLE `%s` (
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
    `message_id` int(11) NOT NULL COMMENT '公告id',
    `accepter` int(11) NOT NULL COMMENT '收公告人id',
    `status` tinyint(4) NOT NULL COMMENT '状态（0-删除、1-未读，2-已读）',
    `deleted` tinyint(4) DEFAULT '0' COMMENT '是否删除：0、正常；1、删除；',
    `send_message` tinyint(4) NOT NULL COMMENT '是否为发送者',
    `update_time` datetime DEFAULT NULL COMMENT '修改时间',
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
    '''
    sql = sql % (tblName)
    creates.append(sql)

    s = "use %s ;" % dbName

    for csql in creates:
        s += csql

    return s


def getModifySql(dbName, sn):
    sn = str(sn)
    # attendance
    tblName = sn + "_attendance"
    sql = ""
    alter = " alter table `" + tblName + "` "
    addCols = [
        ('rule_id', "ADD COLUMN `rule_id`  int NULL COMMENT '考勤规则id' AFTER `user_id`"),
        ('apply_id', "ADD COLUMN `apply_id`  varchar(200) DEFAULT NULL COMMENT '对考勤有影响的申请id集合' AFTER `cross_day`"),
        ('rule_work_time', "ADD COLUMN `rule_work_time`  smallint(6) NULL COMMENT '自由班工作时间' AFTER `apply_id`"),
        ('record_limit_time', "ADD COLUMN `record_limit_time`  time NULL COMMENT '自由班最晚打卡时间' AFTER `rule_work_time`"),
        (
            's_record_time',
            "ADD COLUMN `s_record_time`  smallint(6) NULL COMMENT '上班前有效打卡时间' AFTER `record_limit_time`"),
        ('late_least_time', "ADD COLUMN `late_least_time`  smallint(6) NULL COMMENT '迟到起算时间' AFTER `s_record_time`"),
        ('late_max_time',
         "ADD COLUMN `late_max_time`  smallint(6) NULL COMMENT '迟到上限时间（超过即旷工）' AFTER `late_least_time`"),
        ('leave_least_time', "ADD COLUMN `leave_least_time`  smallint(6) NULL COMMENT '早退起算时间' AFTER `late_max_time`"),
        ('leave_max_time',
         "ADD COLUMN `leave_max_time`  smallint(6) NULL COMMENT '早退上限时间（超过即旷工）' AFTER `leave_least_time`"),
        ('ot_least_time', "ADD COLUMN `ot_least_time`  smallint(6) NULL COMMENT '加班起算时间' AFTER `leave_max_time`"),
        ('attendance_apply',
         "ADD COLUMN `attendance_apply`  varchar(255) DEFAULT '1,2,3,4' COMMENT '关联申请' AFTER `ot_least_time`"),
        ('record_way',
         "ADD COLUMN `record_way`  varchar(255) DEFAULT '1,2,3' COMMENT '允许打卡方式' AFTER `attendance_apply`"),
        ('rule_type', "ADD COLUMN `rule_type`  tinyint(4) DEFAULT 1 COMMENT '班制类型。1固定2多班3自由' AFTER `record_way`"),
    ]
    for tup in addCols:
        if not Tool.colExist(dbName, tblName, tup[0]):
            sql += alter + tup[1] + "; "

    modify = '''
        %s MODIFY COLUMN `schedule_id`  int(11) NULL COMMENT '班次id' AFTER `rule_id`;
        %s MODIFY COLUMN `type`  int(11) NULL DEFAULT 0 COMMENT '考勤类型（加班、出差）' AFTER `attendance_status`;
        %s MODIFY COLUMN `work_time`  smallint(6) NULL COMMENT '应上班的分钟数' AFTER `update_time`;
        %s MODIFY COLUMN `cross_day`  tinyint(1) NULL DEFAULT 0 COMMENT '是否跨天' AFTER `overtime_type`;
    '''

    sql += (modify % ((alter,)*4))

    # schedule
    tblName = sn + "_schedule"
    alter = " alter table `" + tblName + "` "
    addCols = [
        ('rest', "ADD COLUMN `rest`  tinyint(1) NULL DEFAULT 1 COMMENT '是否有休息时间，1是0否' AFTER `cross_day`"),
    ]
    for tup in addCols:
        if not Tool.colExist(dbName, tblName, tup[0]):
            sql += alter + tup[1] + '; '

    modify = '''
        %s MODIFY COLUMN `department_id`  int(11) NULL COMMENT '部门id' AFTER `id`;
        %s MODIFY COLUMN `schedule_name`  varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '班次名称' AFTER `department_id`;
        %s MODIFY COLUMN `s_rest_time`  time NULL COMMENT '午休开始时间' AFTER `e_time`;
        %s MODIFY COLUMN `e_rest_time`  time NULL COMMENT '午休结束时间' AFTER `s_rest_time`;
        %s MODIFY COLUMN `creator`  int(11) NULL COMMENT '创建者id' AFTER `e_rest_time`;
        %s MODIFY COLUMN `create_time`  datetime NULL COMMENT '创建时间' AFTER `creator`;
        %s MODIFY COLUMN `work_time`  smallint(6) NULL DEFAULT 0 COMMENT '上班时间（分钟数）' AFTER `deleted`;
        %s MODIFY COLUMN `cross_day`  tinyint(1) NULL DEFAULT 0 COMMENT '是否跨天' AFTER `work_time`;
    '''

    sql += (modify % ((alter,) * 8))

    # attendance_record
    tblName = sn + "_attendance_record"
    if (not Tool.colExist(dbName, tblName, 'record_type')):
        s = " ALTER TABLE `%s` ADD COLUMN `record_type` tinyint(1) NULL DEFAULT 1 COMMENT '打卡方式。1人脸2二维码3外勤签到4补签' AFTER `time`;"
        sql += (s % tblName)

    # report
    tblName = sn + "_report"
    alter = " alter table " + tblName + " "
    addCols = [
        ('report_type', "ADD COLUMN `report_type`  tinyint(4) NULL COMMENT '汇报类型。1日报2周报' AFTER `type`"),
        ('work_plan', "ADD COLUMN `work_plan`  varchar(5000) NULL COMMENT '下周工作计划' AFTER `content`"),
        ('files', "ADD COLUMN `files`  varchar(255) NULL COMMENT '图片' AFTER `work_plan`"),
        ('report_end_date', "ADD COLUMN `report_end_date`  date NULL COMMENT '汇报结束日期' AFTER `report_date`"),
    ]
    for tup in addCols:
        if not Tool.colExist(dbName, tblName, tup[0]):
            sql += alter + tup[1] + "; "

    # user
    tblName = sn + "_user"
    alter = " alter table " + tblName + " "
    addCols = [
        ('report_to', "ADD COLUMN `report_to`  int(11) NULL COMMENT '汇报对象' AFTER `range` ;"),
    ]
    for tup in addCols:
        if not Tool.colExist(dbName, tblName, tup[0]):
            sql += alter + tup[1] + '; '

    # apply_config
    tblName = sn + "_apply_config"
    alter = " alter table `" + tblName + "` "
    addCols = [
        ('intel_approver', "ADD COLUMN `intel_approver`  varchar(255) NULL COMMENT '智能申请审批职位id' AFTER `approver`"),
        ('company', "ADD COLUMN `company`  tinyint(1) NULL DEFAULT 0 COMMENT '是否全公司适用' AFTER `department_id`"),
        ('hand_sign', "ADD COLUMN `hand_sign`  tinyint(1) NULL DEFAULT 1 COMMENT '是否启用手签' AFTER `approver`"),
        ('process_type',
         "ADD COLUMN `process_type`  tinyint(1) NULL DEFAULT 1 COMMENT '审批流程类别。1员工2智能（职位）' AFTER `hand_sign`"),
    ]
    for tup in addCols:
        if not Tool.colExist(dbName, tblName, tup[0]):
            sql += alter + tup[1] + '; '

    dropCols = [
        ('apply_enname', "drop column `apply_enname`"),
        ('url', "drop column `url`"),
    ]

    for tup in dropCols:
        if Tool.colExist(dbName, tblName, tup[0]):
            sql += alter + tup[1] + ';'

    modify = '''
        %s MODIFY COLUMN `department_id`  varchar(100) NULL DEFAULT NULL COMMENT '可使用此申请的部门id' AFTER `type`;
        %s MODIFY COLUMN `approver`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '申请审批人id' AFTER `apply_name`;
    '''

    sql += modify % ((alter,)*2)

    # apply
    tblName = sn + "_apply"
    alter = " alter table `" + tblName + "` "
    addCols = [
        ('carbon_copy', "ADD COLUMN `carbon_copy`  varchar(1000) NULL COMMENT '抄送人员id' AFTER `approver`"),
        ('files', "ADD COLUMN `files`  varchar(255) NULL COMMENT '附带文件（图片）' AFTER `content`"),
        ('day_count', "ADD COLUMN `day_count`  int NULL DEFAULT NULL COMMENT '天数' AFTER `files`"),
        ('hour_count', "ADD COLUMN `hour_count`  int NULL DEFAULT NULL COMMENT '小时数' AFTER `day_count`"),
        ('process_type',
         "ADD COLUMN `process_type`  tinyint(1) NULL DEFAULT 1 COMMENT '审批流程列表。1员工审批2智能审批（职位）' AFTER `approver`"),
        ('hand_sign', "ADD COLUMN `hand_sign`  tinyint(1) NULL COMMENT '是否开启手签1是0否' AFTER `gps_location`,"),
        (
            'overtime_type',
            "ADD COLUMN `overtime_type`  tinyint(1) NULL DEFAULT 0 COMMENT '加班类型，是否法定假日' AFTER `e_time`"),
    ]

    for tup in addCols:
        if not Tool.colExist(dbName, tblName, tup[0]):
            sql += alter + tup[1] + '; '

    modify = '''
        %s MODIFY COLUMN `content`  text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '内容' AFTER `title`;
    '''

    sql += modify % alter

    # apply_info
    tblName = sn + "_apply_info"
    alter = " alter table `" + tblName + "` "
    addCols = [
        ('role_id', "ADD COLUMN `role_id`  int NULL COMMENT '职位id。智能审批流程时用' AFTER `accepter`"),
        ('remind_time', "ADD COLUMN `remind_time`  datetime NULL COMMENT '上一次催办时间' AFTER `read`"),
    ]
    for tup in addCols:
        if not Tool.colExist(dbName, tblName, tup[0]):
            sql += alter + tup[1] + '; '

    modify = '''
        %s MODIFY COLUMN `accepter`  int(11) NULL COMMENT '申请接收人id（审批人及自己）' AFTER `apply_id`;
    '''

    sql += modify % alter

    # notice
    tblName = sn + "_notice"
    alter = " alter table `" + tblName + "` "
    addCols = [
        ('send_all', "ADD COLUMN `send_all`  tinyint(4) NULL COMMENT '是否全公司发送：0，否；1，是；' AFTER `status`"),
        ('department_id', "ADD COLUMN `department_id`  varchar(1000) NULL COMMENT '公司接收部门ID集合，以|区分' AFTER `send_all`"),
        ('user_id', "ADD COLUMN `user_id`  varchar(1000) NULL COMMENT '公司接收用户ID集合，以|区分' AFTER `department_id`"),
        ('attachments', "ADD COLUMN `attachments`  varchar(255) NULL COMMENT '公告的附件或图片集合，以；；区分' AFTER `user_id`"),
    ]
    for tup in addCols:
        if not Tool.colExist(dbName, tblName, tup[0]):
            sql += alter + tup[1] + '; '

    modify = '''
        %s MODIFY COLUMN `content`  varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '公告内容' AFTER `title`;
        %s MODIFY COLUMN `e_date`  date NULL COMMENT '失效时间' AFTER `s_date`;
    '''

    sql += modify % ((alter,)*2)

    # display
    tblName = sn + "_display"
    s = " ALTER TABLE `%s` MODIFY COLUMN `sort` integer(5) NOT NULL COMMENT '排序' AFTER `add_time`;"
    sql += (s % tblName)

    return sql


def getAuthSql(start, end):
    dbIndex = None
    if start == end:
        dbIndex = start

    data = getDbs(dbIndex)

    db = connection
    cursor = db.cursor()

    sqlss = ''

    # per row for company
    for d in data:

        companyId = str(d[1])
        dbIndex = str(d[3])

        dbName = "curato" + dbIndex
        if not Tool.dbExist(dbName):
            continue

        sqls = "use %s;" % dbName

        tblName = companyId + "_staff_role_auth"

        createTbl = '''
        drop table if EXISTS `%s`;
        CREATE TABLE `%s` (
        `id`  int(5) UNSIGNED  NOT NULL AUTO_INCREMENT ,
        `role_id`  int(5) NULL ,
        `auth`  text NULL ,
        PRIMARY KEY (`id`)
        )
        ;
        '''
        createTbl = createTbl % (tblName, tblName)

        sqls += createTbl

        oldTbl = companyId + "_user_role_auth"

        if Tool.tblExist(dbName, oldTbl):

            authSql = "select * from %s " % oldTbl
            cursor.execute("use %s" % dbName)
            cursor.execute(authSql)
            res = cursor.fetchall()

            insertSql = "insert into %s (role_id, auth) values " % tblName
            insertCount = 0

            for a in res:
                authStr = a[4]
                roleId = a[1]
                authStr = authStr.strip(',')
                auth = convertAuth(authStr)
                if len(auth) > 0:
                    auth = ','.join(str(n) for n in auth)
                else:
                    auth = ''

                insertCount += 1

                insertSql += " ('%s', '%s')," % (roleId, auth)

            if insertCount:
                insertSql = insertSql.rstrip(',')
                insertSql += ';'
            else:
                insertSql = ''

            sqls += insertSql

        sqlss += sqls

    return sqlss


def convertAuth(authStr):
    authOld = authStr.split(',')
    map = [
        [[9, 12, 13, 14], [9]],
        [[10, 16, 17, 18], [10]],
        [[19], [25]],
        [[24], [13]],
        [[29], [2, 3]],
        [[32], [15]],
        [[31, 33], [16]],
        [[34], [17]],
        [[35], [6]],
        [[36], [7]],
        [[51], [22]],
        [[63], [23]],
        [[53, 54], [24]],
        [[62], [19]],
        [[61], [20]],
    ]
    authNew = cx(map, authOld)
    return authNew


def cx(map, old):
    new = []
    for item in map:
        source = item[0]
        target = item[1]
        if isIn(source, old):
            new = new + target

    return list(set(new))


def isIn(list1, list2):
    i = False
    for item in list1:
        if str(item) in list2:
            i = True
            break
    return i


def op_update_dump(start=None, end=None):
    print 'Generating update ..'
    update_dump_start = time.time()
    db = connection
    cursor = db.cursor()
    # cursor.execute("select * from t_database where dbname < 3 ")
    cursor.execute("use curato_base")

    dbIndex = None
    if start == end:
        dbIndex = start

    if dbIndex:
        s = "select * from t_database where dbname = '" + dbIndex + "' "
    elif (start and end):
        s = "select * from t_database where dbname >= %s and dbname <= %s " % (start, end)
    else:
        all = raw_input('Dump all ? (y/N) ')
        if all != 'y':
            os._exit(1)
        s = "select * from t_database"

    cursor.execute(s)
    data = cursor.fetchall()

    # log_file = dir + 'update.log'
    # h = open(log_file, 'w')

    sqls = ""

    for d in data:
        t1 = time.time()
        sn = str(d[1])  # companyId
        dbName = "curato" + d[3]  # db index
        if not Tool.dbExist(dbName):
            continue
        s = ""
        create_sql = getCreateSql(dbName, sn)
        print 'create_sql..' + dbName + '-' + sn
        modify_sql = getModifySql(dbName, sn)
        print 'modify_sql..' + dbName + '-' + sn
        s += create_sql
        s += modify_sql

        sqls += s

        t2 = time.time()

        t = t2 - t1
        print "Generating %s Cost Time %s" % (dbName + '-' + sn, t)

        # h.write("Generating %s Cost Time %s" % (dbName + '-' + sn, t))

    f = update_file
    fo = open(f, "w")
    fo.write(sqls)
    fo.close()

    update_dump_end = time.time()
    print "Generating Cost Time %s" % (update_dump_end - update_dump_start)

    print 'Generating update done. file: %s' % update_file
    return 1


def readInput(ipt):
    if ',' in ipt:
        rets = []
        elems = ipt.split(',')
        for e in elems:
            rets.append(e.strip())
        return rets
    return ipt.strip()


def op_dump(s, e):
    print 'Dumping dbs ..'
    fo = open(dump_log, "w")
    t1 = time.time()
    if s == e:
        db_name = 'curato' + s
        cmd = dumper + " -h " + host_from + " -u " + user_from + " -p '" + pwd_from + "' -B " + db_name + " -o " + dump_dir + db_name + "/"
        if not just_print:
            print 'dump start:'
            backup = os.system(cmd)
    else:
        for i in range(int(s), int(e)):
            db_name = 'curato' + str(i)
            cmd = dumper + " -h " + host_from + " -u " + user_from + " -p '" + pwd_from + "' -B " + db_name + " -o " + dump_dir + db_name + "/"
            if not just_print:
                print 'dump start:'
                backup = os.system(cmd)
            t2 = time.time()
            t = round(t2 - t1)
            print cmd
            print "%s Cost Time %s" % (db_name, t)

            fo.write("%s : %d seconds\n" % (db_name, t))

    print "Dump Cost Time %s" % (time.time() - t1)
    return 1


def op_load(s, e):
    print 'Loading dbs from local dirs ..'
    fo = open(load_log, "w")
    t1 = time.time()
    if s == e:
        db_name = 'curato' + s
        cmd = loader + " -h '" + host + "' -u '" + user + "' -p '" + pwd + "' -B " + db_name + " -d " + dump_dir + db_name + "/"
        if not just_print:
            backup = os.system(cmd)
    else:
        for i in range(int(s), int(e)):
            db_name = 'curato' + str(i)
            cmd = loader + " -h '" + host + "' -u '" + user + "' -p '" + pwd + "' -B " + db_name + " -d " + dump_dir + db_name + "/"
            if not just_print:
                backup = os.system(cmd)
            t2 = time.time()
            t = round(t2 - t1)
            print cmd
            print "%s Cost Time %s" % (db_name, t)
            fo.write("%s : %d seconds\n" % (db_name, t))

    print "Load Cost Time %s" % (time.time() - t1)
    return 1


def op_update_load():
    print 'Loading update ..'
    cmd = "mysql -h'" + host + "' -u'" + user + "' -p'" + pwd + "' -f mysql < " + update_file
    t1 = time.time()
    if not just_print:
        os.popen(cmd)
    t2 = time.time()
    t = t2 - t1
    print "source from dump cost %s " % t
    return 1


def op_auth_dump(s, e):
    print 'Generating auth ..'
    f = open(auth_file, 'w')
    t1 = time.time()
    if not just_print:
        f.write(getAuthSql(s, e))
    f.close()
    t2 = time.time()
    print "Generating authSql Cost Time %s" % (t2 - t1)
    return 1


def load_to_db_from(f, name='file'):
    print 'Loading %s ..' % name
    cmd = "mysql -h'" + host + "' -u'" + user + "' -p'" + pwd + "' -f mysql < " + f
    t1 = time.time()
    if not just_print:
        os.popen(cmd)
    t2 = time.time()
    t = t2 - t1
    print "Loaded from %s cost %s " % (name, t)


def op_auth_load():
    load_to_db_from(auth_file, 'auth')


def op_clear_dump(s, e):
    print 'Generating clear ..'
    f = open(clear_file, 'w')
    t1 = time.time()
    if not just_print:
        f.write(getClearSql(s, e))
    f.close()
    t2 = time.time()
    print "Generating clearSql Cost Time %s" % (t2 - t1)


def op_clear_load():
    load_to_db_from(clear_file, 'clear')


def op_schema_load():
    load_to_db_from(schema_file, 'schema')


def op_base_auth_load():
    load_to_db_from(auth_base_file, 'base auth data')


def op_extra(s, e):
    print 'Generating extra ..'
    f = open(extra_file, 'w')
    t1 = time.time()
    if not just_print:
        f.write(getExtraSql(s, e))
    f.close()
    t2 = time.time()
    print "Generating extraSql Cost Time %s" % (t2 - t1)

    load_to_db_from(extra_file, 'extra')


if __name__ == '__main__':

    host = config['MYSQL_HOST']
    user = config['MYSQL_USER']
    pwd = config['MYSQL_PWD']

    host_from = config['RDS_HOST']
    user_from = config['RDS_USER']
    pwd_from = config['RDS_PWD']

    update_file = config['UPDATE_FILE']
    auth_file = config['AUTH_FILE']
    clear_file = config['CLEAR_FILE']
    extra_file = config['EXTRA_FILE']

    schema_file = config['SCHEMA_FILE']
    auth_base_file = config['BASE_AUTH_FILE']

    dump_dir = config['DUMP_DIR']
    dump_log = config['DUMP_LOG']
    dumper = config['DUMPER']

    load_log = config['LOAD_LOG']
    loader = config['LOADER']

    just_print = int(config['JUST_PRINT'])

    examine_paths = [dump_dir, schema_file]
    check_result = True
    for path in examine_paths:
        if not os.path.exists(path):
            check_result = False
            print "file or dir not exist: %s" % path
    if not check_result:
        os._exit(1)

    entry = '''
    1)Manual
    2)Automatic
    '''
    print entry
    mode = raw_input('Select mode: ')
    if mode == '1':
        print 'Manual operation start ..'
        pass
    elif mode == '2':
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print 'Automatic process start ..'

        start = 1
        end = 2

        ta = time.time()

        # 1.dump
        op_dump(start, end)
        # 2.load
        op_load(start, end)
        # 3.update dump
        op_update_dump(start, end)
        # 4.update load
        op_update_load()
        # 5.auth dump
        op_auth_dump(start, end)
        # 6.auth load
        op_auth_load()
        # 7.clear dump
        op_clear_dump(start, end)
        # 8.clear load
        op_clear_load()
        # 9.extra
        op_extra(start, end)
        # 10.schema
        op_schema_load()
        # 11.base auth data
        op_base_auth_load()

        tb = time.time()

        print 'Automatic process end.'
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print "Total Time Cost %s seconds. " % (tb - ta)

        os._exit(1)
    else:
        print 'Unknown command.'

        os._exit(1)

    lv1 = '''
    1) init dbs  ...
    2) dump and load ...
    3) update ...
    4) auth ...
    5) clear ...
    6) extra ...
    7) schema ...
    '''
    print lv1
    ipt = raw_input("Pick one:")
    if ipt == '1':  # init dbs
        print 'Unsupported.'
    elif ipt == '2':  # dump and load
        lv2 = '''
        1) dump dbs to local ...
        2) load from local
        '''
        print lv2
        ipt = raw_input("Enter your choice:")

        if ipt == '1':  # dump
            start = raw_input("Db index from:")
            end = raw_input("Db index to:")
            op_dump(start, end)

        elif ipt == '2':  # load
            start = raw_input("Db index from:")
            end = raw_input("Db index to:")
            op_load(start, end)

        else:
            print 'Unknown command.'

    elif ipt == '3':  # update
        lv2 = '''
        1) update.sql generate ...
        2) update.sql load
        '''
        print lv2
        ipt = raw_input("Enter your choice:")
        if ipt == '1':  # update generate
            start = raw_input("Db index from:")
            end = raw_input("Db index to:")

            op_update_dump(start, end)

        elif ipt == '2':  # update load
            op_update_load()
        else:
            print 'Unknown command.'

    elif ipt == '4':  # auth
        lv2 = '''
        1) auth.sql generate ...
        2) auth.sql load
        '''
        print lv2
        ipt = raw_input("Enter your choice:")
        if ipt == '1':  # auth generate
            start = raw_input("Db index from:")
            end = raw_input("Db index to:")
            op_auth_dump(start, end)

        elif ipt == '2':  # auth load
            op_auth_load()
        else:
            print 'Unknown command.'
    elif ipt == '5':  # clear
        lv2 = '''
        1) clear.sql generate ...
        2) clear.sql load
        '''
        print lv2
        ipt = raw_input("Enter your choice:")
        if ipt == '1':  # clear generate
            start = raw_input("Db index from:")
            end = raw_input("Db index to:")
            op_clear_dump(start, end)

        elif ipt == '2':  # clear load
            op_clear_load()
        else:
            print 'Unknown command.'

    elif ipt == '6':  # extra
        start = raw_input("Db index from:")
        end = raw_input("Db index to:")

        op_extra(start, end)

    elif ipt == '7':  # schema
        exist = os.path.exists(schema_file)
        if not exist:
            print 'Schema file not exist'
            os._exit(1)
        op_schema_load()

    elif ipt == '8':  # base auth
        exist = os.path.exists(auth_base_file)
        if not exist:
            print 'Base auth file not exist'
            os._exit(1)
        op_base_auth_load()

    else:
        print 'Unknown command.'

