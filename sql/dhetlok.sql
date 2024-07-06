/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Host           : localhost:3306
 Source Schema         : dhetlok

 Target Server Type    : MySQL
 Target Server Version : 80027
 File Encoding         : 65001

 Date: 07/07/2024 02:07:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for artist
-- ----------------------------
DROP TABLE IF EXISTS `artist`;
CREATE TABLE `artist`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `real_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `genre` int NULL DEFAULT NULL,
  `img_url` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `hot` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of artist
-- ----------------------------
INSERT INTO `artist` VALUES (1, '毛不易', 1, '1656402941.jpg', 1);
INSERT INTO `artist` VALUES (2, 'GALA', 1, '1656403048.jpg', 1);
INSERT INTO `artist` VALUES (3, '戴羽彤', 1, '1656403128.jpg', 1);
INSERT INTO `artist` VALUES (4, '房东的猫', 1, '1656403685.jpg', 1);
INSERT INTO `artist` VALUES (5, '张碧晨', 1, '1656403886.jpg', 1);
INSERT INTO `artist` VALUES (6, '周杰伦', 1, '1656403897.jpg', 1);
INSERT INTO `artist` VALUES (7, '黄霄云', 1, '1656403910.jpg', 1);
INSERT INTO `artist` VALUES (8, '薛之谦', 1, '1656403922.jpg', 1);
INSERT INTO `artist` VALUES (9, '朴树', 1, '1656403943.jpg', 1);
INSERT INTO `artist` VALUES (10, '张学友', 1, '1656403957.jpg', 1);
INSERT INTO `artist` VALUES (11, '莫文蔚', 1, '1656403993.jpg', 1);
INSERT INTO `artist` VALUES (12, '李代沫', 1, '1656404008.jpg', 0);
INSERT INTO `artist` VALUES (13, '卢冠廷', 1, '1656404069.jpg', 1);

-- ----------------------------
-- Table structure for collect
-- ----------------------------
DROP TABLE IF EXISTS `collect`;
CREATE TABLE `collect`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `song` int NULL DEFAULT NULL,
  `owner` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of collect
-- ----------------------------
INSERT INTO `collect` VALUES (1, 19, 2);
INSERT INTO `collect` VALUES (2, 15, 1);
INSERT INTO `collect` VALUES (3, 16, 2);
INSERT INTO `collect` VALUES (4, 11, 1);
INSERT INTO `collect` VALUES (5, 5, 2);
INSERT INTO `collect` VALUES (6, 21, 1);
INSERT INTO `collect` VALUES (7, 2, 1);
INSERT INTO `collect` VALUES (8, 4, 1);
INSERT INTO `collect` VALUES (9, 6, 2);
INSERT INTO `collect` VALUES (10, 12, 2);
INSERT INTO `collect` VALUES (11, 2, 2);
INSERT INTO `collect` VALUES (12, 17, 2);
INSERT INTO `collect` VALUES (13, 19, 1);
INSERT INTO `collect` VALUES (14, 2, 2);
INSERT INTO `collect` VALUES (15, 17, 1);
INSERT INTO `collect` VALUES (16, 19, 1);
INSERT INTO `collect` VALUES (17, 5, 2);
INSERT INTO `collect` VALUES (18, 13, 1);
INSERT INTO `collect` VALUES (19, 2, 2);
INSERT INTO `collect` VALUES (20, 4, 2);

-- ----------------------------
-- Table structure for song
-- ----------------------------
DROP TABLE IF EXISTS `song`;
CREATE TABLE `song`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `real_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `artist` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `file_url` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `hits` int NULL DEFAULT NULL,
  `genre` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of song
-- ----------------------------
INSERT INTO `song` VALUES (1, '一程山路', '毛不易', '1656491821.mp3', 0, 1);
INSERT INTO `song` VALUES (2, '追梦赤子心', 'GALA', '1656491868.mp3', 0, 1);
INSERT INTO `song` VALUES (3, '这就是爱情', '李代沫', '1656491890.mp3', 0, 1);
INSERT INTO `song` VALUES (4, '云烟成雨', '房东的猫', '1656491913.mp3', 0, 1);
INSERT INTO `song` VALUES (5, '一生所爱', '卢冠廷', '1656491932.mp3', 0, 1);
INSERT INTO `song` VALUES (6, '这世界那么多人', '莫文蔚', '1656491954.mp3', 0, 1);
INSERT INTO `song` VALUES (7, '永不失联的爱', '单依纯', '1656492073.mp3', 0, 1);
INSERT INTO `song` VALUES (8, '漠河舞厅', '戴羽彤', '1656492160.mp3', 0, 1);
INSERT INTO `song` VALUES (9, '最美的瞬间', '弹棉花的小花', '1656492189.mp3', 0, 1);
INSERT INTO `song` VALUES (10, '虞兮叹', '闻人听书', '1656492236.mp3', 0, 1);
INSERT INTO `song` VALUES (11, '开往早晨的午夜', '张碧晨', '1656492361.mp3', 0, 1);
INSERT INTO `song` VALUES (12, '只要平凡', '张碧晨', '1656492382.mp3', 0, 1);
INSERT INTO `song` VALUES (13, '认真的雪', '薛之谦', '1656492435.mp3', 0, 1);
INSERT INTO `song` VALUES (14, '演员', '薛之谦', '1656492448.mp3', 0, 1);
INSERT INTO `song` VALUES (15, '天外来物', '薛之谦', '1656492467.mp3', 0, 1);
INSERT INTO `song` VALUES (16, '带我去很远的地方', '黄霄云', '1656492525.mp3', 0, 1);
INSERT INTO `song` VALUES (17, 'NEW BOY', '朴树', '1656492592.mp3', 0, 1);
INSERT INTO `song` VALUES (18, '平凡之路', '朴树', '1656492617.mp3', 0, 1);
INSERT INTO `song` VALUES (19, '烟花易冷', '周杰伦', '1656492813.mp3', 0, 1);
INSERT INTO `song` VALUES (20, '如果这都不算爱', '张学友', '1656492930.mp3', 0, 1);
INSERT INTO `song` VALUES (21, '吻别', '张学友', '1656492946.mp3', 0, 1);

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `role` int NULL DEFAULT NULL,
  `deleted` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_info
-- ----------------------------
INSERT INTO `user_info` VALUES (1, 'lyx', '666', 0, 0);
INSERT INTO `user_info` VALUES (2, 'hxd', '123', 1, 0);

SET FOREIGN_KEY_CHECKS = 1;
