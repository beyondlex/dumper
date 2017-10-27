
use curato_base;

DROP TABLE IF EXISTS `t_staff_auth`;
CREATE TABLE `t_staff_auth`  (
  `id` int(4) UNSIGNED NOT NULL AUTO_INCREMENT,
  `pid` int(4) NULL DEFAULT 0,
  `level` tinyint(1) NULL DEFAULT 0,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `code` varchar(99) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` tinyint(1) NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_staff_auth
-- ----------------------------
INSERT INTO `t_staff_auth` VALUES (1, 0, 0, '公告', 'notice', 1);
INSERT INTO `t_staff_auth` VALUES (2, 1, 1, '创建公告', 'notice_create', 1);
INSERT INTO `t_staff_auth` VALUES (3, 1, 1, '管理公告', 'notice_manage', 1);
INSERT INTO `t_staff_auth` VALUES (4, 0, 0, '考勤', 'attendance', 1);
INSERT INTO `t_staff_auth` VALUES (5, 0, 0, '排班', 'schedule', 1);
INSERT INTO `t_staff_auth` VALUES (6, 5, 1, '查看排班', 'schedule_manage', 1);
INSERT INTO `t_staff_auth` VALUES (7, 5, 1, '管理考勤规则', 'schedule_rule_manage', 1);
INSERT INTO `t_staff_auth` VALUES (8, 0, 0, '申请审批', 'apply', 1);
INSERT INTO `t_staff_auth` VALUES (9, 8, 1, '发起申请', 'apply_create', 1);
INSERT INTO `t_staff_auth` VALUES (10, 8, 1, '审批申请', 'apply_approve', 1);
INSERT INTO `t_staff_auth` VALUES (11, 8, 1, '流程设计', 'apply_approve_config', 1);
INSERT INTO `t_staff_auth` VALUES (12, 0, 0, '邮箱', 'message', 1);
INSERT INTO `t_staff_auth` VALUES (13, 12, 1, '写邮件', 'message_write', 1);
INSERT INTO `t_staff_auth` VALUES (14, 0, 0, '汇报', 'report', 1);
INSERT INTO `t_staff_auth` VALUES (15, 14, 1, '查看汇报', 'report_view', 1);
INSERT INTO `t_staff_auth` VALUES (16, 14, 1, '写汇报', 'report_write', 1);
INSERT INTO `t_staff_auth` VALUES (17, 14, 1, '回复汇报', 'report_reply', 1);
INSERT INTO `t_staff_auth` VALUES (18, 0, 0, '签到', 'signin', 1);
INSERT INTO `t_staff_auth` VALUES (19, 18, 1, '使用签到', 'signin_base', 1);
INSERT INTO `t_staff_auth` VALUES (20, 18, 1, '查看统计', 'signin_statistics', 1);
INSERT INTO `t_staff_auth` VALUES (21, 0, 0, '部门与员工', 'staff', 1);
INSERT INTO `t_staff_auth` VALUES (22, 21, 1, '设置人脸数据', 'staff_face_set', 1);
INSERT INTO `t_staff_auth` VALUES (23, 21, 1, '修改员工', 'staff_manage', 1);
INSERT INTO `t_staff_auth` VALUES (24, 21, 1, '管理部门', 'staff_dept_manage', 1);
INSERT INTO `t_staff_auth` VALUES (25, 4, 1, '查看个人考勤', 'attendance_mine', 1);
INSERT INTO `t_staff_auth` VALUES (26, 21, 1, '浏览部门员工', 'staff_scope_dept', 1);
INSERT INTO `t_staff_auth` VALUES (27, 21, 1, '浏览全部员工', 'staff_scope_company', 1);
INSERT INTO `t_staff_auth` VALUES (28, 4, 1, '查看他人考勤', 'attendance_stat', 1);

