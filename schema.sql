use curato_base;
CREATE TABLE `schema_attendance_rule` (
	`id` INT (11) NOT NULL AUTO_INCREMENT COMMENT '主键',
	`rule_name` VARCHAR (255) NOT NULL COMMENT '规则名称',
	`schedule_id` VARCHAR (255) NOT NULL COMMENT '关联的班次时间段id，可多个',
	`rule_type` TINYINT (4) NOT NULL COMMENT '班制类型。1固定2多班3自由',
	`week_day` VARCHAR (255) DEFAULT NULL COMMENT '工作日，周一到周日，数字表示',
	`s_record_time` SMALLINT (6) NULL DEFAULT NULL COMMENT '上班前多久打卡有效',
	`e_record_time` SMALLINT (6) NULL DEFAULT NULL COMMENT '下班后多久内打卡有效',
	`late_least_time` SMALLINT (6) NULL DEFAULT NULL COMMENT '迟到起算时间（超过才算迟到）',
	`late_max_time` SMALLINT (6) NULL DEFAULT NULL COMMENT '迟到上限时间（超过算旷工）',
	`leave_least_time` SMALLINT (6) NULL DEFAULT NULL COMMENT '早退起算时间（超过才算早退）',
	`leave_max_time` SMALLINT (6) NULL DEFAULT NULL COMMENT '早退上限时间（超过即旷工）',
	`ot_least_time` SMALLINT (6) NULL DEFAULT NULL COMMENT '加班起算时间（超过才可申请加班）',
	`record_way` VARCHAR (255) DEFAULT NULL COMMENT '允许打卡的方式，人脸、二维码、外勤签到',
	`department_id` VARCHAR (255) DEFAULT NULL COMMENT '适用的部门id',
	`user_id` VARCHAR (255) DEFAULT NULL COMMENT '适用的用户id',
	`rule_work_time` SMALLINT (6) NULL DEFAULT NULL COMMENT '自由班制的工作时间',
	`record_limit_time` time NULL DEFAULT NULL COMMENT '自由班制的最晚打卡时间',
	`attendance_apply` VARCHAR (255) DEFAULT NULL COMMENT '关联可影响考勤的申请，可多个',
	`status` TINYINT (1) DEFAULT '1' COMMENT '状态',
	`create_time` datetime DEFAULT NULL COMMENT '创建时间',
	`create_from` TINYINT (1) DEFAULT NULL COMMENT '创建操作来源，1web2移动',
	`create_by` INT (11) DEFAULT NULL COMMENT '创建者id',
	`update_time` datetime DEFAULT NULL COMMENT '修改时间',
	`update_from` TINYINT (1) DEFAULT NULL COMMENT '修改操作来源，1web2移动',
	`update_by` INT (11) DEFAULT NULL COMMENT '修改者id',
	PRIMARY KEY (`id`)
) ENGINE = INNODB DEFAULT CHARSET = utf8 COMMENT = '考勤规则表';

CREATE TABLE `schema_attendance_user_rule` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`user_id` INT NULL COMMENT '已有规则的员工id',
	`rule_id` INT NULL COMMENT '考勤规则id',
	PRIMARY KEY (`id`)
) COMMENT = '规则用户配置表';

ALTER TABLE `schema_attendance`  ADD COLUMN `rule_id` INT NULL COMMENT '考勤规则id' AFTER `user_id`;
ALTER TABLE `schema_attendance`  ADD COLUMN `apply_id` VARCHAR (200) NULL COMMENT '对考勤有影响的申请id集合' AFTER `cross_day`;
ALTER TABLE `schema_attendance`  ADD COLUMN `rule_work_time` SMALLINT (6) NULL COMMENT '自由班工作时间' AFTER `apply_id`;
ALTER TABLE `schema_attendance`  ADD COLUMN `record_limit_time` time NULL COMMENT '自由班最晚打卡时间' AFTER `rule_work_time`;
ALTER TABLE `schema_attendance`  ADD COLUMN `s_record_time` SMALLINT (6) NULL COMMENT '上班前有效打卡时间' AFTER `record_limit_time`;
ALTER TABLE `schema_attendance`  ADD COLUMN `late_least_time` SMALLINT (6) NULL COMMENT '迟到起算时间' AFTER `s_record_time`;
ALTER TABLE `schema_attendance`  ADD COLUMN `late_max_time` SMALLINT (6) NULL COMMENT '迟到上限时间（超过即旷工）' AFTER `late_least_time`;
ALTER TABLE `schema_attendance`  ADD COLUMN `leave_least_time` SMALLINT (6) NULL COMMENT '早退起算时间' AFTER `late_max_time`;
ALTER TABLE `schema_attendance`  ADD COLUMN `leave_max_time` SMALLINT (6) NULL COMMENT '早退上限时间（超过即旷工）' AFTER `leave_least_time`;
ALTER TABLE `schema_attendance`  ADD COLUMN `ot_least_time` SMALLINT (6) NULL COMMENT '加班起算时间' AFTER `leave_max_time`;
ALTER TABLE `schema_attendance`  ADD COLUMN `attendance_apply` VARCHAR (255) NULL COMMENT '关联申请' AFTER `ot_least_time`;
ALTER TABLE `schema_attendance`  ADD COLUMN `record_way` VARCHAR (255) NULL COMMENT '允许打卡方式' AFTER `attendance_apply`;
ALTER TABLE `schema_attendance`  ADD COLUMN `rule_type` TINYINT (4) NULL COMMENT '班制类型。1固定2多班3自由' AFTER `record_way`;
ALTER TABLE `schema_attendance`  MODIFY COLUMN `schedule_id` INT (11) NULL COMMENT '班次id' AFTER `rule_id`;
ALTER TABLE `schema_attendance`  MODIFY COLUMN `type` INT (11) NULL DEFAULT 0 COMMENT '考勤类型（加班、出差）' AFTER `attendance_status`;
ALTER TABLE `schema_attendance`  MODIFY COLUMN `work_time` SMALLINT (6) NULL COMMENT '应上班的分钟数' AFTER `update_time`;
ALTER TABLE `schema_attendance`  MODIFY COLUMN `cross_day` TINYINT (1) NULL DEFAULT 0 COMMENT '是否跨天' AFTER `overtime_type`;

ALTER TABLE `schema_schedule`  ADD COLUMN `rest` TINYINT (1) NULL DEFAULT 1 COMMENT '是否有休息时间，1是0否' AFTER `cross_day`;
ALTER TABLE `schema_schedule`  MODIFY COLUMN `department_id` INT (11) NULL COMMENT '部门id' AFTER `id`;
ALTER TABLE `schema_schedule`  MODIFY COLUMN `schedule_name` VARCHAR (50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '班次名称' AFTER `department_id`;
ALTER TABLE `schema_schedule`  MODIFY COLUMN `s_rest_time` time NULL COMMENT '午休开始时间' AFTER `e_time`;
ALTER TABLE `schema_schedule`  MODIFY COLUMN `e_rest_time` time NULL COMMENT '午休结束时间' AFTER `s_rest_time`;
ALTER TABLE `schema_schedule`  MODIFY COLUMN `creator` INT (11) NULL COMMENT '创建者id' AFTER `e_rest_time`;
ALTER TABLE `schema_schedule`  MODIFY COLUMN `create_time` datetime NULL COMMENT '创建时间' AFTER `creator`;
ALTER TABLE `schema_schedule`  MODIFY COLUMN `work_time` SMALLINT (6) NULL DEFAULT 0 COMMENT '上班时间（分钟数）' AFTER `deleted`;
ALTER TABLE `schema_schedule`  MODIFY COLUMN `cross_day` TINYINT (1) NULL DEFAULT 0 COMMENT '是否跨天' AFTER `work_time`;

ALTER TABLE `schema_attendance_record` ADD COLUMN `record_type` TINYINT (1) NULL DEFAULT 1 COMMENT '打卡方式。1人脸2二维码3外勤签到4补签' AFTER `time`;

ALTER TABLE `schema_apply_config` DROP COLUMN `apply_enname`;
ALTER TABLE `schema_apply_config` DROP COLUMN `url`;
ALTER TABLE `schema_apply_config` MODIFY COLUMN `department_id` VARCHAR (100) NULL DEFAULT NULL COMMENT '可使用此申请的部门id' AFTER `type`;
ALTER TABLE `schema_apply_config` MODIFY COLUMN `approver` VARCHAR (255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '申请审批人id' AFTER `apply_name`;
ALTER TABLE `schema_apply_config` ADD COLUMN `intel_approver` VARCHAR (255) NULL COMMENT '智能申请审批职位id' AFTER `approver`;
ALTER TABLE `schema_apply_config` ADD COLUMN `company` TINYINT (1) NULL DEFAULT 0 COMMENT '是否全公司适用' AFTER `department_id`;
ALTER TABLE `schema_apply_config` ADD COLUMN `hand_sign` TINYINT (1) NULL DEFAULT 1 COMMENT '是否启用手签' AFTER `approver`;
ALTER TABLE `schema_apply_config` ADD COLUMN `process_type` TINYINT (1) NULL DEFAULT 1 COMMENT '审批流程类别。1员工2智能（职位）' AFTER `hand_sign`;

ALTER TABLE `schema_apply` MODIFY COLUMN `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '内容' AFTER `title`;
ALTER TABLE `schema_apply` ADD COLUMN `carbon_copy` VARCHAR (1000) NULL COMMENT '抄送人员id' AFTER `approver`;
ALTER TABLE `schema_apply` ADD COLUMN `files` VARCHAR (255) NULL COMMENT '附带文件（图片）' AFTER `content`;
ALTER TABLE `schema_apply` ADD COLUMN `day_count` INT NULL DEFAULT NULL COMMENT '天数' AFTER `files`;
ALTER TABLE `schema_apply` ADD COLUMN `hour_count` INT NULL DEFAULT NULL COMMENT '小时数' AFTER `day_count`;
ALTER TABLE `schema_apply` ADD COLUMN `process_type` TINYINT (1) NULL DEFAULT 1 COMMENT '审批流程列表。1员工审批2智能审批（职位）' AFTER `approver`;
ALTER TABLE `schema_apply` ADD COLUMN `hand_sign` TINYINT (1) NULL COMMENT '是否开启手签1是0否' AFTER `gps_location`;
ALTER TABLE `schema_apply` ADD COLUMN `overtime_type` TINYINT (1) NULL DEFAULT 0 COMMENT '加班类型，是否法定假日' AFTER `e_time`;

ALTER TABLE `schema_apply_info` MODIFY COLUMN `accepter` INT (11) NULL COMMENT '申请接收人id（审批人及自己）' AFTER `apply_id`;
ALTER TABLE `schema_apply_info` ADD COLUMN `role_id` INT NULL COMMENT '职位id。智能审批流程时用' AFTER `accepter`;
ALTER TABLE `schema_apply_info` ADD COLUMN `remind_time` datetime NULL COMMENT '上一次催办时间' AFTER `read`;

ALTER TABLE `schema_report` ADD COLUMN `report_type` TINYINT (4) NULL COMMENT '汇报类型。1日报2周报' AFTER `type`;
ALTER TABLE `schema_report` ADD COLUMN `work_plan` VARCHAR (5000) NULL COMMENT '下周工作计划' AFTER `content`;
ALTER TABLE `schema_report` ADD COLUMN `report_end_date` date NULL COMMENT '汇报结束日期' AFTER `report_date`;
ALTER TABLE `schema_report` ADD COLUMN `files` VARCHAR (255) NULL COMMENT '图片' AFTER `work_plan`;

ALTER TABLE `schema_user` ADD COLUMN `report_to` INT (11) NULL DEFAULT 1 COMMENT '汇报对象' AFTER `range`;

CREATE TABLE `schema_report_read_info` (
	`id` INT (11) NOT NULL,
	`report_id` INT (11) NOT NULL COMMENT '日报ID',
	`accepter` INT (11) NOT NULL COMMENT '接受者ID',
	`status` TINYINT (2) NULL DEFAULT 0 COMMENT '状态，0未读1已读',
	`create_time` datetime NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `schema_notice` MODIFY COLUMN `content` VARCHAR (1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '公告内容' AFTER `title`;
ALTER TABLE `schema_notice` ADD COLUMN `send_all` TINYINT (4) NULL COMMENT '是否全公司发送：0，否；1，是；' AFTER `status`;
ALTER TABLE `schema_notice` ADD COLUMN `department_id` VARCHAR (1000) NULL COMMENT '公司接收部门ID集合，以|区分' AFTER `send_all`;
ALTER TABLE `schema_notice` ADD COLUMN `user_id` VARCHAR (1000) NULL COMMENT '公司接收用户ID集合，以|区分' AFTER `department_id`;
ALTER TABLE `schema_notice` ADD COLUMN `attachments` VARCHAR (255) NULL COMMENT '公告的附件或图片集合，以；；区分' AFTER `user_id`;

CREATE TABLE `schema_notice_info` (
	`id` INT (11) NOT NULL AUTO_INCREMENT COMMENT '主键',
	`message_id` INT (11) NOT NULL COMMENT '公告id',
	`accepter` INT (11) NOT NULL COMMENT '收公告人id',
	`status` TINYINT (4) NOT NULL COMMENT '状态（0-删除、1-未读，2-已读）',
	`deleted` TINYINT (4) DEFAULT '0' COMMENT '是否删除：0、正常；1、删除；',
	`send_message` TINYINT (4) NOT NULL COMMENT '是否为发送者',
	`update_time` datetime DEFAULT NULL COMMENT '修改时间',
	PRIMARY KEY (`id`)
) ENGINE = INNODB AUTO_INCREMENT = 16 DEFAULT CHARSET = utf8;

ALTER TABLE `schema_display` MODIFY COLUMN `sort` integer(5) NOT NULL COMMENT '排序' AFTER `add_time`;

CREATE TABLE `schema_staff_role_auth` (
`id` INT ( 5 ) UNSIGNED NOT NULL AUTO_INCREMENT,
`role_id` INT ( 5 ) NULL,
`auth` text NULL,
PRIMARY KEY ( `id` ) 
);

