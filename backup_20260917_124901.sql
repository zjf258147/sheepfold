mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 5.7.44, for Linux (x86_64)
--
-- Host: localhost    Database: ims
-- ------------------------------------------------------
-- Server version	5.7.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('bd138515121c');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bom_detail`
--

DROP TABLE IF EXISTS `bom_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bom_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bom_id` int(11) NOT NULL COMMENT '鍏宠仈BOM涓昏〃',
  `material_sku_id` int(11) NOT NULL COMMENT '鍘熸潗鏂欑墿鏂橧D',
  `material_sku_code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍘熸潗鏂欑紪鐮?,
  `material_sku_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍘熸潗鏂欏悕绉?,
  `spec` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '瑙勬牸',
  `unit` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍗曚綅',
  `quantity_per_unit` decimal(10,3) NOT NULL COMMENT '鍗曞彴鐢ㄩ噺',
  `wastage_rate` decimal(5,2) DEFAULT NULL COMMENT '鎹熻€楃巼(%)',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `level` int(11) NOT NULL DEFAULT '2' COMMENT '灞傜骇锛?=鎴愬搧, 1=瀛愮粍浠? 2=闆朵欢',
  `parent_detail_id` int(11) DEFAULT NULL COMMENT '鐖剁骇鏄庣粏琛孖D锛堣嚜寮曠敤锛?,
  `item_version` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鏄庣粏琛岀増鏈紙濡侫00/V1.0.0锛?,
  `process_note` text COLLATE utf8mb4_unicode_ci COMMENT '宸ヨ壓璇存槑',
  PRIMARY KEY (`id`),
  KEY `material_sku_id` (`material_sku_id`),
  KEY `ix_bom_detail_bom_id` (`bom_id`),
  KEY `ix_bom_detail_parent_detail_id` (`parent_detail_id`),
  CONSTRAINT `bom_detail_ibfk_1` FOREIGN KEY (`bom_id`) REFERENCES `bom_header` (`id`) ON DELETE CASCADE,
  CONSTRAINT `bom_detail_ibfk_2` FOREIGN KEY (`material_sku_id`) REFERENCES `product_sku` (`id`),
  CONSTRAINT `fk_bom_detail_parent` FOREIGN KEY (`parent_detail_id`) REFERENCES `bom_detail` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bom_detail`
--

LOCK TABLES `bom_detail` WRITE;
/*!40000 ALTER TABLE `bom_detail` DISABLE KEYS */;
INSERT INTO `bom_detail` VALUES (1,1,4,'RM-MCU-H7','MCU 涓绘帶鑺墖 STM32H7','STM32H743','棰?,1.000,0.50,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(2,1,5,'RM-PMIC-12','鐢垫簮绠＄悊鑺墖 PMIC-12V','PMIC-12V-3A','棰?,2.000,1.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(3,1,6,'RM-FLASH-16','Flash 瀛樺偍鑺墖 16MB','W25Q128','棰?,1.000,0.50,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(4,1,7,'RM-WIFI-01','WiFi/BT 妯＄粍','ESP32-C3','涓?,1.000,1.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(5,1,8,'RM-CASE-200','閾濆悎閲戝澹?XG-200','XG-200-Housing','濂?,1.000,0.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(6,1,10,'RM-PCB-20','PCB 涓绘澘 V2.0','PCB-V2.0-4L','鍧?,1.000,2.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(7,1,11,'RM-BOX-01','褰╃洅鍖呰','350x250x80mm','涓?,1.000,0.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(8,1,12,'RM-MANUAL','璇存槑涔?淇濅慨鍗?,'A5-鍙岃','濂?,1.000,0.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(9,2,4,'RM-MCU-H7','MCU 涓绘帶鑺墖 STM32H7','STM32H743','棰?,1.000,0.50,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(10,2,5,'RM-PMIC-12','鐢垫簮绠＄悊鑺墖 PMIC-12V','PMIC-12V-3A','棰?,1.000,1.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(11,2,6,'RM-FLASH-16','Flash 瀛樺偍鑺墖 16MB','W25Q128','棰?,1.000,0.50,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(12,2,7,'RM-WIFI-01','WiFi/BT 妯＄粍','ESP32-C3','涓?,1.000,1.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(13,2,9,'RM-CASE-100','閾濆悎閲戝澹?XG-100','XG-100-Housing','濂?,1.000,0.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(14,2,10,'RM-PCB-20','PCB 涓绘澘 V2.0','PCB-V2.0-4L','鍧?,1.000,2.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(15,2,11,'RM-BOX-01','褰╃洅鍖呰','350x250x80mm','涓?,1.000,0.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL),(16,2,12,'RM-MANUAL','璇存槑涔?淇濅慨鍗?,'A5-鍙岃','濂?,1.000,0.00,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28',2,NULL,NULL,NULL);
/*!40000 ALTER TABLE `bom_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bom_header`
--

DROP TABLE IF EXISTS `bom_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bom_header` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bom_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'BOM缂栧彿',
  `bom_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'BOM鍚嶇О',
  `version` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鐗堟湰鍙?,
  `product_sku_id` int(11) NOT NULL COMMENT '鎴愬搧鐗╂枡ID',
  `product_sku_code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎴愬搧鐗╂枡缂栫爜',
  `product_sku_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎴愬搧鐗╂枡鍚嶇О',
  `plan_quantity` int(11) NOT NULL COMMENT '璁″垝鐢熶骇鏁伴噺',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'DRAFT' COMMENT '鐘舵€?,
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_by` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍒涘缓浜?,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bom_no` (`bom_no`),
  KEY `ix_bom_header_bom_no` (`bom_no`),
  KEY `ix_bom_header_product_sku_id` (`product_sku_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bom_header`
--

LOCK TABLES `bom_header` WRITE;
/*!40000 ALTER TABLE `bom_header` DISABLE KEYS */;
INSERT INTO `bom_header` VALUES (1,'BOM-2609-001','AIoT鏅鸿兘缃戝叧 XG-200 鏍囧噯BOM','V1.0',1,'FG-GW-200','AIoT 鏅鸿兘缃戝叧 XG-200',100,'PUBLISHED','2026骞碤3閲忎骇鐗堟湰','1','2026-09-07 09:51:28','2026-09-07 09:51:28'),(2,'BOM-2609-002','AIoT鏅鸿兘缃戝叧 XG-100 鏍囧噯BOM','V1.0',2,'FG-GW-100','AIoT 鏅鸿兘缃戝叧 XG-100',50,'PUBLISHED','2026骞碤3閲忎骇鐗堟湰','1','2026-09-07 09:51:28','2026-09-07 09:51:28'),(3,'BOM76645ACB','娴嬭瘯BOM','V1.0',2,'FG-GW-100','AIoT 鏅鸿兘缃戝叧 XG-100',100,'DRAFT','娴嬭瘯BOM瀵煎叆','admin','2026-09-08 05:18:06','2026-09-08 05:18:06');
/*!40000 ALTER TABLE `bom_header` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '瀹㈡埛ID',
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '瀹㈡埛鍚嶇О',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `weight` int(11) NOT NULL DEFAULT '0' COMMENT '鏉冮噸锛岃秺楂樿秺闈犲墠',
  `contact_person` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鑱旂郴浜?,
  `contact_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鑱旂郴鐢佃瘽',
  `contact_email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '閭',
  `address` text COLLATE utf8mb4_unicode_ci COMMENT '鍦板潃',
  `contract_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍚堝悓缂栧彿',
  `contract_start` date DEFAULT NULL COMMENT '鍚堝悓璧峰鏃ユ湡',
  `contract_end` date DEFAULT NULL COMMENT '鍚堝悓鍒版湡鏃ユ湡',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'鍖椾含鏅鸿仈绉戞妧鏈夐檺鍏徃','2026-09-07 09:51:28','2026-09-07 09:51:28',100,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'骞垮窞浜戝垱鏁版嵁鏈夐檺鍏徃','2026-09-07 09:51:28','2026-09-07 09:51:28',90,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'鍗庝负鎶€鏈湁闄愬叕鍙?,'2026-09-07 09:51:28','2026-09-07 09:51:28',95,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'涓浗绉诲姩閫氫俊闆嗗洟','2026-09-07 09:51:28','2026-09-07 09:51:28',85,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'鏉窞娴峰悍濞佽鏁板瓧鎶€鏈湁闄愬叕鍙?,'2026-09-07 09:51:28','2026-09-07 09:51:28',80,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6,'娣卞湷鑵捐璁＄畻鏈虹郴缁熸湁闄愬叕鍙?,'2026-09-07 09:51:28','2026-09-07 09:51:28',75,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,'闃块噷宸村反闆嗗洟','2026-09-07 09:51:28','2026-09-07 09:51:28',70,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8,'涓婃捣鍟嗘堡绉戞妧寮€鍙戞湁闄愬叕鍙?,'2026-09-07 09:51:28','2026-09-07 09:51:28',60,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_ledger`
--

DROP TABLE IF EXISTS `device_ledger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_ledger` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '鍙拌处ID',
  `item_sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '璁惧SN锛屽叧鑱攊nventory_item.item_sn',
  `station_id` int(11) NOT NULL COMMENT '鍦虹珯',
  `installed_date` date NOT NULL COMMENT '瀹夎鍒板満绔欐棩鏈?,
  `removed_date` date DEFAULT NULL COMMENT '绉婚櫎鏃ユ湡锛孨ULL=褰撳墠鍦ㄥ満绔?,
  `warranty_start` date DEFAULT NULL COMMENT '璐ㄤ繚璧峰鏃ユ湡',
  `warranty_end` date DEFAULT NULL COMMENT '璐ㄤ繚鍒版湡鏃ユ湡',
  `software_version` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '杞欢鐗堟湰鍙?,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '杩愯涓?鏁呴殰/宸插洖鏀?,
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  KEY `station_id` (`station_id`),
  KEY `ix_device_ledger_item_sn` (`item_sn`),
  KEY `ix_device_ledger_status` (`status`),
  CONSTRAINT `device_ledger_ibfk_1` FOREIGN KEY (`station_id`) REFERENCES `station` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_ledger`
--

LOCK TABLES `device_ledger` WRITE;
/*!40000 ALTER TABLE `device_ledger` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_ledger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inbound_order`
--

DROP TABLE IF EXISTS `inbound_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inbound_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'JIN-鍗曞彿',
  `inbound_mode` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'PROCUREMENT/NON_PROCUREMENT',
  `stock_condition` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍏ュ簱绫诲瀷/搴撳瓨灞炴€?,
  `partner_id` int(11) NOT NULL COMMENT '寰€鏉ュ崟浣?,
  `related_outbound_order_id` bigint(20) DEFAULT NULL COMMENT '鍏宠仈鍑哄簱鍗曪紙闈為噰璐叆搴擄級',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `operation_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_qty` int(11) NOT NULL COMMENT '鍟嗗搧鎬绘暟閲?,
  `submitted_by` int(11) DEFAULT NULL,
  `reviewed_by` int(11) DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_inbound_order_order_no` (`order_no`),
  KEY `related_outbound_order_id` (`related_outbound_order_id`),
  KEY `reviewed_by` (`reviewed_by`),
  KEY `submitted_by` (`submitted_by`),
  KEY `ix_inbound_order_operation_status` (`operation_status`),
  KEY `inbound_order_ibfk_1` (`partner_id`),
  CONSTRAINT `inbound_order_ibfk_1` FOREIGN KEY (`partner_id`) REFERENCES `partner` (`id`),
  CONSTRAINT `inbound_order_ibfk_2` FOREIGN KEY (`related_outbound_order_id`) REFERENCES `outbound_order` (`id`),
  CONSTRAINT `inbound_order_ibfk_3` FOREIGN KEY (`reviewed_by`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `inbound_order_ibfk_4` FOREIGN KEY (`submitted_by`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inbound_order`
--

LOCK TABLES `inbound_order` WRITE;
/*!40000 ALTER TABLE `inbound_order` DISABLE KEYS */;
INSERT INTO `inbound_order` VALUES (1,'JIN-260907-001','PROCUREMENT','NEW',1,NULL,'XG-200 棣栨壒閲忎骇鍏ュ簱','COMPLETED',30,2,1,'2026-08-31 00:00:00','2026-09-01 00:00:00','2026-09-07 09:51:28','2026-09-07 09:51:28'),(2,'JIN-260907-002','PROCUREMENT','NEW',2,NULL,'XG-100 鍏ュ簱','COMPLETED',20,2,1,'2026-09-02 00:00:00','2026-09-03 00:00:00','2026-09-07 09:51:28','2026-09-07 09:51:28'),(3,'JIN-260907-003','PROCUREMENT','NEW',3,NULL,'4G閫氫俊妯″潡鍏ュ簱','COMPLETED',50,2,1,'2026-09-04 00:00:00','2026-09-05 00:00:00','2026-09-07 09:51:28','2026-09-07 09:51:28'),(4,'JIN-20260908-0001','PROCUREMENT','NEW',10,NULL,'娴嬭瘯鍏ュ簱','INITIATED',50,1,NULL,NULL,NULL,'2026-09-08 05:16:30','2026-09-08 05:16:30');
/*!40000 ALTER TABLE `inbound_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inbound_order_item`
--

DROP TABLE IF EXISTS `inbound_order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inbound_order_item` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `inbound_order_id` bigint(20) NOT NULL,
  `line_id` bigint(20) NOT NULL,
  `item_id` bigint(20) DEFAULT NULL,
  `item_sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '褰曞叆鎴栫敓鎴愮殑SN',
  `sn_source` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'MANUAL/AUTO',
  PRIMARY KEY (`id`),
  KEY `item_id` (`item_id`),
  KEY `line_id` (`line_id`),
  KEY `ix_inbound_order_item_inbound_order_id` (`inbound_order_id`),
  CONSTRAINT `inbound_order_item_ibfk_1` FOREIGN KEY (`inbound_order_id`) REFERENCES `inbound_order` (`id`),
  CONSTRAINT `inbound_order_item_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `inventory_item` (`id`),
  CONSTRAINT `inbound_order_item_ibfk_3` FOREIGN KEY (`line_id`) REFERENCES `inbound_order_line` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inbound_order_item`
--

LOCK TABLES `inbound_order_item` WRITE;
/*!40000 ALTER TABLE `inbound_order_item` DISABLE KEYS */;
INSERT INTO `inbound_order_item` VALUES (1,1,1,1,'XG200-2609-0001','MANUAL'),(2,1,1,2,'XG200-2609-0002','MANUAL'),(3,1,1,3,'XG200-2609-0003','MANUAL'),(4,1,1,4,'XG200-2609-0004','MANUAL'),(5,1,1,5,'XG200-2609-0005','MANUAL'),(6,1,1,6,'XG200-2609-0006','MANUAL'),(7,1,1,7,'XG200-2609-0007','MANUAL'),(8,1,1,8,'XG200-2609-0008','MANUAL'),(9,1,1,9,'XG200-2609-0009','MANUAL'),(10,1,1,10,'XG200-2609-0010','MANUAL'),(11,1,1,11,'XG200-2609-0011','MANUAL'),(12,1,1,12,'XG200-2609-0012','MANUAL'),(13,1,1,13,'XG200-2609-0013','MANUAL'),(14,1,1,14,'XG200-2609-0014','MANUAL'),(15,1,1,15,'XG200-2609-0015','MANUAL'),(16,1,1,16,'XG200-2609-0016','MANUAL'),(17,1,1,17,'XG200-2609-0017','MANUAL'),(18,1,1,18,'XG200-2609-0018','MANUAL'),(19,1,1,19,'XG200-2609-0019','MANUAL'),(20,1,1,20,'XG200-2609-0020','MANUAL'),(21,1,1,21,'XG200-2609-0021','MANUAL'),(22,1,1,22,'XG200-2609-0022','MANUAL'),(23,1,1,23,'XG200-2609-0023','MANUAL'),(24,1,1,24,'XG200-2609-0024','MANUAL'),(25,1,1,25,'XG200-2609-0025','MANUAL'),(26,1,1,26,'XG200-2609-0026','MANUAL'),(27,1,1,27,'XG200-2609-0027','MANUAL'),(28,1,1,28,'XG200-2609-0028','MANUAL'),(29,1,1,29,'XG200-2609-0029','MANUAL'),(30,1,1,30,'XG200-2609-0030','MANUAL'),(31,2,2,31,'XG100-2609-0001','MANUAL'),(32,2,2,32,'XG100-2609-0002','MANUAL'),(33,2,2,33,'XG100-2609-0003','MANUAL'),(34,2,2,34,'XG100-2609-0004','MANUAL'),(35,2,2,35,'XG100-2609-0005','MANUAL'),(36,2,2,36,'XG100-2609-0006','MANUAL'),(37,2,2,37,'XG100-2609-0007','MANUAL'),(38,2,2,38,'XG100-2609-0008','MANUAL'),(39,2,2,39,'XG100-2609-0009','MANUAL'),(40,2,2,40,'XG100-2609-0010','MANUAL'),(41,2,2,41,'XG100-2609-0011','MANUAL'),(42,2,2,42,'XG100-2609-0012','MANUAL'),(43,2,2,43,'XG100-2609-0013','MANUAL'),(44,2,2,44,'XG100-2609-0014','MANUAL'),(45,2,2,45,'XG100-2609-0015','MANUAL'),(46,2,2,46,'XG100-2609-0016','MANUAL'),(47,2,2,47,'XG100-2609-0017','MANUAL'),(48,2,2,48,'XG100-2609-0018','MANUAL'),(49,2,2,49,'XG100-2609-0019','MANUAL'),(50,2,2,50,'XG100-2609-0020','MANUAL'),(51,3,3,51,'M4G-2609-0001','MANUAL'),(52,3,3,52,'M4G-2609-0002','MANUAL'),(53,3,3,53,'M4G-2609-0003','MANUAL'),(54,3,3,54,'M4G-2609-0004','MANUAL'),(55,3,3,55,'M4G-2609-0005','MANUAL'),(56,3,3,56,'M4G-2609-0006','MANUAL'),(57,3,3,57,'M4G-2609-0007','MANUAL'),(58,3,3,58,'M4G-2609-0008','MANUAL'),(59,3,3,59,'M4G-2609-0009','MANUAL'),(60,3,3,60,'M4G-2609-0010','MANUAL'),(61,3,3,61,'M4G-2609-0011','MANUAL'),(62,3,3,62,'M4G-2609-0012','MANUAL'),(63,3,3,63,'M4G-2609-0013','MANUAL'),(64,3,3,64,'M4G-2609-0014','MANUAL'),(65,3,3,65,'M4G-2609-0015','MANUAL'),(66,3,3,66,'M4G-2609-0016','MANUAL'),(67,3,3,67,'M4G-2609-0017','MANUAL'),(68,3,3,68,'M4G-2609-0018','MANUAL'),(69,3,3,69,'M4G-2609-0019','MANUAL'),(70,3,3,70,'M4G-2609-0020','MANUAL'),(71,3,3,71,'M4G-2609-0021','MANUAL'),(72,3,3,72,'M4G-2609-0022','MANUAL'),(73,3,3,73,'M4G-2609-0023','MANUAL'),(74,3,3,74,'M4G-2609-0024','MANUAL'),(75,3,3,75,'M4G-2609-0025','MANUAL'),(76,3,3,76,'M4G-2609-0026','MANUAL'),(77,3,3,77,'M4G-2609-0027','MANUAL'),(78,3,3,78,'M4G-2609-0028','MANUAL'),(79,3,3,79,'M4G-2609-0029','MANUAL'),(80,3,3,80,'M4G-2609-0030','MANUAL'),(81,3,3,81,'M4G-2609-0031','MANUAL'),(82,3,3,82,'M4G-2609-0032','MANUAL'),(83,3,3,83,'M4G-2609-0033','MANUAL'),(84,3,3,84,'M4G-2609-0034','MANUAL'),(85,3,3,85,'M4G-2609-0035','MANUAL'),(86,3,3,86,'M4G-2609-0036','MANUAL'),(87,3,3,87,'M4G-2609-0037','MANUAL'),(88,3,3,88,'M4G-2609-0038','MANUAL'),(89,3,3,89,'M4G-2609-0039','MANUAL'),(90,3,3,90,'M4G-2609-0040','MANUAL'),(91,3,3,91,'M4G-2609-0041','MANUAL'),(92,3,3,92,'M4G-2609-0042','MANUAL'),(93,3,3,93,'M4G-2609-0043','MANUAL'),(94,3,3,94,'M4G-2609-0044','MANUAL'),(95,3,3,95,'M4G-2609-0045','MANUAL'),(96,3,3,96,'M4G-2609-0046','MANUAL'),(97,3,3,97,'M4G-2609-0047','MANUAL'),(98,3,3,98,'M4G-2609-0048','MANUAL'),(99,3,3,99,'M4G-2609-0049','MANUAL'),(100,3,3,100,'M4G-2609-0050','MANUAL');
/*!40000 ALTER TABLE `inbound_order_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inbound_order_line`
--

DROP TABLE IF EXISTS `inbound_order_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inbound_order_line` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `inbound_order_id` bigint(20) NOT NULL,
  `sku_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL COMMENT '鍟嗗搧鏁伴噺',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `unit_price` decimal(12,2) DEFAULT NULL COMMENT '閲囪喘鍗曚环',
  PRIMARY KEY (`id`),
  KEY `sku_id` (`sku_id`),
  KEY `ix_inbound_order_line_inbound_order_id` (`inbound_order_id`),
  CONSTRAINT `inbound_order_line_ibfk_1` FOREIGN KEY (`inbound_order_id`) REFERENCES `inbound_order` (`id`),
  CONSTRAINT `inbound_order_line_ibfk_2` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inbound_order_line`
--

LOCK TABLES `inbound_order_line` WRITE;
/*!40000 ALTER TABLE `inbound_order_line` DISABLE KEYS */;
INSERT INTO `inbound_order_line` VALUES (1,1,1,30,'2026-09-07 09:51:28',2850.00),(2,2,2,20,'2026-09-07 09:51:28',1680.00),(3,3,3,50,'2026-09-07 09:51:28',320.00),(4,4,12,50,'2026-09-08 05:16:31',45.00);
/*!40000 ALTER TABLE `inbound_order_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incoming_inspection`
--

DROP TABLE IF EXISTS `incoming_inspection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `incoming_inspection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `receipt_id` int(11) NOT NULL COMMENT '鍒拌揣鍗?ID',
  `inspection_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '妫€楠岀紪鍙?,
  `inspector_id` int(11) NOT NULL COMMENT '妫€楠屼汉 ID',
  `inspection_date` date NOT NULL COMMENT '妫€楠屾棩鏈?,
  `result` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'ACCEPTED / CONCESSION_ACCEPTED / REJECTED',
  `sample_qty` int(11) NOT NULL DEFAULT '0' COMMENT '鎶芥牱鏁伴噺',
  `defect_qty` int(11) NOT NULL DEFAULT '0' COMMENT '涓嶈壇鏁伴噺',
  `defect_description` text COLLATE utf8mb4_unicode_ci COMMENT '涓嶈壇鎻忚堪',
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  KEY `inspector_id` (`inspector_id`),
  KEY `ix_incoming_inspection_receipt_id` (`receipt_id`),
  CONSTRAINT `incoming_inspection_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `incoming_receipt` (`id`),
  CONSTRAINT `incoming_inspection_ibfk_2` FOREIGN KEY (`inspector_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incoming_inspection`
--

LOCK TABLES `incoming_inspection` WRITE;
/*!40000 ALTER TABLE `incoming_inspection` DISABLE KEYS */;
INSERT INTO `incoming_inspection` VALUES (1,1,'INSP-260907-001',3,'2026-09-01','ACCEPTED',20,2,'灏戦噺寮曡剼姘у寲',NULL,'妫€楠岄€氳繃','2026-09-07 09:51:28','2026-09-07 09:51:28'),(2,2,'INSP-260907-002',3,'2026-09-03','ACCEPTED',20,1,'灏戦噺寮曡剼姘у寲',NULL,'妫€楠岄€氳繃','2026-09-07 09:51:28','2026-09-07 09:51:28'),(3,3,'INSP-260907-003',3,'2026-08-29','ACCEPTED',20,1,'灏戦噺寮曡剼姘у寲',NULL,'妫€楠岄€氳繃','2026-09-07 09:51:28','2026-09-07 09:51:28'),(4,4,'INSP-260907-004',3,'2026-08-13','ACCEPTED',20,0,'澶栬鏃犲紓甯革紝鐢垫皵鎬ц兘鍚堟牸',NULL,'妫€楠岄€氳繃','2026-09-07 09:51:28','2026-09-07 09:51:28'),(5,5,'INSP-260907-005',3,'2026-08-26','ACCEPTED',20,2,'灏戦噺寮曡剼姘у寲',NULL,'妫€楠岄€氳繃','2026-09-07 09:51:28','2026-09-07 09:51:28'),(6,8,'JC20260917001',1,'2026-09-17','ACCEPTED',10,0,NULL,'鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉','绉嶅瓙鏁版嵁','2026-09-17 01:26:52','2026-09-17 01:26:52'),(7,8,'JC20260917002',1,'2026-09-17','ACCEPTED',10,0,NULL,'鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉','绉嶅瓙鏁版嵁','2026-09-17 01:28:29','2026-09-17 01:28:29');
/*!40000 ALTER TABLE `incoming_inspection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incoming_receipt`
--

DROP TABLE IF EXISTS `incoming_receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `incoming_receipt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `receipt_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍒拌揣鍗曞彿',
  `supplier_id` int(11) NOT NULL COMMENT '渚涘簲鍟?ID',
  `sku_id` int(11) NOT NULL COMMENT '鐗╂枡 SKU ID',
  `batch_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎵规鍙?,
  `quantity` int(11) NOT NULL COMMENT '鍒拌揣鏁伴噺',
  `unit` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '涓? COMMENT '鍗曚綅',
  `status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDING_INSPECTION' COMMENT '鐘舵€?,
  `delivery_date` date NOT NULL COMMENT '鍒拌揣鏃ユ湡',
  `inspector_id` int(11) DEFAULT NULL COMMENT '妫€楠屼汉 ID',
  `inspection_date` date DEFAULT NULL COMMENT '妫€楠屾棩鏈?,
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `confirmed_at` datetime DEFAULT NULL COMMENT '鍏ュ簱纭鏃堕棿',
  `confirmed_by` int(11) DEFAULT NULL COMMENT '鍏ュ簱纭浜?ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_incoming_receipt_receipt_no` (`receipt_no`),
  KEY `inspector_id` (`inspector_id`),
  KEY `ix_incoming_receipt_supplier_id` (`supplier_id`),
  KEY `ix_incoming_receipt_sku_id` (`sku_id`),
  KEY `ix_incoming_receipt_status` (`status`),
  KEY `fk_incoming_receipt_confirmed_by` (`confirmed_by`),
  CONSTRAINT `fk_incoming_receipt_confirmed_by` FOREIGN KEY (`confirmed_by`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `incoming_receipt_ibfk_1` FOREIGN KEY (`supplier_id`) REFERENCES `partner` (`id`),
  CONSTRAINT `incoming_receipt_ibfk_2` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`),
  CONSTRAINT `incoming_receipt_ibfk_3` FOREIGN KEY (`inspector_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incoming_receipt`
--

LOCK TABLES `incoming_receipt` WRITE;
/*!40000 ALTER TABLE `incoming_receipt` DISABLE KEYS */;
INSERT INTO `incoming_receipt` VALUES (1,'RC-260907-001',1,4,'BATCH-2609-348',500,'棰?,'ACCEPTED','2026-09-02',3,'2026-09-01',NULL,'MCU 涓绘帶鑺墖 STM32H7 鏉ユ枡鎵规','2026-09-07 09:51:28','2026-09-07 09:51:28','2026-09-03 00:00:00',1),(2,'RC-260907-002',2,5,'BATCH-2609-724',1000,'棰?,'ACCEPTED','2026-08-24',3,'2026-09-03',NULL,'鐢垫簮绠＄悊鑺墖 PMIC-12V 鏉ユ枡鎵规','2026-09-07 09:51:28','2026-09-07 09:51:28','2026-08-29 00:00:00',1),(3,'RC-260907-003',1,6,'BATCH-2609-814',800,'棰?,'ACCEPTED','2026-09-05',3,'2026-08-29',NULL,'Flash 瀛樺偍鑺墖 16MB 鏉ユ枡鎵规','2026-09-07 09:51:28','2026-09-07 09:51:28','2026-08-22 00:00:00',1),(4,'RC-260907-004',2,7,'BATCH-2609-621',600,'涓?,'ACCEPTED','2026-08-20',3,'2026-08-13',NULL,'WiFi/BT 妯＄粍 鏉ユ枡鎵规','2026-09-07 09:51:28','2026-09-07 09:51:28','2026-08-27 00:00:00',1),(5,'RC-260907-005',3,8,'BATCH-2609-283',300,'濂?,'ACCEPTED','2026-08-24',3,'2026-08-26',NULL,'閾濆悎閲戝澹?XG-200 鏉ユ枡鎵规','2026-09-07 09:51:28','2026-09-07 09:51:28','2026-08-30 00:00:00',1),(6,'RC-260907-006',3,10,'BATCH-2609-963',200,'鍧?,'PENDING_INSPECTION','2026-08-27',3,NULL,NULL,'PCB 涓绘澘 V2.0 鏉ユ枡鎵规','2026-09-07 09:51:28','2026-09-07 09:51:28',NULL,NULL),(7,'LCR0DE0D923',10,12,'BATCH001',50,'濂?,'PENDING','2026-09-01',NULL,NULL,NULL,'娴嬭瘯鏉ユ枡瀵煎叆','2026-09-08 05:21:16','2026-09-08 05:21:16',NULL,NULL),(8,'RC-TEST-001',1,1,'BATCH-TEST',100,'涓?,'ACCEPTED','2026-09-09',1,'2026-09-17','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉',NULL,'2026-09-09 02:13:07','2026-09-17 01:26:52',NULL,NULL);
/*!40000 ALTER TABLE `incoming_receipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incoming_return`
--

DROP TABLE IF EXISTS `incoming_return`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `incoming_return` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `receipt_id` int(11) NOT NULL COMMENT '鍒拌揣鍗?ID',
  `return_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '閫€璐у崟鍙?,
  `return_qty` int(11) NOT NULL COMMENT '閫€璐ф暟閲?,
  `return_reason` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '閫€璐у師鍥?,
  `return_date` date NOT NULL COMMENT '閫€璐ф棩鏈?,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDING' COMMENT 'PENDING / CONFIRMED',
  `operator_id` int(11) NOT NULL COMMENT '鎿嶄綔浜?ID',
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_incoming_return_return_no` (`return_no`),
  KEY `operator_id` (`operator_id`),
  KEY `ix_incoming_return_receipt_id` (`receipt_id`),
  CONSTRAINT `incoming_return_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `incoming_receipt` (`id`),
  CONSTRAINT `incoming_return_ibfk_2` FOREIGN KEY (`operator_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incoming_return`
--

LOCK TABLES `incoming_return` WRITE;
/*!40000 ALTER TABLE `incoming_return` DISABLE KEYS */;
INSERT INTO `incoming_return` VALUES (1,4,'RT-260907-001',10,'WiFi妯＄粍閮ㄥ垎鎵规淇″彿寮哄害涓嶈揪鏍?,'2026-08-26','CONFIRMED',5,NULL,'渚涘簲鍟嗗凡纭閫€璐?,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(2,5,'RT-260907-002',5,'澶栧３琛ㄩ潰鏈夎交寰垝鐥曪紝涓嶇鍚堝瑙傛爣鍑?,'2026-09-02','PENDING',5,NULL,'寰呬緵搴斿晢纭','2026-09-07 09:51:28','2026-09-07 09:51:28');
/*!40000 ALTER TABLE `incoming_return` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_adjustment`
--

DROP TABLE IF EXISTS `inventory_adjustment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_adjustment` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '璋冩暣ID',
  `adjustment_no` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'TZ鍓嶇紑璋冩暣鍗曞彿',
  `stocktake_id` int(11) NOT NULL COMMENT '鐩樼偣浠诲姟ID',
  `stocktake_line_id` int(11) NOT NULL COMMENT '鐩樼偣鏄庣粏ID',
  `item_sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '璁惧SN',
  `adjustment_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'SURPLUS/SHORTAGE',
  `before_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '璋冩暣鍓嶅簱瀛樼姸鎬?,
  `after_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '璋冩暣鍚庡簱瀛樼姸鎬?,
  `reason` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '璋冩暣鍘熷洜',
  `operator_id` int(11) NOT NULL COMMENT '鎿嶄綔浜?,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_inventory_adjustment_adjustment_no` (`adjustment_no`),
  KEY `operator_id` (`operator_id`),
  KEY `stocktake_id` (`stocktake_id`),
  KEY `stocktake_line_id` (`stocktake_line_id`),
  CONSTRAINT `inventory_adjustment_ibfk_1` FOREIGN KEY (`operator_id`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `inventory_adjustment_ibfk_2` FOREIGN KEY (`stocktake_id`) REFERENCES `stocktake` (`id`),
  CONSTRAINT `inventory_adjustment_ibfk_3` FOREIGN KEY (`stocktake_line_id`) REFERENCES `stocktake_line` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_adjustment`
--

LOCK TABLES `inventory_adjustment` WRITE;
/*!40000 ALTER TABLE `inventory_adjustment` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_adjustment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_daily_summary`
--

DROP TABLE IF EXISTS `inventory_daily_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_daily_summary` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `snapshot_date` date NOT NULL COMMENT '涓氬姟鏃ユ湡',
  `opening_in_stock_qty` int(11) DEFAULT NULL COMMENT '鏈熷垵鍦ㄥ簱浠舵暟',
  `inbound_qty` int(11) NOT NULL DEFAULT '0' COMMENT '褰撴棩瀹℃牳鍏ュ簱浠舵暟',
  `outbound_qty` int(11) NOT NULL DEFAULT '0' COMMENT '褰撴棩瀹℃牳鍑哄簱浠舵暟',
  `closing_in_stock_qty` int(11) NOT NULL COMMENT '鏈熸湯鍦ㄥ簱浠舵暟',
  `closing_asset_amount` decimal(14,2) DEFAULT NULL COMMENT '鏈熸湯鍦ㄥ簱璧勪骇閲戦',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `snapshot_date` (`snapshot_date`),
  UNIQUE KEY `ix_inventory_daily_summary_snapshot_date` (`snapshot_date`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_daily_summary`
--

LOCK TABLES `inventory_daily_summary` WRITE;
/*!40000 ALTER TABLE `inventory_daily_summary` DISABLE KEYS */;
INSERT INTO `inventory_daily_summary` VALUES (1,'2026-08-08',10,8,0,18,27000.00,'2026-09-07 09:51:29'),(2,'2026-08-13',25,9,0,34,51000.00,'2026-09-07 09:51:29'),(3,'2026-08-18',40,0,5,35,52500.00,'2026-09-07 09:51:29'),(4,'2026-08-23',55,0,4,51,76500.00,'2026-09-07 09:51:29'),(5,'2026-08-28',70,1,5,66,99000.00,'2026-09-07 09:51:29'),(6,'2026-08-31',79,5,0,84,126000.00,'2026-09-07 09:51:29'),(7,'2026-09-02',85,0,3,82,123000.00,'2026-09-07 09:51:29'),(8,'2026-09-04',91,10,0,101,151500.00,'2026-09-07 09:51:29'),(9,'2026-09-05',94,6,0,100,150000.00,'2026-09-07 09:51:29'),(10,'2026-09-06',97,6,0,103,154500.00,'2026-09-07 09:51:29'),(11,'2026-09-07',103,0,0,100,135100.00,'2026-09-07 15:50:00'),(14,'2026-09-14',100,0,0,102,135100.00,'2026-09-14 15:50:05'),(15,'2026-09-15',102,0,0,102,135100.00,'2026-09-15 15:50:01'),(16,'2026-09-16',102,0,0,102,135100.00,'2026-09-16 15:50:00');
/*!40000 ALTER TABLE `inventory_daily_summary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_item`
--

DROP TABLE IF EXISTS `inventory_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_item` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `item_sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Item SN',
  `sku_id` int(11) NOT NULL COMMENT 'SKU ID',
  `stock_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '搴撳瓨鐘舵€?,
  `stock_condition` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '搴撳瓨灞炴€?,
  `operation_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎿嶄綔鐘舵€?,
  `last_order_no` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鏈€杩戝叧鑱斿崟鍙?,
  `quantity` int(11) NOT NULL COMMENT '鏁伴噺锛屽浐瀹氫负1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `unit_price` decimal(12,2) DEFAULT NULL COMMENT '閲囪喘鍗曚环',
  `replaced_by_sn` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '濡傛灉宸叉浛鎹紝鎸囧悜鏂?SN',
  `replaced_from_sn` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '濡傛灉鏄淮淇悗鏂?SN锛屾寚鍚戞棫 SN',
  `current_location` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '搴撴埧' COMMENT '搴撴埧/宸插彂鍑?缁翠慨涓?宸叉姤搴?,
  `warehouse_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'RAW_MATERIAL' COMMENT '浠撳簱绫诲瀷',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_inventory_item_item_sn` (`item_sn`),
  KEY `ix_inventory_item_sku_id` (`sku_id`),
  KEY `ix_inventory_item_stock_status` (`stock_status`),
  KEY `ix_inventory_item_warehouse_type` (`warehouse_type`),
  CONSTRAINT `inventory_item_ibfk_1` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_item`
--

LOCK TABLES `inventory_item` WRITE;
/*!40000 ALTER TABLE `inventory_item` DISABLE KEYS */;
INSERT INTO `inventory_item` VALUES (1,'XG200-2609-0001',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(2,'XG200-2609-0002',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(3,'XG200-2609-0003',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(4,'XG200-2609-0004',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(5,'XG200-2609-0005',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(6,'XG200-2609-0006',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(7,'XG200-2609-0007',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(8,'XG200-2609-0008',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(9,'XG200-2609-0009',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(10,'XG200-2609-0010',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(11,'XG200-2609-0011',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(12,'XG200-2609-0012',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(13,'XG200-2609-0013',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(14,'XG200-2609-0014',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(15,'XG200-2609-0015',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(16,'XG200-2609-0016',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(17,'XG200-2609-0017',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(18,'XG200-2609-0018',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(19,'XG200-2609-0019',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(20,'XG200-2609-0020',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(21,'XG200-2609-0021',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(22,'XG200-2609-0022',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(23,'XG200-2609-0023',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(24,'XG200-2609-0024',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(25,'XG200-2609-0025',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(26,'XG200-2609-0026',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(27,'XG200-2609-0027',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(28,'XG200-2609-0028',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(29,'XG200-2609-0029',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(30,'XG200-2609-0030',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'A鍖?01鏋?,'RAW_MATERIAL'),(31,'XG100-2609-0001',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(32,'XG100-2609-0002',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(33,'XG100-2609-0003',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(34,'XG100-2609-0004',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(35,'XG100-2609-0005',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(36,'XG100-2609-0006',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(37,'XG100-2609-0007',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(38,'XG100-2609-0008',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(39,'XG100-2609-0009',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(40,'XG100-2609-0010',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(41,'XG100-2609-0011',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(42,'XG100-2609-0012',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(43,'XG100-2609-0013',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(44,'XG100-2609-0014',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(45,'XG100-2609-0015',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(46,'XG100-2609-0016',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(47,'XG100-2609-0017',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(48,'XG100-2609-0018',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(49,'XG100-2609-0019',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(50,'XG100-2609-0020',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'A鍖?02鏋?,'RAW_MATERIAL'),(51,'M4G-2609-0001',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(52,'M4G-2609-0002',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(53,'M4G-2609-0003',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(54,'M4G-2609-0004',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(55,'M4G-2609-0005',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(56,'M4G-2609-0006',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(57,'M4G-2609-0007',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(58,'M4G-2609-0008',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(59,'M4G-2609-0009',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(60,'M4G-2609-0010',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(61,'M4G-2609-0011',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(62,'M4G-2609-0012',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(63,'M4G-2609-0013',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(64,'M4G-2609-0014',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(65,'M4G-2609-0015',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(66,'M4G-2609-0016',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(67,'M4G-2609-0017',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(68,'M4G-2609-0018',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(69,'M4G-2609-0019',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(70,'M4G-2609-0020',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(71,'M4G-2609-0021',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(72,'M4G-2609-0022',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(73,'M4G-2609-0023',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(74,'M4G-2609-0024',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(75,'M4G-2609-0025',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(76,'M4G-2609-0026',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(77,'M4G-2609-0027',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(78,'M4G-2609-0028',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(79,'M4G-2609-0029',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(80,'M4G-2609-0030',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(81,'M4G-2609-0031',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(82,'M4G-2609-0032',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(83,'M4G-2609-0033',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(84,'M4G-2609-0034',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(85,'M4G-2609-0035',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(86,'M4G-2609-0036',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(87,'M4G-2609-0037',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(88,'M4G-2609-0038',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(89,'M4G-2609-0039',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(90,'M4G-2609-0040',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(91,'M4G-2609-0041',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(92,'M4G-2609-0042',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(93,'M4G-2609-0043',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(94,'M4G-2609-0044',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(95,'M4G-2609-0045',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(96,'M4G-2609-0046',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(97,'M4G-2609-0047',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(98,'M4G-2609-0048',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(99,'M4G-2609-0049',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(100,'M4G-2609-0050',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',320.00,NULL,NULL,'B鍖?03鏋?,'RAW_MATERIAL'),(101,'XG200-2609-0031',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'宸插彂鍑?,'RAW_MATERIAL'),(102,'XG200-2609-0032',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'宸插彂鍑?,'RAW_MATERIAL'),(103,'XG200-2609-0033',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'宸插彂鍑?,'RAW_MATERIAL'),(104,'XG200-2609-0034',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'宸插彂鍑?,'RAW_MATERIAL'),(105,'XG200-2609-0035',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'宸插彂鍑?,'RAW_MATERIAL'),(106,'XG200-2609-0036',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'宸插彂鍑?,'RAW_MATERIAL'),(107,'XG200-2609-0037',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'宸插彂鍑?,'RAW_MATERIAL'),(108,'XG100-2609-0021',2,'RND','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'鐮斿彂閮?,'RAW_MATERIAL'),(109,'XG100-2609-0022',2,'RND','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'鐮斿彂閮?,'RAW_MATERIAL'),(110,'XG100-2609-0023',2,'RND','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',1680.00,NULL,NULL,'鐮斿彂閮?,'RAW_MATERIAL'),(111,'XG200-2609-0038',1,'BORROWED','NEW','COMPLETED',NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28',2850.00,NULL,NULL,'宸插€熷嚭','RAW_MATERIAL'),(112,'SN-TEST-INV-001',12,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-08 05:14:36','2026-09-08 05:14:36',NULL,NULL,NULL,'A搴?,'RAW_MATERIAL'),(113,'SN-TEST-INV-002',11,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09-08 05:14:36','2026-09-08 05:14:36',NULL,NULL,NULL,'B搴?,'RAW_MATERIAL');
/*!40000 ALTER TABLE `inventory_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_item_history`
--

DROP TABLE IF EXISTS `inventory_item_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_item_history` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `item_id` bigint(20) NOT NULL COMMENT '鍗曞搧ID',
  `event_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'INBOUND/OUTBOUND/STATUS_CHANGE',
  `order_no` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍏宠仈鍗曞彿',
  `from_stock_status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `to_stock_status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `from_operation_status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `to_operation_status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `operator_id` int(11) DEFAULT NULL,
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL COMMENT '璁板綍鏃堕棿',
  PRIMARY KEY (`id`),
  KEY `operator_id` (`operator_id`),
  KEY `ix_inventory_item_history_item_id` (`item_id`),
  CONSTRAINT `inventory_item_history_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `inventory_item` (`id`),
  CONSTRAINT `inventory_item_history_ibfk_2` FOREIGN KEY (`operator_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_item_history`
--

LOCK TABLES `inventory_item_history` WRITE;
/*!40000 ALTER TABLE `inventory_item_history` DISABLE KEYS */;
INSERT INTO `inventory_item_history` VALUES (1,1,'INBOUND','JIN-260907-001',NULL,'IN_STOCK',NULL,'COMPLETED',10,'閲囪喘鍏ュ簱','2026-08-31 00:00:00'),(2,2,'INBOUND','JIN-260907-001',NULL,'IN_STOCK',NULL,'COMPLETED',10,'閲囪喘鍏ュ簱','2026-08-31 00:00:00'),(3,3,'INBOUND','JIN-260907-001',NULL,'IN_STOCK',NULL,'COMPLETED',10,'閲囪喘鍏ュ簱','2026-08-31 00:00:00'),(4,4,'INBOUND','JIN-260907-001',NULL,'IN_STOCK',NULL,'COMPLETED',10,'閲囪喘鍏ュ簱','2026-08-31 00:00:00'),(5,5,'INBOUND','JIN-260907-001',NULL,'IN_STOCK',NULL,'COMPLETED',10,'閲囪喘鍏ュ簱','2026-08-31 00:00:00'),(6,101,'OUTBOUND','JOUT-260907-001','IN_STOCK','SOLD',NULL,'COMPLETED',10,'鍞嚭鍑哄簱','2026-09-06 00:00:00'),(7,102,'OUTBOUND','JOUT-260907-001','IN_STOCK','SOLD',NULL,'COMPLETED',10,'鍞嚭鍑哄簱','2026-09-06 00:00:00'),(8,103,'OUTBOUND','JOUT-260907-001','IN_STOCK','SOLD',NULL,'COMPLETED',10,'鍞嚭鍑哄簱','2026-09-06 00:00:00'),(9,104,'OUTBOUND','JOUT-260907-001','IN_STOCK','SOLD',NULL,'COMPLETED',10,'鍞嚭鍑哄簱','2026-09-06 00:00:00'),(10,105,'OUTBOUND','JOUT-260907-001','IN_STOCK','SOLD',NULL,'COMPLETED',10,'鍞嚭鍑哄簱','2026-09-06 00:00:00'),(11,106,'OUTBOUND','JOUT-260907-002','IN_STOCK','SAMPLE',NULL,'COMPLETED',10,'鏍锋満鍑哄簱','2026-08-29 00:00:00'),(12,107,'OUTBOUND','JOUT-260907-002','IN_STOCK','SAMPLE',NULL,'COMPLETED',10,'鏍锋満鍑哄簱','2026-08-29 00:00:00'),(13,108,'OUTBOUND','JOUT-260907-003','IN_STOCK','RND',NULL,'COMPLETED',3,'鐮斿彂鍑哄簱','2026-08-31 00:00:00'),(14,109,'OUTBOUND','JOUT-260907-003','IN_STOCK','RND',NULL,'COMPLETED',3,'鐮斿彂鍑哄簱','2026-08-31 00:00:00'),(15,110,'OUTBOUND','JOUT-260907-003','IN_STOCK','RND',NULL,'COMPLETED',3,'鐮斿彂鍑哄簱','2026-08-31 00:00:00'),(16,111,'OUTBOUND','JOUT-260907-004','IN_STOCK','BORROWED',NULL,'PICKING',10,'鍊熺敤鍑哄簱','2026-09-04 00:00:00');
/*!40000 ALTER TABLE `inventory_item_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_item_snapshot`
--

DROP TABLE IF EXISTS `inventory_item_snapshot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_item_snapshot` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `snapshot_at` datetime NOT NULL COMMENT '蹇収鏃堕棿',
  `item_id` bigint(20) NOT NULL COMMENT '鍘熷崟鍝両D',
  `item_sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sku_id` int(11) NOT NULL,
  `stock_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `stock_condition` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `operation_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_order_no` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `snapshot_month` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '蹇収鎵€灞炴湀浠斤紝鏍煎紡 YYYY-MM',
  `unit_price` decimal(12,2) DEFAULT NULL COMMENT '閲囪喘鍗曚环',
  `snapshot_date` date DEFAULT NULL COMMENT '蹇収涓氬姟鏃ユ湡',
  `snapshot_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'MONTHLY' COMMENT 'DAILY/MONTHLY',
  `warehouse_type` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '浠撳簱绫诲瀷',
  PRIMARY KEY (`id`),
  KEY `ix_inventory_item_snapshot_item_sn` (`item_sn`),
  KEY `ix_inventory_item_snapshot_snapshot_at` (`snapshot_at`),
  KEY `ix_inventory_item_snapshot_snapshot_month` (`snapshot_month`),
  KEY `ix_inventory_item_snapshot_snapshot_date` (`snapshot_date`),
  KEY `ix_inventory_item_snapshot_snapshot_type` (`snapshot_type`),
  KEY `ix_inventory_item_snapshot_date_type` (`snapshot_date`,`snapshot_type`)
) ENGINE=InnoDB AUTO_INCREMENT=896 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_item_snapshot`
--

LOCK TABLES `inventory_item_snapshot` WRITE;
/*!40000 ALTER TABLE `inventory_item_snapshot` DISABLE KEYS */;
INSERT INTO `inventory_item_snapshot` VALUES (1,'2026-09-07 23:59:59',1,'XG200-2609-0001',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(2,'2026-09-07 23:59:59',2,'XG200-2609-0002',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(3,'2026-09-07 23:59:59',3,'XG200-2609-0003',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(4,'2026-09-07 23:59:59',4,'XG200-2609-0004',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(5,'2026-09-07 23:59:59',5,'XG200-2609-0005',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(7,'2026-09-07 23:59:59',6,'XG200-2609-0006',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(9,'2026-09-07 23:59:59',7,'XG200-2609-0007',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(11,'2026-09-07 23:59:59',8,'XG200-2609-0008',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(13,'2026-09-07 23:59:59',9,'XG200-2609-0009',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(15,'2026-09-07 23:59:59',10,'XG200-2609-0010',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(17,'2026-09-07 23:59:59',11,'XG200-2609-0011',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(18,'2026-09-07 23:59:59',12,'XG200-2609-0012',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(21,'2026-09-07 23:59:59',13,'XG200-2609-0013',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(23,'2026-09-07 23:59:59',14,'XG200-2609-0014',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(24,'2026-09-07 23:59:59',15,'XG200-2609-0015',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(26,'2026-09-07 23:59:59',16,'XG200-2609-0016',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(28,'2026-09-07 23:59:59',17,'XG200-2609-0017',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(31,'2026-09-07 23:59:59',18,'XG200-2609-0018',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(33,'2026-09-07 23:59:59',19,'XG200-2609-0019',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(34,'2026-09-07 23:59:59',20,'XG200-2609-0020',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(37,'2026-09-07 23:59:59',21,'XG200-2609-0021',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(38,'2026-09-07 23:59:59',22,'XG200-2609-0022',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(40,'2026-09-07 23:59:59',23,'XG200-2609-0023',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(42,'2026-09-07 23:59:59',24,'XG200-2609-0024',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(44,'2026-09-07 23:59:59',25,'XG200-2609-0025',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(46,'2026-09-07 23:59:59',26,'XG200-2609-0026',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(48,'2026-09-07 23:59:59',27,'XG200-2609-0027',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(51,'2026-09-07 23:59:59',28,'XG200-2609-0028',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(52,'2026-09-07 23:59:59',29,'XG200-2609-0029',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(55,'2026-09-07 23:59:59',30,'XG200-2609-0030',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(56,'2026-09-07 23:59:59',31,'XG100-2609-0001',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(59,'2026-09-07 23:59:59',32,'XG100-2609-0002',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(61,'2026-09-07 23:59:59',33,'XG100-2609-0003',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(63,'2026-09-07 23:59:59',34,'XG100-2609-0004',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(64,'2026-09-07 23:59:59',35,'XG100-2609-0005',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(67,'2026-09-07 23:59:59',36,'XG100-2609-0006',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(69,'2026-09-07 23:59:59',37,'XG100-2609-0007',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(71,'2026-09-07 23:59:59',38,'XG100-2609-0008',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(72,'2026-09-07 23:59:59',39,'XG100-2609-0009',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(74,'2026-09-07 23:59:59',40,'XG100-2609-0010',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(77,'2026-09-07 23:59:59',41,'XG100-2609-0011',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(79,'2026-09-07 23:59:59',42,'XG100-2609-0012',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(80,'2026-09-07 23:59:59',43,'XG100-2609-0013',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(83,'2026-09-07 23:59:59',44,'XG100-2609-0014',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(84,'2026-09-07 23:59:59',45,'XG100-2609-0015',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(87,'2026-09-07 23:59:59',46,'XG100-2609-0016',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(88,'2026-09-07 23:59:59',47,'XG100-2609-0017',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(91,'2026-09-07 23:59:59',48,'XG100-2609-0018',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(92,'2026-09-07 23:59:59',49,'XG100-2609-0019',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(94,'2026-09-07 23:59:59',50,'XG100-2609-0020',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(97,'2026-09-07 23:59:59',51,'M4G-2609-0001',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(98,'2026-09-07 23:59:59',52,'M4G-2609-0002',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(100,'2026-09-07 23:59:59',53,'M4G-2609-0003',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(102,'2026-09-07 23:59:59',54,'M4G-2609-0004',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(104,'2026-09-07 23:59:59',55,'M4G-2609-0005',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(106,'2026-09-07 23:59:59',56,'M4G-2609-0006',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(108,'2026-09-07 23:59:59',57,'M4G-2609-0007',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(110,'2026-09-07 23:59:59',58,'M4G-2609-0008',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(113,'2026-09-07 23:59:59',59,'M4G-2609-0009',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(114,'2026-09-07 23:59:59',60,'M4G-2609-0010',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(117,'2026-09-07 23:59:59',61,'M4G-2609-0011',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(118,'2026-09-07 23:59:59',62,'M4G-2609-0012',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(120,'2026-09-07 23:59:59',63,'M4G-2609-0013',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(122,'2026-09-07 23:59:59',64,'M4G-2609-0014',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(125,'2026-09-07 23:59:59',65,'M4G-2609-0015',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(127,'2026-09-07 23:59:59',66,'M4G-2609-0016',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(129,'2026-09-07 23:59:59',67,'M4G-2609-0017',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(131,'2026-09-07 23:59:59',68,'M4G-2609-0018',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(132,'2026-09-07 23:59:59',69,'M4G-2609-0019',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(134,'2026-09-07 23:59:59',70,'M4G-2609-0020',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(136,'2026-09-07 23:59:59',71,'M4G-2609-0021',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(139,'2026-09-07 23:59:59',72,'M4G-2609-0022',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(140,'2026-09-07 23:59:59',73,'M4G-2609-0023',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(142,'2026-09-07 23:59:59',74,'M4G-2609-0024',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(145,'2026-09-07 23:59:59',75,'M4G-2609-0025',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(147,'2026-09-07 23:59:59',76,'M4G-2609-0026',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(149,'2026-09-07 23:59:59',77,'M4G-2609-0027',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(151,'2026-09-07 23:59:59',78,'M4G-2609-0028',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(152,'2026-09-07 23:59:59',79,'M4G-2609-0029',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(155,'2026-09-07 23:59:59',80,'M4G-2609-0030',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(156,'2026-09-07 23:59:59',81,'M4G-2609-0031',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(158,'2026-09-07 23:59:59',82,'M4G-2609-0032',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(160,'2026-09-07 23:59:59',83,'M4G-2609-0033',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(163,'2026-09-07 23:59:59',84,'M4G-2609-0034',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(164,'2026-09-07 23:59:59',85,'M4G-2609-0035',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(166,'2026-09-07 23:59:59',86,'M4G-2609-0036',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(169,'2026-09-07 23:59:59',87,'M4G-2609-0037',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(171,'2026-09-07 23:59:59',88,'M4G-2609-0038',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(173,'2026-09-07 23:59:59',89,'M4G-2609-0039',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(175,'2026-09-07 23:59:59',90,'M4G-2609-0040',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(177,'2026-09-07 23:59:59',91,'M4G-2609-0041',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(179,'2026-09-07 23:59:59',92,'M4G-2609-0042',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(181,'2026-09-07 23:59:59',93,'M4G-2609-0043',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(183,'2026-09-07 23:59:59',94,'M4G-2609-0044',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(185,'2026-09-07 23:59:59',95,'M4G-2609-0045',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(187,'2026-09-07 23:59:59',96,'M4G-2609-0046',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(189,'2026-09-07 23:59:59',97,'M4G-2609-0047',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(191,'2026-09-07 23:59:59',98,'M4G-2609-0048',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(194,'2026-09-07 23:59:59',99,'M4G-2609-0049',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(195,'2026-09-07 23:59:59',100,'M4G-2609-0050',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-07','DAILY',NULL),(197,'2026-09-07 23:59:59',101,'XG200-2609-0031',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(200,'2026-09-07 23:59:59',102,'XG200-2609-0032',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(202,'2026-09-07 23:59:59',103,'XG200-2609-0033',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(204,'2026-09-07 23:59:59',104,'XG200-2609-0034',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(206,'2026-09-07 23:59:59',105,'XG200-2609-0035',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(208,'2026-09-07 23:59:59',106,'XG200-2609-0036',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(209,'2026-09-07 23:59:59',107,'XG200-2609-0037',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(212,'2026-09-07 23:59:59',108,'XG100-2609-0021',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(214,'2026-09-07 23:59:59',109,'XG100-2609-0022',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(215,'2026-09-07 23:59:59',110,'XG100-2609-0023',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-07','DAILY',NULL),(217,'2026-09-07 23:59:59',111,'XG200-2609-0038',1,'BORROWED','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-07','DAILY',NULL),(444,'2026-09-14 23:59:59',1,'XG200-2609-0001',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(445,'2026-09-14 23:59:59',2,'XG200-2609-0002',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(446,'2026-09-14 23:59:59',3,'XG200-2609-0003',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(447,'2026-09-14 23:59:59',4,'XG200-2609-0004',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(448,'2026-09-14 23:59:59',5,'XG200-2609-0005',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(449,'2026-09-14 23:59:59',6,'XG200-2609-0006',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(450,'2026-09-14 23:59:59',7,'XG200-2609-0007',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(451,'2026-09-14 23:59:59',8,'XG200-2609-0008',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(452,'2026-09-14 23:59:59',9,'XG200-2609-0009',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(453,'2026-09-14 23:59:59',10,'XG200-2609-0010',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(454,'2026-09-14 23:59:59',11,'XG200-2609-0011',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(455,'2026-09-14 23:59:59',12,'XG200-2609-0012',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(456,'2026-09-14 23:59:59',13,'XG200-2609-0013',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(457,'2026-09-14 23:59:59',14,'XG200-2609-0014',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(458,'2026-09-14 23:59:59',15,'XG200-2609-0015',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(459,'2026-09-14 23:59:59',16,'XG200-2609-0016',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(460,'2026-09-14 23:59:59',17,'XG200-2609-0017',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(461,'2026-09-14 23:59:59',18,'XG200-2609-0018',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(462,'2026-09-14 23:59:59',19,'XG200-2609-0019',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(463,'2026-09-14 23:59:59',20,'XG200-2609-0020',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(464,'2026-09-14 23:59:59',21,'XG200-2609-0021',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(465,'2026-09-14 23:59:59',22,'XG200-2609-0022',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(466,'2026-09-14 23:59:59',23,'XG200-2609-0023',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(467,'2026-09-14 23:59:59',24,'XG200-2609-0024',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(468,'2026-09-14 23:59:59',25,'XG200-2609-0025',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(469,'2026-09-14 23:59:59',26,'XG200-2609-0026',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(470,'2026-09-14 23:59:59',27,'XG200-2609-0027',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(471,'2026-09-14 23:59:59',28,'XG200-2609-0028',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(472,'2026-09-14 23:59:59',29,'XG200-2609-0029',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(473,'2026-09-14 23:59:59',30,'XG200-2609-0030',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(474,'2026-09-14 23:59:59',31,'XG100-2609-0001',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(475,'2026-09-14 23:59:59',32,'XG100-2609-0002',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(476,'2026-09-14 23:59:59',33,'XG100-2609-0003',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(477,'2026-09-14 23:59:59',34,'XG100-2609-0004',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(478,'2026-09-14 23:59:59',35,'XG100-2609-0005',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(479,'2026-09-14 23:59:59',36,'XG100-2609-0006',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(480,'2026-09-14 23:59:59',37,'XG100-2609-0007',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(481,'2026-09-14 23:59:59',38,'XG100-2609-0008',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(482,'2026-09-14 23:59:59',39,'XG100-2609-0009',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(483,'2026-09-14 23:59:59',40,'XG100-2609-0010',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(484,'2026-09-14 23:59:59',41,'XG100-2609-0011',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(485,'2026-09-14 23:59:59',42,'XG100-2609-0012',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(486,'2026-09-14 23:59:59',43,'XG100-2609-0013',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(487,'2026-09-14 23:59:59',44,'XG100-2609-0014',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(488,'2026-09-14 23:59:59',45,'XG100-2609-0015',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(489,'2026-09-14 23:59:59',46,'XG100-2609-0016',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(490,'2026-09-14 23:59:59',47,'XG100-2609-0017',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(491,'2026-09-14 23:59:59',48,'XG100-2609-0018',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(492,'2026-09-14 23:59:59',49,'XG100-2609-0019',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(493,'2026-09-14 23:59:59',50,'XG100-2609-0020',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(494,'2026-09-14 23:59:59',51,'M4G-2609-0001',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(495,'2026-09-14 23:59:59',52,'M4G-2609-0002',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(496,'2026-09-14 23:59:59',53,'M4G-2609-0003',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(497,'2026-09-14 23:59:59',54,'M4G-2609-0004',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(498,'2026-09-14 23:59:59',55,'M4G-2609-0005',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(499,'2026-09-14 23:59:59',56,'M4G-2609-0006',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(500,'2026-09-14 23:59:59',57,'M4G-2609-0007',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(501,'2026-09-14 23:59:59',58,'M4G-2609-0008',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(502,'2026-09-14 23:59:59',59,'M4G-2609-0009',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(503,'2026-09-14 23:59:59',60,'M4G-2609-0010',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(504,'2026-09-14 23:59:59',61,'M4G-2609-0011',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(505,'2026-09-14 23:59:59',62,'M4G-2609-0012',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(506,'2026-09-14 23:59:59',63,'M4G-2609-0013',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(507,'2026-09-14 23:59:59',64,'M4G-2609-0014',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(508,'2026-09-14 23:59:59',65,'M4G-2609-0015',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(509,'2026-09-14 23:59:59',66,'M4G-2609-0016',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(510,'2026-09-14 23:59:59',67,'M4G-2609-0017',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(511,'2026-09-14 23:59:59',68,'M4G-2609-0018',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(512,'2026-09-14 23:59:59',69,'M4G-2609-0019',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(513,'2026-09-14 23:59:59',70,'M4G-2609-0020',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(514,'2026-09-14 23:59:59',71,'M4G-2609-0021',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(515,'2026-09-14 23:59:59',72,'M4G-2609-0022',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(516,'2026-09-14 23:59:59',73,'M4G-2609-0023',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(517,'2026-09-14 23:59:59',74,'M4G-2609-0024',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(518,'2026-09-14 23:59:59',75,'M4G-2609-0025',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(519,'2026-09-14 23:59:59',76,'M4G-2609-0026',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(520,'2026-09-14 23:59:59',77,'M4G-2609-0027',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(521,'2026-09-14 23:59:59',78,'M4G-2609-0028',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(522,'2026-09-14 23:59:59',79,'M4G-2609-0029',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(523,'2026-09-14 23:59:59',80,'M4G-2609-0030',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(524,'2026-09-14 23:59:59',81,'M4G-2609-0031',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(525,'2026-09-14 23:59:59',82,'M4G-2609-0032',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(526,'2026-09-14 23:59:59',83,'M4G-2609-0033',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(527,'2026-09-14 23:59:59',84,'M4G-2609-0034',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(528,'2026-09-14 23:59:59',85,'M4G-2609-0035',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(529,'2026-09-14 23:59:59',86,'M4G-2609-0036',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(530,'2026-09-14 23:59:59',87,'M4G-2609-0037',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(531,'2026-09-14 23:59:59',88,'M4G-2609-0038',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(532,'2026-09-14 23:59:59',89,'M4G-2609-0039',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(533,'2026-09-14 23:59:59',90,'M4G-2609-0040',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(534,'2026-09-14 23:59:59',91,'M4G-2609-0041',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(535,'2026-09-14 23:59:59',92,'M4G-2609-0042',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(536,'2026-09-14 23:59:59',93,'M4G-2609-0043',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(537,'2026-09-14 23:59:59',94,'M4G-2609-0044',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(538,'2026-09-14 23:59:59',95,'M4G-2609-0045',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(539,'2026-09-14 23:59:59',96,'M4G-2609-0046',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(540,'2026-09-14 23:59:59',97,'M4G-2609-0047',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(541,'2026-09-14 23:59:59',98,'M4G-2609-0048',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(542,'2026-09-14 23:59:59',99,'M4G-2609-0049',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(543,'2026-09-14 23:59:59',100,'M4G-2609-0050',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-14','DAILY','RAW_MATERIAL'),(544,'2026-09-14 23:59:59',101,'XG200-2609-0031',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(545,'2026-09-14 23:59:59',102,'XG200-2609-0032',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(546,'2026-09-14 23:59:59',103,'XG200-2609-0033',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(547,'2026-09-14 23:59:59',104,'XG200-2609-0034',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(548,'2026-09-14 23:59:59',105,'XG200-2609-0035',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(549,'2026-09-14 23:59:59',106,'XG200-2609-0036',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(550,'2026-09-14 23:59:59',107,'XG200-2609-0037',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(551,'2026-09-14 23:59:59',108,'XG100-2609-0021',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(552,'2026-09-14 23:59:59',109,'XG100-2609-0022',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(553,'2026-09-14 23:59:59',110,'XG100-2609-0023',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-14','DAILY','RAW_MATERIAL'),(554,'2026-09-14 23:59:59',111,'XG200-2609-0038',1,'BORROWED','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-14','DAILY','RAW_MATERIAL'),(555,'2026-09-14 23:59:59',112,'SN-TEST-INV-001',12,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',NULL,'2026-09-14','DAILY','RAW_MATERIAL'),(556,'2026-09-14 23:59:59',113,'SN-TEST-INV-002',11,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',NULL,'2026-09-14','DAILY','RAW_MATERIAL'),(557,'2026-09-15 23:59:59',1,'XG200-2609-0001',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(559,'2026-09-15 23:59:59',2,'XG200-2609-0002',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(560,'2026-09-15 23:59:59',3,'XG200-2609-0003',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(562,'2026-09-15 23:59:59',4,'XG200-2609-0004',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(565,'2026-09-15 23:59:59',5,'XG200-2609-0005',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(566,'2026-09-15 23:59:59',6,'XG200-2609-0006',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(568,'2026-09-15 23:59:59',7,'XG200-2609-0007',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(570,'2026-09-15 23:59:59',8,'XG200-2609-0008',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(572,'2026-09-15 23:59:59',9,'XG200-2609-0009',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(575,'2026-09-15 23:59:59',10,'XG200-2609-0010',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(577,'2026-09-15 23:59:59',11,'XG200-2609-0011',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(579,'2026-09-15 23:59:59',12,'XG200-2609-0012',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(580,'2026-09-15 23:59:59',13,'XG200-2609-0013',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(583,'2026-09-15 23:59:59',14,'XG200-2609-0014',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(585,'2026-09-15 23:59:59',15,'XG200-2609-0015',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(588,'2026-09-15 23:59:59',16,'XG200-2609-0016',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(590,'2026-09-15 23:59:59',17,'XG200-2609-0017',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(592,'2026-09-15 23:59:59',18,'XG200-2609-0018',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(594,'2026-09-15 23:59:59',19,'XG200-2609-0019',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(596,'2026-09-15 23:59:59',20,'XG200-2609-0020',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(598,'2026-09-15 23:59:59',21,'XG200-2609-0021',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(600,'2026-09-15 23:59:59',22,'XG200-2609-0022',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(602,'2026-09-15 23:59:59',23,'XG200-2609-0023',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(604,'2026-09-15 23:59:59',24,'XG200-2609-0024',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(605,'2026-09-15 23:59:59',25,'XG200-2609-0025',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(608,'2026-09-15 23:59:59',26,'XG200-2609-0026',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(610,'2026-09-15 23:59:59',27,'XG200-2609-0027',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(611,'2026-09-15 23:59:59',28,'XG200-2609-0028',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(614,'2026-09-15 23:59:59',29,'XG200-2609-0029',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(616,'2026-09-15 23:59:59',30,'XG200-2609-0030',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(617,'2026-09-15 23:59:59',31,'XG100-2609-0001',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(620,'2026-09-15 23:59:59',32,'XG100-2609-0002',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(622,'2026-09-15 23:59:59',33,'XG100-2609-0003',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(623,'2026-09-15 23:59:59',34,'XG100-2609-0004',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(626,'2026-09-15 23:59:59',35,'XG100-2609-0005',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(628,'2026-09-15 23:59:59',36,'XG100-2609-0006',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(630,'2026-09-15 23:59:59',37,'XG100-2609-0007',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(632,'2026-09-15 23:59:59',38,'XG100-2609-0008',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(634,'2026-09-15 23:59:59',39,'XG100-2609-0009',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(636,'2026-09-15 23:59:59',40,'XG100-2609-0010',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(638,'2026-09-15 23:59:59',41,'XG100-2609-0011',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(639,'2026-09-15 23:59:59',42,'XG100-2609-0012',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(641,'2026-09-15 23:59:59',43,'XG100-2609-0013',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(644,'2026-09-15 23:59:59',44,'XG100-2609-0014',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(646,'2026-09-15 23:59:59',45,'XG100-2609-0015',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(648,'2026-09-15 23:59:59',46,'XG100-2609-0016',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(650,'2026-09-15 23:59:59',47,'XG100-2609-0017',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(652,'2026-09-15 23:59:59',48,'XG100-2609-0018',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(654,'2026-09-15 23:59:59',49,'XG100-2609-0019',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(655,'2026-09-15 23:59:59',50,'XG100-2609-0020',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(657,'2026-09-15 23:59:59',51,'M4G-2609-0001',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(659,'2026-09-15 23:59:59',52,'M4G-2609-0002',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(661,'2026-09-15 23:59:59',53,'M4G-2609-0003',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(663,'2026-09-15 23:59:59',54,'M4G-2609-0004',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(665,'2026-09-15 23:59:59',55,'M4G-2609-0005',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(668,'2026-09-15 23:59:59',56,'M4G-2609-0006',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(669,'2026-09-15 23:59:59',57,'M4G-2609-0007',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(672,'2026-09-15 23:59:59',58,'M4G-2609-0008',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(674,'2026-09-15 23:59:59',59,'M4G-2609-0009',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(675,'2026-09-15 23:59:59',60,'M4G-2609-0010',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(678,'2026-09-15 23:59:59',61,'M4G-2609-0011',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(680,'2026-09-15 23:59:59',62,'M4G-2609-0012',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(682,'2026-09-15 23:59:59',63,'M4G-2609-0013',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(684,'2026-09-15 23:59:59',64,'M4G-2609-0014',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(687,'2026-09-15 23:59:59',65,'M4G-2609-0015',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(689,'2026-09-15 23:59:59',66,'M4G-2609-0016',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(690,'2026-09-15 23:59:59',67,'M4G-2609-0017',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(693,'2026-09-15 23:59:59',68,'M4G-2609-0018',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(695,'2026-09-15 23:59:59',69,'M4G-2609-0019',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(696,'2026-09-15 23:59:59',70,'M4G-2609-0020',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(698,'2026-09-15 23:59:59',71,'M4G-2609-0021',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(701,'2026-09-15 23:59:59',72,'M4G-2609-0022',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(703,'2026-09-15 23:59:59',73,'M4G-2609-0023',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(705,'2026-09-15 23:59:59',74,'M4G-2609-0024',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(707,'2026-09-15 23:59:59',75,'M4G-2609-0025',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(708,'2026-09-15 23:59:59',76,'M4G-2609-0026',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(711,'2026-09-15 23:59:59',77,'M4G-2609-0027',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(712,'2026-09-15 23:59:59',78,'M4G-2609-0028',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(715,'2026-09-15 23:59:59',79,'M4G-2609-0029',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(716,'2026-09-15 23:59:59',80,'M4G-2609-0030',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(719,'2026-09-15 23:59:59',81,'M4G-2609-0031',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(720,'2026-09-15 23:59:59',82,'M4G-2609-0032',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(723,'2026-09-15 23:59:59',83,'M4G-2609-0033',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(724,'2026-09-15 23:59:59',84,'M4G-2609-0034',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(726,'2026-09-15 23:59:59',85,'M4G-2609-0035',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(729,'2026-09-15 23:59:59',86,'M4G-2609-0036',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(730,'2026-09-15 23:59:59',87,'M4G-2609-0037',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(732,'2026-09-15 23:59:59',88,'M4G-2609-0038',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(735,'2026-09-15 23:59:59',89,'M4G-2609-0039',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(737,'2026-09-15 23:59:59',90,'M4G-2609-0040',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(739,'2026-09-15 23:59:59',91,'M4G-2609-0041',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(741,'2026-09-15 23:59:59',92,'M4G-2609-0042',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(743,'2026-09-15 23:59:59',93,'M4G-2609-0043',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(745,'2026-09-15 23:59:59',94,'M4G-2609-0044',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(747,'2026-09-15 23:59:59',95,'M4G-2609-0045',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(749,'2026-09-15 23:59:59',96,'M4G-2609-0046',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(750,'2026-09-15 23:59:59',97,'M4G-2609-0047',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(752,'2026-09-15 23:59:59',98,'M4G-2609-0048',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(754,'2026-09-15 23:59:59',99,'M4G-2609-0049',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(756,'2026-09-15 23:59:59',100,'M4G-2609-0050',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-15','DAILY','RAW_MATERIAL'),(759,'2026-09-15 23:59:59',101,'XG200-2609-0031',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(761,'2026-09-15 23:59:59',102,'XG200-2609-0032',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(763,'2026-09-15 23:59:59',103,'XG200-2609-0033',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(765,'2026-09-15 23:59:59',104,'XG200-2609-0034',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(767,'2026-09-15 23:59:59',105,'XG200-2609-0035',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(768,'2026-09-15 23:59:59',106,'XG200-2609-0036',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(770,'2026-09-15 23:59:59',107,'XG200-2609-0037',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(773,'2026-09-15 23:59:59',108,'XG100-2609-0021',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(775,'2026-09-15 23:59:59',109,'XG100-2609-0022',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(776,'2026-09-15 23:59:59',110,'XG100-2609-0023',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-15','DAILY','RAW_MATERIAL'),(778,'2026-09-15 23:59:59',111,'XG200-2609-0038',1,'BORROWED','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-15','DAILY','RAW_MATERIAL'),(781,'2026-09-15 23:59:59',112,'SN-TEST-INV-001',12,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',NULL,'2026-09-15','DAILY','RAW_MATERIAL'),(782,'2026-09-15 23:59:59',113,'SN-TEST-INV-002',11,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',NULL,'2026-09-15','DAILY','RAW_MATERIAL'),(783,'2026-09-16 23:59:59',1,'XG200-2609-0001',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(784,'2026-09-16 23:59:59',2,'XG200-2609-0002',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(785,'2026-09-16 23:59:59',3,'XG200-2609-0003',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(786,'2026-09-16 23:59:59',4,'XG200-2609-0004',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(787,'2026-09-16 23:59:59',5,'XG200-2609-0005',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(788,'2026-09-16 23:59:59',6,'XG200-2609-0006',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(789,'2026-09-16 23:59:59',7,'XG200-2609-0007',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(790,'2026-09-16 23:59:59',8,'XG200-2609-0008',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(791,'2026-09-16 23:59:59',9,'XG200-2609-0009',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(792,'2026-09-16 23:59:59',10,'XG200-2609-0010',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(793,'2026-09-16 23:59:59',11,'XG200-2609-0011',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(794,'2026-09-16 23:59:59',12,'XG200-2609-0012',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(795,'2026-09-16 23:59:59',13,'XG200-2609-0013',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(796,'2026-09-16 23:59:59',14,'XG200-2609-0014',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(797,'2026-09-16 23:59:59',15,'XG200-2609-0015',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(798,'2026-09-16 23:59:59',16,'XG200-2609-0016',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(799,'2026-09-16 23:59:59',17,'XG200-2609-0017',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(800,'2026-09-16 23:59:59',18,'XG200-2609-0018',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(801,'2026-09-16 23:59:59',19,'XG200-2609-0019',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(802,'2026-09-16 23:59:59',20,'XG200-2609-0020',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(803,'2026-09-16 23:59:59',21,'XG200-2609-0021',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(804,'2026-09-16 23:59:59',22,'XG200-2609-0022',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(805,'2026-09-16 23:59:59',23,'XG200-2609-0023',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(806,'2026-09-16 23:59:59',24,'XG200-2609-0024',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(807,'2026-09-16 23:59:59',25,'XG200-2609-0025',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(808,'2026-09-16 23:59:59',26,'XG200-2609-0026',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(809,'2026-09-16 23:59:59',27,'XG200-2609-0027',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(810,'2026-09-16 23:59:59',28,'XG200-2609-0028',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(811,'2026-09-16 23:59:59',29,'XG200-2609-0029',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(812,'2026-09-16 23:59:59',30,'XG200-2609-0030',1,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(813,'2026-09-16 23:59:59',31,'XG100-2609-0001',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(814,'2026-09-16 23:59:59',32,'XG100-2609-0002',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(815,'2026-09-16 23:59:59',33,'XG100-2609-0003',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(816,'2026-09-16 23:59:59',34,'XG100-2609-0004',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(817,'2026-09-16 23:59:59',35,'XG100-2609-0005',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(818,'2026-09-16 23:59:59',36,'XG100-2609-0006',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(819,'2026-09-16 23:59:59',37,'XG100-2609-0007',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(820,'2026-09-16 23:59:59',38,'XG100-2609-0008',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(821,'2026-09-16 23:59:59',39,'XG100-2609-0009',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(822,'2026-09-16 23:59:59',40,'XG100-2609-0010',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(823,'2026-09-16 23:59:59',41,'XG100-2609-0011',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(824,'2026-09-16 23:59:59',42,'XG100-2609-0012',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(825,'2026-09-16 23:59:59',43,'XG100-2609-0013',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(826,'2026-09-16 23:59:59',44,'XG100-2609-0014',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(827,'2026-09-16 23:59:59',45,'XG100-2609-0015',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(828,'2026-09-16 23:59:59',46,'XG100-2609-0016',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(829,'2026-09-16 23:59:59',47,'XG100-2609-0017',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(830,'2026-09-16 23:59:59',48,'XG100-2609-0018',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(831,'2026-09-16 23:59:59',49,'XG100-2609-0019',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(832,'2026-09-16 23:59:59',50,'XG100-2609-0020',2,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(833,'2026-09-16 23:59:59',51,'M4G-2609-0001',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(834,'2026-09-16 23:59:59',52,'M4G-2609-0002',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(835,'2026-09-16 23:59:59',53,'M4G-2609-0003',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(836,'2026-09-16 23:59:59',54,'M4G-2609-0004',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(837,'2026-09-16 23:59:59',55,'M4G-2609-0005',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(838,'2026-09-16 23:59:59',56,'M4G-2609-0006',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(839,'2026-09-16 23:59:59',57,'M4G-2609-0007',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(840,'2026-09-16 23:59:59',58,'M4G-2609-0008',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(841,'2026-09-16 23:59:59',59,'M4G-2609-0009',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(842,'2026-09-16 23:59:59',60,'M4G-2609-0010',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(843,'2026-09-16 23:59:59',61,'M4G-2609-0011',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(844,'2026-09-16 23:59:59',62,'M4G-2609-0012',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(845,'2026-09-16 23:59:59',63,'M4G-2609-0013',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(846,'2026-09-16 23:59:59',64,'M4G-2609-0014',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(847,'2026-09-16 23:59:59',65,'M4G-2609-0015',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(848,'2026-09-16 23:59:59',66,'M4G-2609-0016',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(849,'2026-09-16 23:59:59',67,'M4G-2609-0017',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(850,'2026-09-16 23:59:59',68,'M4G-2609-0018',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(851,'2026-09-16 23:59:59',69,'M4G-2609-0019',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(852,'2026-09-16 23:59:59',70,'M4G-2609-0020',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(853,'2026-09-16 23:59:59',71,'M4G-2609-0021',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(854,'2026-09-16 23:59:59',72,'M4G-2609-0022',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(855,'2026-09-16 23:59:59',73,'M4G-2609-0023',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(856,'2026-09-16 23:59:59',74,'M4G-2609-0024',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(857,'2026-09-16 23:59:59',75,'M4G-2609-0025',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(858,'2026-09-16 23:59:59',76,'M4G-2609-0026',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(859,'2026-09-16 23:59:59',77,'M4G-2609-0027',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(860,'2026-09-16 23:59:59',78,'M4G-2609-0028',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(861,'2026-09-16 23:59:59',79,'M4G-2609-0029',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(862,'2026-09-16 23:59:59',80,'M4G-2609-0030',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(863,'2026-09-16 23:59:59',81,'M4G-2609-0031',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(864,'2026-09-16 23:59:59',82,'M4G-2609-0032',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(865,'2026-09-16 23:59:59',83,'M4G-2609-0033',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(866,'2026-09-16 23:59:59',84,'M4G-2609-0034',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(867,'2026-09-16 23:59:59',85,'M4G-2609-0035',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(868,'2026-09-16 23:59:59',86,'M4G-2609-0036',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(869,'2026-09-16 23:59:59',87,'M4G-2609-0037',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(870,'2026-09-16 23:59:59',88,'M4G-2609-0038',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(871,'2026-09-16 23:59:59',89,'M4G-2609-0039',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(872,'2026-09-16 23:59:59',90,'M4G-2609-0040',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(873,'2026-09-16 23:59:59',91,'M4G-2609-0041',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(874,'2026-09-16 23:59:59',92,'M4G-2609-0042',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(875,'2026-09-16 23:59:59',93,'M4G-2609-0043',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(876,'2026-09-16 23:59:59',94,'M4G-2609-0044',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(877,'2026-09-16 23:59:59',95,'M4G-2609-0045',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(878,'2026-09-16 23:59:59',96,'M4G-2609-0046',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(879,'2026-09-16 23:59:59',97,'M4G-2609-0047',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(880,'2026-09-16 23:59:59',98,'M4G-2609-0048',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(881,'2026-09-16 23:59:59',99,'M4G-2609-0049',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(882,'2026-09-16 23:59:59',100,'M4G-2609-0050',3,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',320.00,'2026-09-16','DAILY','RAW_MATERIAL'),(883,'2026-09-16 23:59:59',101,'XG200-2609-0031',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(884,'2026-09-16 23:59:59',102,'XG200-2609-0032',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(885,'2026-09-16 23:59:59',103,'XG200-2609-0033',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(886,'2026-09-16 23:59:59',104,'XG200-2609-0034',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(887,'2026-09-16 23:59:59',105,'XG200-2609-0035',1,'SOLD','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(888,'2026-09-16 23:59:59',106,'XG200-2609-0036',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(889,'2026-09-16 23:59:59',107,'XG200-2609-0037',1,'SAMPLE','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(890,'2026-09-16 23:59:59',108,'XG100-2609-0021',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(891,'2026-09-16 23:59:59',109,'XG100-2609-0022',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(892,'2026-09-16 23:59:59',110,'XG100-2609-0023',2,'RND','NEW','COMPLETED',NULL,1,'2026-09',1680.00,'2026-09-16','DAILY','RAW_MATERIAL'),(893,'2026-09-16 23:59:59',111,'XG200-2609-0038',1,'BORROWED','NEW','COMPLETED',NULL,1,'2026-09',2850.00,'2026-09-16','DAILY','RAW_MATERIAL'),(894,'2026-09-16 23:59:59',112,'SN-TEST-INV-001',12,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',NULL,'2026-09-16','DAILY','RAW_MATERIAL'),(895,'2026-09-16 23:59:59',113,'SN-TEST-INV-002',11,'IN_STOCK','NEW','COMPLETED',NULL,1,'2026-09',NULL,'2026-09-16','DAILY','RAW_MATERIAL');
/*!40000 ALTER TABLE `inventory_item_snapshot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_sku_daily_ledger`
--

DROP TABLE IF EXISTS `inventory_sku_daily_ledger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_sku_daily_ledger` (
  `snapshot_date` date NOT NULL COMMENT '涓氬姟鏃ユ湡',
  `sku_id` int(11) NOT NULL COMMENT 'SKU ID',
  `opening_in_stock_qty` int(11) DEFAULT NULL COMMENT '鏈熷垵鍦ㄥ簱浠舵暟',
  `inbound_qty` int(11) NOT NULL DEFAULT '0' COMMENT '褰撴棩瀹℃牳鍏ュ簱浠舵暟',
  `outbound_qty` int(11) NOT NULL DEFAULT '0' COMMENT '褰撴棩瀹℃牳鍑哄簱浠舵暟',
  `closing_in_stock_qty` int(11) NOT NULL COMMENT '鏈熸湯鍦ㄥ簱浠舵暟',
  `closing_asset_amount` decimal(14,2) DEFAULT NULL COMMENT '鏈熸湯鍦ㄥ簱璧勪骇閲戦',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `inbound_new` int(11) NOT NULL DEFAULT '0',
  `inbound_returned_from_sale` int(11) NOT NULL DEFAULT '0',
  `inbound_returned_from_sold_offline` int(11) NOT NULL DEFAULT '0',
  `inbound_returned_from_presold` int(11) NOT NULL DEFAULT '0',
  `inbound_returned_from_gift` int(11) NOT NULL DEFAULT '0',
  `inbound_returned_from_scrapped` int(11) NOT NULL DEFAULT '0',
  `inbound_returned_from_rnd` int(11) NOT NULL DEFAULT '0',
  `inbound_returned_from_sample` int(11) NOT NULL DEFAULT '0',
  `inbound_returned_from_trial` int(11) NOT NULL DEFAULT '0',
  `inbound_returned_from_repair` int(11) NOT NULL DEFAULT '0',
  `outbound_trial` int(11) NOT NULL DEFAULT '0',
  `outbound_scrapped` int(11) NOT NULL DEFAULT '0',
  `outbound_borrowed` int(11) NOT NULL DEFAULT '0',
  `outbound_sold_offline` int(11) NOT NULL DEFAULT '0',
  `outbound_gifted` int(11) NOT NULL DEFAULT '0',
  `outbound_sample` int(11) NOT NULL DEFAULT '0',
  `outbound_presold` int(11) NOT NULL DEFAULT '0',
  `outbound_repair` int(11) NOT NULL DEFAULT '0',
  `outbound_rnd` int(11) NOT NULL DEFAULT '0',
  `outbound_sold` int(11) NOT NULL DEFAULT '0',
  `outbound_dept_procurement` int(11) NOT NULL DEFAULT '0' COMMENT '鍑哄簱-閮ㄩ棬閲囪喘',
  `inbound_returned_from_dept_procurement` int(11) NOT NULL DEFAULT '0' COMMENT '鍏ュ簱-閮ㄩ棬閲囪喘閫€鍥?,
  PRIMARY KEY (`snapshot_date`,`sku_id`),
  KEY `sku_id` (`sku_id`),
  CONSTRAINT `inventory_sku_daily_ledger_ibfk_1` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_sku_daily_ledger`
--

LOCK TABLES `inventory_sku_daily_ledger` WRITE;
/*!40000 ALTER TABLE `inventory_sku_daily_ledger` DISABLE KEYS */;
INSERT INTO `inventory_sku_daily_ledger` VALUES ('2026-09-07',1,0,0,0,30,85500.00,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',2,0,0,0,20,33600.00,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',3,0,0,0,50,16000.00,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',4,0,0,0,0,NULL,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',5,0,0,0,0,NULL,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',6,0,0,0,0,NULL,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',7,0,0,0,0,NULL,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',8,0,0,0,0,NULL,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',9,0,0,0,0,NULL,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',10,0,0,0,0,NULL,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',11,0,0,0,0,NULL,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-07',12,0,0,0,0,NULL,'2026-09-07 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',1,30,0,0,30,85500.00,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',2,20,0,0,20,33600.00,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',3,50,0,0,50,16000.00,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',4,0,0,0,0,NULL,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',5,0,0,0,0,NULL,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',6,0,0,0,0,NULL,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',7,0,0,0,0,NULL,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',8,0,0,0,0,NULL,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',9,0,0,0,0,NULL,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',10,0,0,0,0,NULL,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',11,0,0,0,1,0.00,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-14',12,0,0,0,1,0.00,'2026-09-14 15:50:05',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',1,30,0,0,30,85500.00,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',2,20,0,0,20,33600.00,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',3,50,0,0,50,16000.00,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',4,0,0,0,0,NULL,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',5,0,0,0,0,NULL,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',6,0,0,0,0,NULL,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',7,0,0,0,0,NULL,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',8,0,0,0,0,NULL,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',9,0,0,0,0,NULL,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',10,0,0,0,0,NULL,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',11,1,0,0,1,0.00,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-15',12,1,0,0,1,0.00,'2026-09-15 15:50:01',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',1,30,0,0,30,85500.00,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',2,20,0,0,20,33600.00,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',3,50,0,0,50,16000.00,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',4,0,0,0,0,NULL,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',5,0,0,0,0,NULL,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',6,0,0,0,0,NULL,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',7,0,0,0,0,NULL,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',8,0,0,0,0,NULL,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',9,0,0,0,0,NULL,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',10,0,0,0,0,NULL,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',11,1,0,0,1,0.00,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2026-09-16',12,1,0,0,1,0.00,'2026-09-16 15:50:00',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `inventory_sku_daily_ledger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `outbound_order`
--

DROP TABLE IF EXISTS `outbound_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `outbound_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_no` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'JOUT-鍗曞彿',
  `outbound_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'SOLD/BORROWED/GIFTED/SCRAPPED',
  `partner_id` int(11) NOT NULL COMMENT '寰€鏉ュ崟浣?,
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `operation_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_qty` int(11) NOT NULL,
  `submitted_by` int(11) DEFAULT NULL,
  `reviewed_by` int(11) DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `customer_name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '瀹㈡埛鍚嶇О',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_outbound_order_order_no` (`order_no`),
  KEY `reviewed_by` (`reviewed_by`),
  KEY `submitted_by` (`submitted_by`),
  KEY `ix_outbound_order_operation_status` (`operation_status`),
  KEY `outbound_order_ibfk_1` (`partner_id`),
  CONSTRAINT `outbound_order_ibfk_1` FOREIGN KEY (`partner_id`) REFERENCES `partner` (`id`),
  CONSTRAINT `outbound_order_ibfk_2` FOREIGN KEY (`reviewed_by`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `outbound_order_ibfk_3` FOREIGN KEY (`submitted_by`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outbound_order`
--

LOCK TABLES `outbound_order` WRITE;
/*!40000 ALTER TABLE `outbound_order` DISABLE KEYS */;
INSERT INTO `outbound_order` VALUES (1,'JOUT-260907-001','SOLD',5,'XG-200 棣栨壒鍑鸿揣','COMPLETED',5,2,1,'2026-09-05 00:00:00','2026-09-06 00:00:00','2026-09-07 09:51:28','2026-09-07 09:51:28','鍖椾含鏅鸿仈绉戞妧鏈夐檺鍏徃'),(2,'JOUT-260907-002','SAMPLE',7,'XG-200 鏍锋満閫佹祴鍗庝负','COMPLETED',2,2,1,'2026-08-28 00:00:00','2026-08-29 00:00:00','2026-09-07 09:51:28','2026-09-07 09:51:28','鍗庝负鎶€鏈湁闄愬叕鍙?),(3,'JOUT-260907-003','RND',9,'XG-100 鐮斿彂娴嬭瘯鐢ㄦ満','COMPLETED',3,4,1,'2026-08-30 00:00:00','2026-08-31 00:00:00','2026-09-07 09:51:28','2026-09-07 09:51:28','娣卞湷璧涙牸鐢靛瓙甯傚満鏈夐檺鍏徃'),(4,'JOUT-260907-004','BORROWED',8,'鍊熺敤XG-200 1鍙扮敤浜庣幇鍦烘紨绀?,'PICKING',1,2,NULL,'2026-09-04 00:00:00',NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','涓浗绉诲姩閫氫俊闆嗗洟'),(5,'JOUT-20260908-0001','SOLD_ONLINE',10,'娴嬭瘯鍑哄簱','INITIATED',0,1,NULL,'2026-09-11 17:38:16',NULL,'2026-09-08 05:16:49','2026-09-11 09:38:15','娴嬭瘯瀹㈡埛');
/*!40000 ALTER TABLE `outbound_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `outbound_order_item`
--

DROP TABLE IF EXISTS `outbound_order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `outbound_order_item` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `outbound_order_id` bigint(20) NOT NULL,
  `item_id` bigint(20) NOT NULL,
  `sku_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `item_id` (`item_id`),
  KEY `sku_id` (`sku_id`),
  KEY `ix_outbound_order_item_outbound_order_id` (`outbound_order_id`),
  CONSTRAINT `outbound_order_item_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `inventory_item` (`id`),
  CONSTRAINT `outbound_order_item_ibfk_2` FOREIGN KEY (`outbound_order_id`) REFERENCES `outbound_order` (`id`),
  CONSTRAINT `outbound_order_item_ibfk_3` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outbound_order_item`
--

LOCK TABLES `outbound_order_item` WRITE;
/*!40000 ALTER TABLE `outbound_order_item` DISABLE KEYS */;
INSERT INTO `outbound_order_item` VALUES (1,1,101,1,1),(2,1,102,1,1),(3,1,103,1,1),(4,1,104,1,1),(5,1,105,1,1),(6,2,106,1,1),(7,2,107,1,1),(8,3,108,2,1),(9,3,109,2,1),(10,3,110,2,1),(11,4,111,1,1);
/*!40000 ALTER TABLE `outbound_order_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner`
--

DROP TABLE IF EXISTS `partner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partner` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '鍗曚綅ID',
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍗曚綅鍚嶇О',
  `group_id` int(11) NOT NULL COMMENT '鍒嗙粍ID',
  `partner_type` smallint(6) NOT NULL COMMENT '0=渚涘簲鍟?瀹㈡埛 1=瀹㈡埛 2=渚涘簲鍟?,
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '澶囨敞',
  `status` smallint(6) NOT NULL COMMENT '1=鍚敤 0=鍋滅敤',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  KEY `ix_partner_group_id` (`group_id`),
  CONSTRAINT `partner_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `partner_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner`
--

LOCK TABLES `partner` WRITE;
/*!40000 ALTER TABLE `partner` DISABLE KEYS */;
INSERT INTO `partner` VALUES (1,'娣卞湷鍗庡己鐢靛瓙鏈夐檺鍏徃',1,2,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(2,'涓婃捣鑺簮寰數瀛愭湁闄愬叕鍙?,1,2,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(3,'涓滆帪绮惧瘑浜旈噾鍒跺搧鏈夐檺鍏徃',2,2,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(4,'鑻忓窞鍗氫笘鍖呰鏉愭枡鏈夐檺鍏徃',3,2,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(5,'鍖椾含鏅鸿仈绉戞妧鏈夐檺鍏徃',4,1,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(6,'骞垮窞浜戝垱鏁版嵁鏈夐檺鍏徃',4,1,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(7,'鍗庝负鎶€鏈湁闄愬叕鍙?,5,1,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(8,'涓浗绉诲姩閫氫俊闆嗗洟',5,1,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(9,'娣卞湷璧涙牸鐢靛瓙甯傚満鏈夐檺鍏徃',1,0,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(10,'鏉窞娴峰悍濞佽鏁板瓧鎶€鏈湁闄愬叕鍙?,5,1,NULL,1,'2026-09-07 09:51:28','2026-09-07 09:51:28');
/*!40000 ALTER TABLE `partner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner_group`
--

DROP TABLE IF EXISTS `partner_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partner_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '鍒嗙粍ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍒嗙粍鍚嶇О',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner_group`
--

LOCK TABLES `partner_group` WRITE;
/*!40000 ALTER TABLE `partner_group` DISABLE KEYS */;
INSERT INTO `partner_group` VALUES (1,'鑺墖渚涘簲鍟?,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(2,'缁撴瀯浠朵緵搴斿晢','2026-09-07 09:51:28','2026-09-07 09:51:28'),(3,'鍖呰渚涘簲鍟?,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(4,'缁忛攢鍟?,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(5,'缁堢瀹㈡埛','2026-09-07 09:51:28','2026-09-07 09:51:28');
/*!40000 ALTER TABLE `partner_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_category`
--

DROP TABLE IF EXISTS `product_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '鍒嗙被ID',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍒嗙被鍚嶇О',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_category`
--

LOCK TABLES `product_category` WRITE;
/*!40000 ALTER TABLE `product_category` DISABLE KEYS */;
INSERT INTO `product_category` VALUES (1,'鎴愬搧鈥旀櫤鑳借澶?,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(2,'鎴愬搧鈥旈厤浠?,'2026-09-07 09:51:28','2026-09-07 09:51:28'),(3,'鍘熸潗鏂欌€旂數瀛愬厓鍣ㄤ欢','2026-09-07 09:51:28','2026-09-07 09:51:28'),(4,'鍘熸潗鏂欌€旂粨鏋勪欢','2026-09-07 09:51:28','2026-09-07 09:51:28'),(5,'鍘熸潗鏂欌€斿寘瑁呮潗鏂?,'2026-09-07 09:51:28','2026-09-07 09:51:28');
/*!40000 ALTER TABLE `product_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_sku`
--

DROP TABLE IF EXISTS `product_sku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_sku` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '鍟嗗搧ID',
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍟嗗搧鍚嶇О',
  `category_id` int(11) NOT NULL COMMENT '鍒嗙被ID',
  `barcode` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鏉＄爜缂栫爜锛屽 NO00001',
  `sn_mode` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'SN妯″紡锛歁ANUAL/AUTO/BOTH',
  `status` smallint(6) NOT NULL COMMENT '1=鍚敤 0=鍋滅敤',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `unit` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '璁￠噺鍗曚綅锛屽 涓?寮?浠?鍓?,
  `sku_code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鐗╂枡缂栫爜锛圲9缂栫爜锛?,
  `spec` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '瑙勬牸鍨嬪彿',
  `sku_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'FINISHED_GOODS' COMMENT '鐗╂枡绫诲瀷',
  PRIMARY KEY (`id`),
  UNIQUE KEY `barcode` (`barcode`),
  UNIQUE KEY `uq_product_sku_sku_code` (`sku_code`),
  KEY `ix_product_sku_category_id` (`category_id`),
  CONSTRAINT `product_sku_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_sku`
--

LOCK TABLES `product_sku` WRITE;
/*!40000 ALTER TABLE `product_sku` DISABLE KEYS */;
INSERT INTO `product_sku` VALUES (1,'AIoT 鏅鸿兘缃戝叧 XG-200',1,'CP00001','BOTH',1,'鏃楄埌娆炬櫤鑳界綉鍏?,'2026-09-07 09:51:28','2026-09-07 09:51:28','鍙?,'FG-GW-200','XG-200','FINISHED_GOODS'),(2,'AIoT 鏅鸿兘缃戝叧 XG-100',1,'CP00002','BOTH',1,'鏍囧噯娆炬櫤鑳界綉鍏?,'2026-09-07 09:51:28','2026-09-07 09:51:28','鍙?,'FG-GW-100','XG-100','FINISHED_GOODS'),(3,'4G 閫氫俊妯″潡 M-4G',2,'CP00003','MANUAL',1,'4G閫氫俊閰嶄欢','2026-09-07 09:51:28','2026-09-07 09:51:28','涓?,'FG-4G-01','M-4G-v2','FINISHED_GOODS'),(4,'MCU 涓绘帶鑺墖 STM32H7',3,'RM00001','MANUAL',1,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','棰?,'RM-MCU-H7','STM32H743','RAW_MATERIAL'),(5,'鐢垫簮绠＄悊鑺墖 PMIC-12V',3,'RM00002','MANUAL',1,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','棰?,'RM-PMIC-12','PMIC-12V-3A','RAW_MATERIAL'),(6,'Flash 瀛樺偍鑺墖 16MB',3,'RM00003','MANUAL',1,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','棰?,'RM-FLASH-16','W25Q128','RAW_MATERIAL'),(7,'WiFi/BT 妯＄粍',3,'RM00004','MANUAL',1,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','涓?,'RM-WIFI-01','ESP32-C3','RAW_MATERIAL'),(8,'閾濆悎閲戝澹?XG-200',4,'RM00005','MANUAL',1,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','濂?,'RM-CASE-200','XG-200-Housing','RAW_MATERIAL'),(9,'閾濆悎閲戝澹?XG-100',4,'RM00006','MANUAL',1,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','濂?,'RM-CASE-100','XG-100-Housing','RAW_MATERIAL'),(10,'PCB 涓绘澘 V2.0',4,'RM00007','MANUAL',1,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','鍧?,'RM-PCB-20','PCB-V2.0-4L','RAW_MATERIAL'),(11,'褰╃洅鍖呰',5,'RM00008','MANUAL',1,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','涓?,'RM-BOX-01','350x250x80mm','RAW_MATERIAL'),(12,'璇存槑涔?淇濅慨鍗?,5,'RM00009','MANUAL',1,NULL,'2026-09-07 09:51:28','2026-09-07 09:51:28','濂?,'RM-MANUAL','A5-鍙岃','RAW_MATERIAL');
/*!40000 ALTER TABLE `product_sku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_task`
--

DROP TABLE IF EXISTS `production_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `production_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '浠诲姟缂栧彿',
  `bom_id` int(11) NOT NULL COMMENT '鍏宠仈BOM',
  `plan_quantity` int(11) NOT NULL COMMENT '璁″垝鐢熶骇鏁伴噺',
  `material_availability` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'SHORTAGE' COMMENT '榻愬鐘舵€?,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDING' COMMENT '鐘舵€?,
  `start_date` date DEFAULT NULL COMMENT '璁″垝寮€濮嬫棩鏈?,
  `end_date` date DEFAULT NULL COMMENT '璁″垝瀹屾垚鏃ユ湡',
  `created_by` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍒涘缓浜?,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `product_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'FINISHED_PRODUCT' COMMENT '浜у嚭绫诲瀷锛欶INISHED_PRODUCT/SEMI_FINISHED',
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_no` (`task_no`),
  KEY `ix_production_task_task_no` (`task_no`),
  KEY `ix_production_task_bom_id` (`bom_id`),
  CONSTRAINT `production_task_ibfk_1` FOREIGN KEY (`bom_id`) REFERENCES `bom_header` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_task`
--

LOCK TABLES `production_task` WRITE;
/*!40000 ALTER TABLE `production_task` DISABLE KEYS */;
INSERT INTO `production_task` VALUES (1,'TASK-2609-001',1,50,'COMPLETE','COMPLETED','2026-08-18','2026-08-28','3','2026-09-07 09:51:28','2026-09-07 09:51:28','FINISHED_PRODUCT'),(2,'TASK-2609-002',1,30,'COMPLETE','IN_PROGRESS','2026-09-02','2026-09-17','3','2026-09-07 09:51:28','2026-09-07 09:51:28','FINISHED_PRODUCT'),(3,'TASK-2609-003',2,20,'SHORTAGE','IN_PROGRESS','2026-09-12','2026-09-27','3','2026-09-07 09:51:28','2026-09-15 09:48:50','FINISHED_PRODUCT');
/*!40000 ALTER TABLE `production_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material_inventory`
--

DROP TABLE IF EXISTS `raw_material_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw_material_inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sku_id` int(11) NOT NULL COMMENT '鐗╂枡 SKU ID',
  `batch_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎵规鍙?,
  `quantity` int(11) NOT NULL DEFAULT '0' COMMENT '搴撳瓨鏁伴噺',
  `unit` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '涓? COMMENT '鍗曚綅',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'IN_STOCK' COMMENT '搴撳瓨鐘舵€?,
  `supplier_id` int(11) DEFAULT NULL COMMENT '渚涘簲鍟?ID',
  `receipt_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍏宠仈鍒拌揣鍗曞彿',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  KEY `ix_raw_material_inventory_sku_id` (`sku_id`),
  KEY `ix_raw_material_inventory_batch_no` (`batch_no`),
  KEY `ix_raw_material_inventory_supplier_id` (`supplier_id`),
  CONSTRAINT `raw_material_inventory_ibfk_1` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`),
  CONSTRAINT `raw_material_inventory_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `partner` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_inventory`
--

LOCK TABLES `raw_material_inventory` WRITE;
/*!40000 ALTER TABLE `raw_material_inventory` DISABLE KEYS */;
INSERT INTO `raw_material_inventory` VALUES (1,4,'BATCH-2609-348',250,'棰?,'IN_STOCK',1,'RC-260907-001','MCU 涓绘帶鑺墖 STM32H7 鏉ユ枡鎵规 鈥?搴撳瓨鎵规','2026-08-20 00:00:00','2026-08-28 00:00:00'),(2,5,'BATCH-2609-724',500,'棰?,'IN_STOCK',2,'RC-260907-002','鐢垫簮绠＄悊鑺墖 PMIC-12V 鏉ユ枡鎵规 鈥?搴撳瓨鎵规','2026-08-25 00:00:00','2026-08-30 00:00:00'),(3,6,'BATCH-2609-814',400,'棰?,'IN_STOCK',1,'RC-260907-003','Flash 瀛樺偍鑺墖 16MB 鏉ユ枡鎵规 鈥?搴撳瓨鎵规','2026-08-30 00:00:00','2026-08-31 00:00:00'),(4,7,'BATCH-2609-621',300,'涓?,'IN_STOCK',2,'RC-260907-004','WiFi/BT 妯＄粍 鏉ユ枡鎵规 鈥?搴撳瓨鎵规','2026-08-21 00:00:00','2026-08-20 00:00:00'),(5,8,'BATCH-2609-283',150,'濂?,'IN_STOCK',3,'RC-260907-005','閾濆悎閲戝澹?XG-200 鏉ユ枡鎵规 鈥?搴撳瓨鎵规','2026-08-25 00:00:00','2026-08-27 00:00:00');
/*!40000 ALTER TABLE `raw_material_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material_inventory_log`
--

DROP TABLE IF EXISTS `raw_material_inventory_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw_material_inventory_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL COMMENT '搴撳瓨鎵规 ID',
  `sn_id` int(11) DEFAULT NULL COMMENT 'SN ID锛堟寜 SN 鎵ｅ噺鏃惰褰曪級',
  `change_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'INCREASE / DECREASE',
  `change_qty` int(11) NOT NULL COMMENT '鍙樻洿鏁伴噺',
  `before_qty` int(11) NOT NULL COMMENT '鍙樻洿鍓嶆暟閲?,
  `after_qty` int(11) NOT NULL COMMENT '鍙樻洿鍚庢暟閲?,
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `related_order_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍏宠仈鍗曞彿',
  `operator_id` int(11) DEFAULT NULL COMMENT '鎿嶄綔浜?ID',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL COMMENT '鎿嶄綔鏃堕棿',
  PRIMARY KEY (`id`),
  KEY `sn_id` (`sn_id`),
  KEY `operator_id` (`operator_id`),
  KEY `ix_raw_material_inventory_log_inventory_id` (`inventory_id`),
  CONSTRAINT `raw_material_inventory_log_ibfk_1` FOREIGN KEY (`inventory_id`) REFERENCES `raw_material_inventory` (`id`),
  CONSTRAINT `raw_material_inventory_log_ibfk_2` FOREIGN KEY (`sn_id`) REFERENCES `raw_material_sn` (`id`),
  CONSTRAINT `raw_material_inventory_log_ibfk_3` FOREIGN KEY (`operator_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_inventory_log`
--

LOCK TABLES `raw_material_inventory_log` WRITE;
/*!40000 ALTER TABLE `raw_material_inventory_log` DISABLE KEYS */;
INSERT INTO `raw_material_inventory_log` VALUES (1,1,NULL,'INCREASE',250,0,250,'鏉ユ枡妫€楠屽悎鏍煎叆搴?,'RC-260907-001',5,'鏉ユ枡鍏ュ簱','2026-08-25 00:00:00'),(2,2,NULL,'INCREASE',500,0,500,'鏉ユ枡妫€楠屽悎鏍煎叆搴?,'RC-260907-002',5,'鏉ユ枡鍏ュ簱','2026-08-24 00:00:00'),(3,3,NULL,'INCREASE',400,0,400,'鏉ユ枡妫€楠屽悎鏍煎叆搴?,'RC-260907-003',5,'鏉ユ枡鍏ュ簱','2026-08-26 00:00:00'),(4,4,NULL,'INCREASE',300,0,300,'鏉ユ枡妫€楠屽悎鏍煎叆搴?,'RC-260907-004',5,'鏉ユ枡鍏ュ簱','2026-08-20 00:00:00'),(5,5,NULL,'INCREASE',150,0,150,'鏉ユ枡妫€楠屽悎鏍煎叆搴?,'RC-260907-005',5,'鏉ユ枡鍏ュ簱','2026-08-22 00:00:00');
/*!40000 ALTER TABLE `raw_material_inventory_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material_sn`
--

DROP TABLE IF EXISTS `raw_material_sn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw_material_sn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL COMMENT '搴撳瓨鎵规 ID',
  `sn` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍘熸潗鏂?SN 鍙?,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'IN_STOCK' COMMENT 'SN 鐘舵€?,
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  KEY `ix_raw_material_sn_inventory_id` (`inventory_id`),
  KEY `ix_raw_material_sn_sn` (`sn`),
  CONSTRAINT `raw_material_sn_ibfk_1` FOREIGN KEY (`inventory_id`) REFERENCES `raw_material_inventory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_sn`
--

LOCK TABLES `raw_material_sn` WRITE;
/*!40000 ALTER TABLE `raw_material_sn` DISABLE KEYS */;
/*!40000 ALTER TABLE `raw_material_sn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rma_diagnosis`
--

DROP TABLE IF EXISTS `rma_diagnosis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rma_diagnosis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `return_id` int(11) NOT NULL COMMENT '杩斿巶閫€璐у崟 ID',
  `diagnosis_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '璇婃柇缂栧彿 DG',
  `diagnosed_by` int(11) NOT NULL COMMENT '璇婃柇浜?ID',
  `diagnosis_date` date NOT NULL COMMENT '璇婃柇鏃ユ湡',
  `fault_description` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鏁呴殰鎻忚堪',
  `diagnosis_result` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '璇婃柇缁撴灉',
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `repair_plan` text COLLATE utf8mb4_unicode_ci COMMENT '缁翠慨鏂规',
  `inspection_report_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '閫佹鍗曠紪鍙?,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_rma_diagnosis_diagnosis_no` (`diagnosis_no`),
  KEY `fk_rma_diagnosis_diagnosed_by` (`diagnosed_by`),
  KEY `ix_rma_diagnosis_return_id` (`return_id`),
  CONSTRAINT `fk_rma_diagnosis_diagnosed_by` FOREIGN KEY (`diagnosed_by`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `fk_rma_diagnosis_return_id` FOREIGN KEY (`return_id`) REFERENCES `rma_return` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rma_diagnosis`
--

LOCK TABLES `rma_diagnosis` WRITE;
/*!40000 ALTER TABLE `rma_diagnosis` DISABLE KEYS */;
INSERT INTO `rma_diagnosis` VALUES (1,2,'DG-260907-001',6,'2026-08-30','4G閫氫俊妯″潡涓庝富鏉胯繛鎺ュ紓甯革紝澶╃嚎鎺ュ彛鏉惧姩瀵艰嚧淇″彿涓嶇ǔ瀹?,'REPAIRABLE',NULL,'4G妯″潡鎵规闂锛屽缓璁悓鎵规浜у搧棰勯槻鎬ф鏌?,'2026-09-07 09:51:29','2026-09-07 09:51:29','閲嶆柊鐒婃帴澶╃嚎鎺ュ彛锛屾洿鎹?G閫氫俊妯″潡锛屾洿鏂板浐浠惰嚦V2.3.1','INSP-260907-006'),(2,3,'DG-260907-002',6,'2026-09-03','澶栧３鍙充笅瑙掔鎾炲彉褰紝鍐呴儴PCB鏃犳崯浼わ紝鍔熻兘姝ｅ父','REPAIRABLE',NULL,'寤鸿鍔犲己杩愯緭鍖呰','2026-09-07 09:51:29','2026-09-07 09:51:29','鏇存崲澶栧３锛岄噸鏂板仛闃叉按娴嬭瘯',NULL),(3,4,'DG-260907-003',6,'2026-08-18','杩涙按瀵艰嚧涓绘澘鑵愯殌锛孧CU涓绘帶鑺墖STM32H7寮曡剼姘у寲鏂锛孭CB澶氬眰鏉垮眰闂寸煭璺?,'SCRAP',NULL,'鎶ュ簾瀹℃壒涓?,'2026-09-07 09:51:29','2026-09-07 09:51:29','涓绘澘鏇存崲鎴愭湰锟?100锛岃秴杩囨柊鏈烘垚鏈殑70%锛屽缓璁姤搴熷鐞?,NULL),(4,7,'DG20260917001',1,'2026-09-17','娴嬭瘯鏁呴殰锛氳嚜鍔ㄥ寲娴嬭瘯鐢?,'REPAIRABLE','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉','绉嶅瓙鏁版嵁','2026-09-17 01:27:05','2026-09-17 01:27:05',NULL,NULL),(5,8,'DG20260917002',1,'2026-09-17','娴嬭瘯鏁呴殰锛氱數婧愭ā鍧楀紓甯?,'REPAIRABLE','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉','绉嶅瓙鏁版嵁','2026-09-17 01:28:39','2026-09-17 01:28:39',NULL,NULL);
/*!40000 ALTER TABLE `rma_diagnosis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rma_quality_check`
--

DROP TABLE IF EXISTS `rma_quality_check`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rma_quality_check` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `return_id` int(11) NOT NULL COMMENT '杩斿巶閫€璐у崟 ID',
  `checked_by` int(11) NOT NULL COMMENT '妫€楠屼汉 ID',
  `check_date` date NOT NULL COMMENT '妫€楠屾棩鏈?,
  `check_result` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '妫€楠岀粨鏋滐細PASS / FAIL',
  `check_description` text COLLATE utf8mb4_unicode_ci COMMENT '妫€楠屾弿杩?,
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  KEY `fk_rma_quality_check_checked_by` (`checked_by`),
  KEY `ix_rma_quality_check_return_id` (`return_id`),
  CONSTRAINT `fk_rma_quality_check_checked_by` FOREIGN KEY (`checked_by`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `fk_rma_quality_check_return_id` FOREIGN KEY (`return_id`) REFERENCES `rma_return` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rma_quality_check`
--

LOCK TABLES `rma_quality_check` WRITE;
/*!40000 ALTER TABLE `rma_quality_check` DISABLE KEYS */;
INSERT INTO `rma_quality_check` VALUES (1,2,5,'2026-08-30','PASS','4G淇″彿娴嬭瘯姝ｅ父锛岃繛缁繍琛?4灏忔椂鏃犳帀绾匡紝鍚勯」鎸囨爣鍚堟牸',NULL,'璐ㄩ噺妫€楠岄€氳繃锛屽彲鍏ュ簱','2026-09-07 09:51:29','2026-09-07 09:51:29'),(2,3,5,'2026-09-04','PASS','澶栬妫€楠屽悎鏍硷紝闃叉按娴嬭瘯閫氳繃锛屽姛鑳芥祴璇曟甯?,NULL,'璐ㄩ噺妫€楠岄€氳繃锛屽彲鍏ュ簱鎴栧啀鍑鸿揣','2026-09-07 09:51:29','2026-09-07 09:51:29');
/*!40000 ALTER TABLE `rma_quality_check` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rma_repair`
--

DROP TABLE IF EXISTS `rma_repair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rma_repair` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `return_id` int(11) NOT NULL COMMENT '杩斿巶閫€璐у崟 ID',
  `repair_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '缁翠慨宸ュ崟鍙?WX',
  `repair_by` int(11) NOT NULL COMMENT '缁翠慨浜?ID',
  `old_sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍘熻澶?SN',
  `new_sn` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鏂拌澶?SN',
  `repair_description` text COLLATE utf8mb4_unicode_ci COMMENT '缁翠慨鎻忚堪',
  `materials_used` text COLLATE utf8mb4_unicode_ci COMMENT '缁翠慨鐢ㄦ枡',
  `fault_code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鏁呴殰鐮?,
  `repair_date` date DEFAULT NULL COMMENT '缁翠慨瀹屾垚鏃ユ湡',
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `start_time` datetime DEFAULT NULL COMMENT '缁翠慨寮€濮嬫椂闂?,
  `end_time` datetime DEFAULT NULL COMMENT '缁翠慨缁撴潫鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_rma_repair_repair_no` (`repair_no`),
  KEY `fk_rma_repair_repair_by` (`repair_by`),
  KEY `ix_rma_repair_return_id` (`return_id`),
  CONSTRAINT `fk_rma_repair_repair_by` FOREIGN KEY (`repair_by`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `fk_rma_repair_return_id` FOREIGN KEY (`return_id`) REFERENCES `rma_return` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rma_repair`
--

LOCK TABLES `rma_repair` WRITE;
/*!40000 ALTER TABLE `rma_repair` DISABLE KEYS */;
INSERT INTO `rma_repair` VALUES (1,2,'WX-260907-001',3,'XG200-2509-0022','XG200-2609-0100','鏇存崲4G閫氫俊妯″潡锛岄噸鏂扮剨鎺ュぉ绾挎帴鍙ｏ紝鐑у綍鍥轰欢V2.3.1','4G閫氫俊妯″潡 M-4G x1, 澶╃嚎杩炴帴绾?x1','RF-001','2026-08-29',NULL,'4G妯″潡鎵规闂锛屾洿鎹㈠悗淇″彿姝ｅ父','2026-09-07 09:51:29','2026-09-07 09:51:29','2026-08-29 00:00:00','2026-08-29 00:00:00'),(2,3,'WX-260907-002',3,'XG100-2509-0008','XG100-2609-0100','鏇存崲閾濆悎閲戝澹筹紝閲嶆柊缁勮锛岄槻姘存祴璇曢€氳繃','閾濆悎閲戝澹?XG-100 x1, 瀵嗗皝鑳跺湀 x1','MECH-003','2026-09-03',NULL,'澶栧３鏇存崲瀹屾垚锛屽姛鑳芥甯?,'2026-09-07 09:51:29','2026-09-07 09:51:29','2026-09-03 00:00:00','2026-09-03 00:00:00'),(3,8,'WX20260917001',1,'TEST-SN-092834',NULL,'娴嬭瘯缁翠慨锛氭洿鎹㈢數婧愭ā鍧?,'鐢垫簮妯″潡 x1','PWR001','2026-09-17','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉','绉嶅瓙鏁版嵁','2026-09-17 01:28:43','2026-09-17 01:28:43',NULL,NULL);
/*!40000 ALTER TABLE `rma_repair` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rma_reship`
--

DROP TABLE IF EXISTS `rma_reship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rma_reship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `return_id` int(11) NOT NULL COMMENT '杩斿巶閫€璐у崟 ID',
  `reship_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍐嶅嚭璐у崟鍙?RH',
  `new_sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍑鸿揣 SN',
  `software_version` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '杞欢鐗堟湰鍙?,
  `ship_date` date NOT NULL COMMENT '鍑鸿揣鏃ユ湡',
  `recipient` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鏀惰揣浜?瀹㈡埛',
  `operator_id` int(11) NOT NULL COMMENT '鎿嶄綔浜?ID',
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_rma_reship_reship_no` (`reship_no`),
  KEY `fk_rma_reship_operator_id` (`operator_id`),
  KEY `ix_rma_reship_return_id` (`return_id`),
  CONSTRAINT `fk_rma_reship_operator_id` FOREIGN KEY (`operator_id`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `fk_rma_reship_return_id` FOREIGN KEY (`return_id`) REFERENCES `rma_return` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rma_reship`
--

LOCK TABLES `rma_reship` WRITE;
/*!40000 ALTER TABLE `rma_reship` DISABLE KEYS */;
INSERT INTO `rma_reship` VALUES (1,3,'RH-260907-001','XG100-2609-0100','V3.2.1','2026-09-06','鏉窞娴峰悍濞佽鏁板瓧鎶€鏈湁闄愬叕鍙?,10,NULL,'缁翠慨鍚庨噸鏂板彂鍥炲鎴?,'2026-09-07 09:51:29','2026-09-07 09:51:29');
/*!40000 ALTER TABLE `rma_reship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rma_return`
--

DROP TABLE IF EXISTS `rma_return`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rma_return` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `return_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '杩斿巶鍗曞彿 FC',
  `sku_id` int(11) NOT NULL COMMENT '鐗╂枡 SKU ID',
  `sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '璁惧SN',
  `quantity` int(11) NOT NULL DEFAULT '1' COMMENT '閫€璐ф暟閲?,
  `unit` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '涓? COMMENT '鍗曚綅',
  `customer_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '瀹㈡埛鍚嶇О',
  `return_reason` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '閫€璐у師鍥?,
  `return_date` date NOT NULL COMMENT '閫€璐ф棩鏈?,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDING_DIAGNOSIS' COMMENT '鐘舵€?,
  `assigned_to` int(11) DEFAULT NULL COMMENT '鍒嗛厤浜?ID',
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `spec` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '瑙勬牸',
  `assign_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍒嗛厤绫诲瀷锛歅RODUCTION/TEST',
  `assign_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍒嗛厤鍘熷洜',
  `problem_description` text COLLATE utf8mb4_unicode_ci COMMENT '闂鎻忚堪',
  `repair_plan` text COLLATE utf8mb4_unicode_ci COMMENT '缁翠慨鏂规',
  `inspection_report_no` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '閫佹鍗曠紪鍙?,
  `new_sn` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '缁翠慨鍚庢柊SN',
  `reship_station` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '缁翠慨鍚庡彂鍑哄満绔?,
  `materials_used` text COLLATE utf8mb4_unicode_ci COMMENT '缁翠慨鐢ㄦ枡',
  `repair_time_hours` float DEFAULT NULL COMMENT '淇鑰楁椂锛堝皬鏃讹級',
  `turnaround_days` int(11) DEFAULT NULL COMMENT '鍛ㄨ浆鍛ㄦ湡锛堝ぉ锛?,
  `repair_count` int(11) DEFAULT '1' COMMENT '璇N绱缁翠慨娆℃暟',
  `repair_reason` text COLLATE utf8mb4_unicode_ci COMMENT '缁翠慨鍘熷洜锛堢疮璁★級',
  `diagnosis_result` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '璇婃柇缁撴灉',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_rma_return_return_no` (`return_no`),
  KEY `fk_rma_return_assigned_to` (`assigned_to`),
  KEY `ix_rma_return_sn` (`sn`),
  KEY `ix_rma_return_sku_id` (`sku_id`),
  KEY `ix_rma_return_status` (`status`),
  CONSTRAINT `fk_rma_return_assigned_to` FOREIGN KEY (`assigned_to`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `fk_rma_return_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rma_return`
--

LOCK TABLES `rma_return` WRITE;
/*!40000 ALTER TABLE `rma_return` DISABLE KEYS */;
INSERT INTO `rma_return` VALUES (1,'FC-260907-001',1,'XG200-2509-0015',1,'鍙?,'鍖椾含鏅鸿仈绉戞妧鏈夐檺鍏徃','璁惧鏃犳硶姝ｅ父鍚姩锛岀數婧愭寚绀虹伅涓嶄寒','2026-08-23','PENDING_DIAGNOSIS',NULL,NULL,'瀹㈡埛鎬ヤ慨','2026-09-07 09:51:28','2026-09-07 09:51:28','XG-200',NULL,NULL,'瀹㈡埛鍙嶉璁惧涓婄數鍚庢棤浠讳綍鍙嶅簲锛屾€€鐤戠數婧愭ā鍧楁晠闅?,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL),(2,'FC-260907-002',1,'XG200-2509-0022',1,'鍙?,'骞垮窞浜戝垱鏁版嵁鏈夐檺鍏徃','4G淇″彿棰戠箒鎺夌嚎','2026-08-28','DIAGNOSED',6,NULL,'宸蹭慨澶嶏紝寰呮祴璇曢獙璇?,'2026-09-07 09:51:28','2026-09-07 09:51:28','XG-200','TEST','闇€瑕佹祴璇曞伐绋嬪笀璇婃柇4G妯″潡闂','4G妯″潡闂存瓏鎬ф柇杩烇紝宸叉洿鎹?G閫氫俊妯″潡','鏇存崲4G閫氫俊妯″潡 M-4G锛岄噸鏂扮儳褰曞浐浠?,NULL,NULL,NULL,NULL,2.5,5,1,NULL,'REPAIRABLE'),(3,'FC-260907-003',2,'XG100-2509-0008',1,'鍙?,'鏉窞娴峰悍濞佽鏁板瓧鎶€鏈湁闄愬叕鍙?,'澶栧３鍙樺舰锛岀枒浼艰繍杈撴崯鍧?,'2026-09-02','REPAIRED',3,NULL,'宸插畬鎴愮淮淇紝鍑嗗鍙戝洖','2026-09-07 09:51:29','2026-09-07 09:51:29','XG-100','PRODUCTION','闇€瑕佺敓浜ч儴闂ㄦ洿鎹㈠澹?,'澶栧３鍙充笅瑙掓湁鏄庢樉纾曠鐥曡抗锛屽唴閮≒CB瀹屽ソ','鏇存崲閾濆悎閲戝澹筹紝閲嶆柊缁勮娴嬭瘯','INSP-260907-010','XG100-2609-0100','鏉窞婊ㄦ睙绔?,'閾濆悎閲戝澹?XG-100 x1',1,3,1,'澶栧３鏇存崲','REPAIRABLE'),(4,'FC-260907-004',1,'XG200-2509-0040',1,'鍙?,'娣卞湷鑵捐璁＄畻鏈虹郴缁熸湁闄愬叕鍙?,'璁惧杩涙按锛屼富鏉胯厫铓€涓ラ噸','2026-08-13','DIAGNOSED',6,NULL,'璇婃柇缁撹锛氬缓璁姤搴?,'2026-09-07 09:51:29','2026-09-07 09:51:29','XG-200','TEST','璇勪及鏄惁鍙淮淇?,'璁惧杩涙按瀵艰嚧涓绘澘澶氬鑵愯殌锛孧CU鑺墖鎹熷潖锛岀淮淇垚鏈秴杩囨柊鏈?,NULL,NULL,NULL,NULL,NULL,NULL,NULL,2,'棣栨缁翠慨锛氱數婧愭ā鍧楁洿鎹紱鏈锛氳繘姘翠富鏉胯厫铓€','SCRAP'),(5,'FC20260908001',12,'SN-TEST-001',2,'涓?,'娴嬭瘯瀹㈡埛A','娴嬭瘯閫€璐у師鍥?,'2026-09-01','PENDING_DIAGNOSIS',NULL,NULL,'娴嬭瘯澶囨敞','2026-09-08 05:13:53','2026-09-08 05:13:53','A5-鍙岃',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL),(6,'FC20260908002',11,'SN-TEST-002',1,'濂?,'娴嬭瘯瀹㈡埛B','澶栬鎹熷潖','2026-09-02','PENDING_DIAGNOSIS',NULL,NULL,NULL,'2026-09-08 05:13:54','2026-09-08 05:13:54','350x250x80mm',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL),(7,'FC20260917001',12,'TEST-SN-092657',1,'涓?,'娴嬭瘯瀹㈡埛','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉','2026-09-17','DIAGNOSED',NULL,'鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉','绉嶅瓙鏁版嵁','2026-09-17 01:27:00','2026-09-17 01:27:05',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,'REPAIRABLE'),(8,'FC20260917002',12,'TEST-SN-092834',1,'涓?,'娴嬭瘯瀹㈡埛','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉','2026-09-17','REPAIRED',1,'鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉','绉嶅瓙鏁版嵁','2026-09-17 01:28:36','2026-09-17 01:28:43',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,'REPAIRABLE');
/*!40000 ALTER TABLE `rma_return` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rma_scrap`
--

DROP TABLE IF EXISTS `rma_scrap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rma_scrap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `return_id` int(11) NOT NULL COMMENT '杩斿巶閫€璐у崟 ID',
  `scrap_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎶ュ簾鍗曞彿 BF',
  `requested_by` int(11) NOT NULL COMMENT '鐢宠浜?ID',
  `scrap_reason` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎶ュ簾鍘熷洜',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'PENDING' COMMENT '瀹℃壒鐘舵€?,
  `approved_by` int(11) DEFAULT NULL COMMENT '瀹℃壒浜?ID',
  `approved_at` datetime DEFAULT NULL COMMENT '瀹℃壒鏃堕棿',
  `reject_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '椹冲洖鍘熷洜',
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_rma_scrap_scrap_no` (`scrap_no`),
  KEY `fk_rma_scrap_requested_by` (`requested_by`),
  KEY `fk_rma_scrap_approved_by` (`approved_by`),
  KEY `ix_rma_scrap_return_id` (`return_id`),
  KEY `ix_rma_scrap_status` (`status`),
  CONSTRAINT `fk_rma_scrap_approved_by` FOREIGN KEY (`approved_by`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `fk_rma_scrap_requested_by` FOREIGN KEY (`requested_by`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `fk_rma_scrap_return_id` FOREIGN KEY (`return_id`) REFERENCES `rma_return` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rma_scrap`
--

LOCK TABLES `rma_scrap` WRITE;
/*!40000 ALTER TABLE `rma_scrap` DISABLE KEYS */;
INSERT INTO `rma_scrap` VALUES (1,4,'BF-260907-001',6,'璁惧杩涙按瀵艰嚧涓绘澘涓ラ噸鑵愯殌锛孧CU鑺墖鎹熷潖锛孭CB灞傞棿鐭矾锛岀淮淇垚鏈骏2100瓒呰繃鏂版満鎴愭湰70%锛屽缓璁姤搴熷鐞?,'PENDING',NULL,NULL,NULL,NULL,'寰呯鐞嗗憳瀹℃壒','2026-09-07 09:51:29','2026-09-07 09:51:29');
/*!40000 ALTER TABLE `rma_scrap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rma_warehouse_in`
--

DROP TABLE IF EXISTS `rma_warehouse_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rma_warehouse_in` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `return_id` int(11) NOT NULL COMMENT '杩斿巶閫€璐у崟 ID',
  `new_sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鏂癝N',
  `warehouse_by` int(11) NOT NULL COMMENT '鍏ュ簱瀹℃牳浜?ID',
  `warehouse_date` date NOT NULL COMMENT '鍏ュ簱鏃ユ湡',
  `repair_count` int(11) NOT NULL DEFAULT '1' COMMENT '璇N绱缁翠慨娆℃暟',
  `repair_reason` text COLLATE utf8mb4_unicode_ci COMMENT '缁翠慨鍘熷洜锛堢疮璁★級',
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `warehouse_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ZERO_COST_FINISHED' COMMENT '鍏ュ簱浠撳簱绫诲瀷锛歓ERO_COST_FINISHED/ZERO_COST_SEMI',
  PRIMARY KEY (`id`),
  KEY `fk_rma_warehouse_in_warehouse_by` (`warehouse_by`),
  KEY `ix_rma_warehouse_in_return_id` (`return_id`),
  CONSTRAINT `fk_rma_warehouse_in_return_id` FOREIGN KEY (`return_id`) REFERENCES `rma_return` (`id`),
  CONSTRAINT `fk_rma_warehouse_in_warehouse_by` FOREIGN KEY (`warehouse_by`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rma_warehouse_in`
--

LOCK TABLES `rma_warehouse_in` WRITE;
/*!40000 ALTER TABLE `rma_warehouse_in` DISABLE KEYS */;
INSERT INTO `rma_warehouse_in` VALUES (1,2,'XG200-2609-0100',10,'2026-08-31',1,'4G閫氫俊妯″潡鏇存崲',NULL,'缁翠慨鍚庢柊SN宸插叆搴擄紝鍙噸鏂板嚭璐?,'2026-09-07 09:51:29','2026-09-07 09:51:29','ZERO_COST_FINISHED'),(2,3,'XG100-2609-0100',10,'2026-09-05',1,'澶栧３鏇存崲',NULL,'缁翠慨鍚庢柊SN宸插叆搴?,'2026-09-07 09:51:29','2026-09-07 09:51:29','ZERO_COST_FINISHED');
/*!40000 ALTER TABLE `rma_warehouse_in` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipment`
--

DROP TABLE IF EXISTS `shipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shipment_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍑鸿揣鍗曞彿 SH',
  `sku_id` int(11) NOT NULL COMMENT '鐗╂枡ID',
  `sku_code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鐗╂枡缂栫爜锛圲9缂栫爜锛?,
  `sku_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鐗╂枡鍚嶇О',
  `spec` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '瑙勬牸鍨嬪彿',
  `unit` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '涓? COMMENT '鍗曚綅',
  `sn_list` json NOT NULL COMMENT '鍑鸿揣SN鍒楄〃',
  `quantity` int(11) NOT NULL COMMENT '鏁伴噺',
  `ship_date` date NOT NULL COMMENT '鍙戣揣鏃ユ湡',
  `address` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鏀惰揣鍦板潃',
  `logistics_provider` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鐗╂祦渚涘簲鍟?,
  `tracking_no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '蹇€掑崟鍙?,
  `u9_task_no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'U9浠诲姟鍗曞彿',
  `tf_version` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'TF鍗＄増鏈彿',
  `host_version` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '涓婁綅鏈虹増鏈彿',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_by` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍒涘缓浜?,
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shipment_no` (`shipment_no`),
  KEY `ix_shipment_shipment_no` (`shipment_no`),
  KEY `ix_shipment_sku_id` (`sku_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipment`
--

LOCK TABLES `shipment` WRITE;
/*!40000 ALTER TABLE `shipment` DISABLE KEYS */;
INSERT INTO `shipment` VALUES (1,'SH-260907-001',1,'FG-GW-200','AIoT 鏅鸿兘缃戝叧 XG-200','XG-200','鍙?,'[\"XG200-2609-0031\", \"XG200-2609-0032\", \"XG200-2609-0033\", \"XG200-2609-0034\", \"XG200-2609-0035\"]',5,'2026-09-06','鍖椾含甯傛捣娣€鍖轰腑鍏虫潙杞欢鍥?鏅鸿仈绉戞妧澶у帵 8灞?,'椤轰赴閫熻繍','SF556551512434','U9-TASK-2609-001','V3.2.1','V2.8.0','XG-200 棣栨壒鍑鸿揣鑷冲寳浜櫤鑱?,'10',NULL,'2026-09-07 09:51:29','2026-09-07 09:51:29'),(2,'SH-260907-002',3,'FG-4G-01','4G 閫氫俊妯″潡 M-4G','M-4G-v2','涓?,'[\"M4G-2609-0001\", \"M4G-2609-0002\", \"M4G-2609-0003\", \"M4G-2609-0004\", \"M4G-2609-0005\"]',5,'2026-09-04','骞垮窞甯傚ぉ娌冲尯鐝犳睙鏂板煄 浜戝垱鏁版嵁澶у帵 15灞?,'浜笢鐗╂祦','JD388452550374','U9-TASK-2609-002','V3.2.0','V2.8.0','4G閫氫俊妯″潡澶囦欢鍑鸿揣','10',NULL,'2026-09-07 09:51:29','2026-09-07 09:51:29'),(3,'SH-260907-003',2,'FG-GW-100','AIoT 鏅鸿兘缃戝叧 XG-100','XG-100','鍙?,'[\"XG100-2609-0021\"]',1,'2026-08-31','娣卞湷甯傚崡灞卞尯绉戞妧鍥?鑵捐澶у帵 12灞?,'椤轰赴閫熻繍','SF671422363081','U9-TASK-2609-003','V3.2.0','V2.7.5','XG-100 鐮斿彂娴嬭瘯鏍锋満鍑鸿揣','10',NULL,'2026-09-07 09:51:29','2026-09-07 09:51:29'),(4,'SH-260907-004',1,'FG-GW-200','AIoT 鏅鸿兘缃戝叧 XG-200','XG-200','鍙?,'[\"XG200-2609-0036\", \"XG200-2609-0037\"]',2,'2026-08-29','娣卞湷甯傞緳宀楀尯鍧傜敯鍗庝负鍩哄湴 H鍖?,'寰烽偊蹇€?,'DB503302902944',NULL,NULL,NULL,'XG-200 鏍锋満閫佹祴鍗庝负','10',NULL,'2026-09-07 09:51:29','2026-09-07 09:51:29');
/*!40000 ALTER TABLE `shipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `station` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '鍦虹珯ID',
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鍦虹珯鍚嶇О',
  `customer_id` int(11) NOT NULL COMMENT '鍏宠仈瀹㈡埛',
  `address` text COLLATE utf8mb4_unicode_ci COMMENT '鍦虹珯鍦板潃',
  `contact_person` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鑱旂郴浜?,
  `contact_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鑱旂郴鐢佃瘽',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'ACTIVE/INACTIVE',
  `remark` text COLLATE utf8mb4_unicode_ci COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `customer_id` (`customer_id`),
  KEY `ix_station_status` (`status`),
  CONSTRAINT `station_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stocktake`
--

DROP TABLE IF EXISTS `stocktake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stocktake` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '鐩樼偣ID',
  `stocktake_no` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'PD鍓嶇紑鐩樼偣鍗曞彿',
  `mode` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'CYCLE/FULL',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '杩涜涓?宸插畬鎴?宸插彇娑?,
  `warehouse` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鐩樼偣浠撳簱鑼冨洿',
  `created_by` int(11) NOT NULL COMMENT '鍒涘缓浜?,
  `started_at` datetime NOT NULL COMMENT '寮€濮嬫椂闂?,
  `completed_at` datetime DEFAULT NULL COMMENT '瀹屾垚鏃堕棿',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_stocktake_stocktake_no` (`stocktake_no`),
  KEY `created_by` (`created_by`),
  KEY `ix_stocktake_status` (`status`),
  CONSTRAINT `stocktake_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stocktake`
--

LOCK TABLES `stocktake` WRITE;
/*!40000 ALTER TABLE `stocktake` DISABLE KEYS */;
/*!40000 ALTER TABLE `stocktake` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stocktake_line`
--

DROP TABLE IF EXISTS `stocktake_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stocktake_line` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '鏄庣粏ID',
  `stocktake_id` int(11) NOT NULL COMMENT '鐩樼偣浠诲姟ID',
  `item_sn` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '璁惧SN',
  `sku_id` int(11) NOT NULL COMMENT 'SKU ID',
  `system_qty` int(11) NOT NULL COMMENT '绯荤粺鏁伴噺',
  `actual_qty` int(11) NOT NULL COMMENT '瀹炵洏鏁伴噺',
  `diff_qty` int(11) NOT NULL COMMENT '宸紓鏁伴噺',
  `diff_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '宸紓鍘熷洜',
  `scanned_at` datetime DEFAULT NULL COMMENT '鎵爜鏃堕棿',
  `scanned_by` int(11) DEFAULT NULL COMMENT '鎵爜浜?,
  PRIMARY KEY (`id`),
  KEY `scanned_by` (`scanned_by`),
  KEY `sku_id` (`sku_id`),
  KEY `ix_stocktake_line_item_sn` (`item_sn`),
  KEY `ix_stocktake_line_stocktake_id` (`stocktake_id`),
  CONSTRAINT `stocktake_line_ibfk_1` FOREIGN KEY (`scanned_by`) REFERENCES `sys_user` (`id`),
  CONSTRAINT `stocktake_line_ibfk_2` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`),
  CONSTRAINT `stocktake_line_ibfk_3` FOREIGN KEY (`stocktake_id`) REFERENCES `stocktake` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stocktake_line`
--

LOCK TABLES `stocktake_line` WRITE;
/*!40000 ALTER TABLE `stocktake_line` DISABLE KEYS */;
/*!40000 ALTER TABLE `stocktake_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_audit_log`
--

DROP TABLE IF EXISTS `sys_audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_audit_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `operator_id` int(11) DEFAULT NULL COMMENT '鎿嶄綔浜?ID',
  `operator_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎿嶄綔浜鸿处鍙?鏄电О蹇収',
  `action` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎿嶄綔绫诲瀷',
  `module` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '涓氬姟妯″潡',
  `resource_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '璧勬簮绫诲瀷',
  `resource_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '璧勬簮鏍囪瘑',
  `resource_name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '璧勬簮鍚嶇О/鍗曞彿',
  `summary` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鎿嶄綔鎽樿',
  `before_data` text COLLATE utf8mb4_unicode_ci COMMENT '鍙樻洿鍓嶆暟鎹?JSON',
  `after_data` text COLLATE utf8mb4_unicode_ci COMMENT '鍙樻洿鍚庢暟鎹?JSON',
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '瀹㈡埛绔?IP',
  `created_at` datetime NOT NULL COMMENT '鎿嶄綔鏃堕棿',
  `change_reason` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鍙樻洿鍘熷洜',
  PRIMARY KEY (`id`),
  KEY `ix_sys_audit_log_action` (`action`),
  KEY `ix_sys_audit_log_created_at` (`created_at`),
  KEY `ix_sys_audit_log_module` (`module`),
  KEY `ix_sys_audit_log_operator_id` (`operator_id`),
  KEY `ix_sys_audit_log_resource_id` (`resource_id`),
  CONSTRAINT `sys_audit_log_ibfk_1` FOREIGN KEY (`operator_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=565 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_audit_log`
--

LOCK TABLES `sys_audit_log` WRITE;
/*!40000 ALTER TABLE `sys_audit_log` DISABLE KEYS */;
INSERT INTO `sys_audit_log` VALUES (1,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 11:53:10',NULL),(2,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 11:53:48',NULL),(3,1,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','1','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 11:53:59',NULL),(4,2,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','2','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 11:54:11',NULL),(5,3,'鐢熶骇涓荤锛坧roduction锛?,'LOGIN','auth','user','3','production','鐢熶骇涓荤锛坧roduction锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 11:54:22',NULL),(6,4,'娴嬭瘯宸ョ▼甯堬紙tester锛?,'LOGIN','auth','user','4','tester','娴嬭瘯宸ョ▼甯堬紙tester锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 11:54:33',NULL),(7,5,'鏅€氬憳宸ワ紙staff锛?,'LOGIN','auth','user','5','staff','鏅€氬憳宸ワ紙staff锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 11:54:42',NULL),(8,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 11:54:51',NULL),(9,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 12:07:21',NULL),(10,1,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','1','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 12:07:33',NULL),(11,2,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','2','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 12:07:47',NULL),(12,3,'鐢熶骇涓荤锛坧roduction锛?,'LOGIN','auth','user','3','production','鐢熶骇涓荤锛坧roduction锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 12:07:59',NULL),(13,4,'娴嬭瘯宸ョ▼甯堬紙tester锛?,'LOGIN','auth','user','4','tester','娴嬭瘯宸ョ▼甯堬紙tester锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 12:08:10',NULL),(14,5,'鏅€氬憳宸ワ紙staff锛?,'LOGIN','auth','user','5','staff','鏅€氬憳宸ワ紙staff锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 12:08:19',NULL),(15,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-07 12:08:28',NULL),(16,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:09:27',NULL),(17,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:19:23',NULL),(18,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:19:47',NULL),(19,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:20:10',NULL),(20,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:20:31',NULL),(21,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:20:47',NULL),(22,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:21:13',NULL),(23,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:21:43',NULL),(24,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:22:08',NULL),(25,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:22:21',NULL),(26,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:24:00',NULL),(27,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:25:58',NULL),(28,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:26:17',NULL),(29,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:26:38',NULL),(30,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:27:54',NULL),(31,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:28:20',NULL),(32,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:30:46',NULL),(33,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 12:31:25',NULL),(34,6,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','6','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-07 14:02:24',NULL),(35,8,'璧靛缓椋烇紙zjf锛?,'LOGIN','auth','user','8','zjf','璧靛缓椋烇紙zjf锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-08 09:14:02',NULL),(36,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-08 09:14:31',NULL),(37,1,'绠＄悊鍛橈紙admin锛?,'DELETE','user','user','9','zllq','绠＄悊鍛橈紙admin锛?鍒犻櫎 鍛樺伐璐﹀彿銆寊llq銆?,'{\"username\": \"zllq\", \"nickname\": \"宸︾暀鍚痋", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 9, \"avatar\": null, \"status\": 1, \"role\": \"TEST_ENGINEER\", \"created_at\": \"2026-09-07 09:51:27\", \"updated_at\": \"2026-09-07 09:51:27\"}',NULL,'::1','2026-09-08 09:15:59',NULL),(38,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','::1','2026-09-08 11:07:14',NULL),(39,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 11:11:14',NULL),(40,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 11:11:44',NULL),(41,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 11:12:24',NULL),(42,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-08 11:24:48',NULL),(43,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-08 11:29:08',NULL),(44,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 13:06:02',NULL),(45,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-08 13:11:23',NULL),(46,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-08 13:12:28',NULL),(47,1,'绠＄悊鍛橈紙admin锛?,'CREATE','rma','rma_return','FC20260908001','杩斿巶鍗?FC20260908001','Excel瀵煎叆杩斿巶閫€璐у崟锛孲N=SN-TEST-001锛屽師鍥?娴嬭瘯閫€璐у師鍥?,NULL,NULL,'import','2026-09-08 13:13:54',NULL),(48,1,'绠＄悊鍛橈紙admin锛?,'CREATE','rma','rma_return','FC20260908002','杩斿巶鍗?FC20260908002','Excel瀵煎叆杩斿巶閫€璐у崟锛孲N=SN-TEST-002锛屽師鍥?澶栬鎹熷潖',NULL,NULL,'import','2026-09-08 13:13:54',NULL),(49,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-08 13:24:39',NULL),(50,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-08 16:58:09',NULL),(51,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-08 17:06:23',NULL),(52,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-08 17:12:32',NULL),(53,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 17:16:36',NULL),(54,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-08 17:16:45',NULL),(55,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 17:23:35',NULL),(56,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 17:25:03',NULL),(57,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 17:26:17',NULL),(58,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.77','2026-09-08 17:27:22',NULL),(59,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 17:27:36',NULL),(60,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-08 17:28:28',NULL),(61,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'testclient','2026-09-09 10:11:50',NULL),(62,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.77','2026-09-09 12:11:31',NULL),(63,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 12:20:46',NULL),(64,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:46:38',NULL),(65,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:46:38',NULL),(66,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:47:44',NULL),(67,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:48:18',NULL),(68,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:48:28',NULL),(69,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:49:21',NULL),(70,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:49:22',NULL),(71,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:49:49',NULL),(72,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:50:12',NULL),(73,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:50:22',NULL),(74,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-09 17:51:19',NULL),(75,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:02:25',NULL),(76,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:02:45',NULL),(77,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:03:05',NULL),(78,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:03:56',NULL),(79,1,'绠＄悊鍛橈紙admin锛?,'CREATE','user','user','13','warehouse','绠＄悊鍛橈紙admin锛?鏂板 鍛樺伐璐﹀彿銆寃arehouse銆?,NULL,'{\"username\": \"warehouse\", \"nickname\": \"浠撳簱绠＄悊鍛榎", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 13, \"avatar\": null, \"status\": 1, \"role\": \"WAREHOUSE\", \"created_at\": \"2026-09-10 01:03:57\", \"updated_at\": \"2026-09-10 01:03:57\"}','127.0.0.1','2026-09-10 09:03:58',NULL),(80,1,'绠＄悊鍛橈紙admin锛?,'CREATE','user','user','14','quality','绠＄悊鍛橈紙admin锛?鏂板 鍛樺伐璐﹀彿銆宷uality銆?,NULL,'{\"username\": \"quality\", \"nickname\": \"璐ㄦ鍛榎", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 14, \"avatar\": null, \"status\": 1, \"role\": \"QUALITY\", \"created_at\": \"2026-09-10 01:04:00\", \"updated_at\": \"2026-09-10 01:04:00\"}','127.0.0.1','2026-09-10 09:04:00',NULL),(81,1,'绠＄悊鍛橈紙admin锛?,'CREATE','user','user','15','production','绠＄悊鍛橈紙admin锛?鏂板 鍛樺伐璐﹀彿銆宲roduction銆?,NULL,'{\"username\": \"production\", \"nickname\": \"鐢熶骇绠＄悊鍛榎", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 15, \"avatar\": null, \"status\": 1, \"role\": \"PRODUCTION\", \"created_at\": \"2026-09-10 01:04:02\", \"updated_at\": \"2026-09-10 01:04:02\"}','127.0.0.1','2026-09-10 09:04:02',NULL),(82,1,'绠＄悊鍛橈紙admin锛?,'CREATE','user','user','16','tester','绠＄悊鍛橈紙admin锛?鏂板 鍛樺伐璐﹀彿銆宼ester銆?,NULL,'{\"username\": \"tester\", \"nickname\": \"娴嬭瘯鍛榎", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 16, \"avatar\": null, \"status\": 1, \"role\": \"TEST_ENGINEER\", \"created_at\": \"2026-09-10 01:04:04\", \"updated_at\": \"2026-09-10 01:04:04\"}','127.0.0.1','2026-09-10 09:04:05',NULL),(83,1,'绠＄悊鍛橈紙admin锛?,'CREATE','user','user','17','staff','绠＄悊鍛橈紙admin锛?鏂板 鍛樺伐璐﹀彿銆宻taff銆?,NULL,'{\"username\": \"staff\", \"nickname\": \"鏅€氬憳宸", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 17, \"avatar\": null, \"status\": 1, \"role\": \"STAFF\", \"created_at\": \"2026-09-10 01:04:06\", \"updated_at\": \"2026-09-10 01:04:06\"}','127.0.0.1','2026-09-10 09:04:07',NULL),(84,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:05:53',NULL),(85,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:06:24',NULL),(86,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:06:46',NULL),(87,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:07:06',NULL),(88,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:08:14',NULL),(89,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:09:24',NULL),(90,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:09:25',NULL),(91,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:10:40',NULL),(92,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:10:54',NULL),(98,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 09:12:03',NULL),(99,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.77','2026-09-10 12:13:11',NULL),(100,1,'绠＄悊鍛橈紙admin锛?,'TOGGLE','user','user','14','quality','绠＄悊鍛橈紙admin锛?鍒囨崲鐘舵€?鍛樺伐璐﹀彿銆宷uality銆嶏細鐘舵€?1 鈫?0','{\"status\": 1}','{\"status\": 0}','192.168.10.77','2026-09-10 12:15:42',NULL),(101,1,'绠＄悊鍛橈紙admin锛?,'TOGGLE','user','user','14','quality','绠＄悊鍛橈紙admin锛?鍒囨崲鐘舵€?鍛樺伐璐﹀彿銆宷uality銆嶏細鐘舵€?0 鈫?1','{\"status\": 0}','{\"status\": 1}','192.168.10.77','2026-09-10 12:15:44',NULL),(102,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 17:37:42',NULL),(103,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 17:37:45',NULL),(104,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 17:37:48',NULL),(105,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 17:41:56',NULL),(106,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 17:41:58',NULL),(107,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-10 17:42:01',NULL),(108,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-11 17:15:11',NULL),(109,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-11 17:15:15',NULL),(110,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-11 17:15:19',NULL),(111,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-11 17:31:42',NULL),(112,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-11 17:31:44',NULL),(113,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-11 17:31:48',NULL),(114,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.77','2026-09-11 17:37:58',NULL),(115,1,'绠＄悊鍛橈紙admin锛?,'SUBMIT','outbound','outbound_order','5','JOUT-20260908-0001','绠＄悊鍛橈紙admin锛?鎻愪氦瀹℃牳 鍑哄簱鍗曘€孞OUT-20260908-0001銆嶏細鐘舵€?INITIATED 鈫?INITIATED','{\"operation_status\": \"INITIATED\"}','{\"operation_status\": \"INITIATED\"}','192.168.10.77','2026-09-11 17:38:16',NULL),(116,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-11 17:38:43',NULL),(117,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-11 17:38:46',NULL),(118,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-11 17:38:49',NULL),(119,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 12:49:44',NULL),(120,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 12:50:20',NULL),(121,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 12:51:17',NULL),(122,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 12:51:42',NULL),(123,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 12:52:18',NULL),(124,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 12:52:47',NULL),(125,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 12:57:05',NULL),(126,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:10:03',NULL),(127,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:20:32',NULL),(128,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:40:51',NULL),(129,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:41:16',NULL),(130,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.77','2026-09-14 13:44:52',NULL),(131,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:45:35',NULL),(132,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:45:53',NULL),(133,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:46:07',NULL),(134,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:46:23',NULL),(135,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:46:26',NULL),(136,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:46:29',NULL),(137,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:51:09',NULL),(138,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:51:27',NULL),(139,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:56:11',NULL),(140,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:56:13',NULL),(141,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 13:56:17',NULL),(142,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 14:00:01',NULL),(143,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 14:17:36',NULL),(144,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 14:17:39',NULL),(145,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 14:17:42',NULL),(146,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 14:36:49',NULL),(147,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 14:36:52',NULL),(148,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 14:36:57',NULL),(149,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:36:45',NULL),(150,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:37:18',NULL),(151,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:38:29',NULL),(152,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:40:07',NULL),(153,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:40:11',NULL),(154,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:40:15',NULL),(155,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:45:23',NULL),(156,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:45:26',NULL),(157,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:45:29',NULL),(158,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:46:12',NULL),(159,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:46:15',NULL),(160,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:46:18',NULL),(161,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:47:22',NULL),(162,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:47:25',NULL),(163,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 16:47:29',NULL),(164,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 17:36:46',NULL),(165,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 17:36:51',NULL),(166,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 17:39:25',NULL),(167,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 17:39:36',NULL),(168,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 17:39:44',NULL),(169,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 17:54:12',NULL),(170,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:00:56',NULL),(171,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:02:38',NULL),(172,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:06:41',NULL),(173,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:07:00',NULL),(174,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:32:36',NULL),(175,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:33:13',NULL),(176,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:36:18',NULL),(177,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:37:18',NULL),(178,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:38:36',NULL),(179,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-14 18:39:05',NULL),(180,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-15 12:25:48',NULL),(181,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-15 12:25:59',NULL),(182,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-15 12:26:15',NULL),(183,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-15 12:28:37',NULL),(184,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-15 12:29:19',NULL),(185,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-15 12:52:29',NULL),(186,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-15 12:53:17',NULL),(187,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-15 12:55:05',NULL),(188,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-15 13:25:26',NULL),(189,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-15 17:34:58',NULL),(190,1,'绠＄悊鍛橈紙admin锛?,'UPDATE','production','production_task','TASK-2609-003','鐢熶骇浠诲姟 TASK-2609-003','鏇存柊鐢熶骇浠诲姟锛屼慨鏀瑰瓧娈?[\'plan_quantity\', \'status\', \'start_date\', \'end_date\']',NULL,NULL,'192.168.10.3','2026-09-15 17:48:51',''),(191,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-15 17:56:56',NULL),(192,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-15 17:59:32',NULL),(193,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-15 18:10:35',NULL),(194,4,'涔旀．锛坬s锛?,'LOGIN','auth','user','4','qs','涔旀．锛坬s锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.77','2026-09-15 18:26:32',NULL),(195,4,'涔旀．锛坬s锛?,'LOGIN','auth','user','4','qs','涔旀．锛坬s锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.32','2026-09-16 08:56:27',NULL),(196,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.77','2026-09-16 09:01:07',NULL),(197,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.32','2026-09-16 09:21:20',NULL),(198,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 09:23:24',NULL),(199,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.32','2026-09-16 09:32:53',NULL),(200,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 09:35:51',NULL),(201,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 09:37:17',NULL),(202,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 09:37:21',NULL),(203,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 09:37:28',NULL),(204,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-16 10:07:27',NULL),(205,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-16 10:38:54',NULL),(206,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-16 11:05:14',NULL),(207,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-16 11:25:43',NULL),(208,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-16 14:04:52',NULL),(209,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:05:31',NULL),(210,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:05:34',NULL),(211,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:05:38',NULL),(212,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'192.168.10.3','2026-09-16 14:09:12',NULL),(213,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:12:08',NULL),(214,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:12:10',NULL),(215,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:12:14',NULL),(216,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:25:49',NULL),(217,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:30:00',NULL),(218,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:32:28',NULL),(219,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:33:01',NULL),(220,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:35:55',NULL),(221,1,'绠＄悊鍛橈紙admin锛?,'CREATE','user','user','13','warehouse','绠＄悊鍛橈紙admin锛?鏂板 鍛樺伐璐﹀彿銆寃arehouse銆?,NULL,'{\"username\": \"warehouse\", \"nickname\": \"浠撳簱绠＄悊鍛榎", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 13, \"avatar\": null, \"status\": 1, \"role\": \"WAREHOUSE\", \"created_at\": \"2026-09-16 06:35:57\", \"updated_at\": \"2026-09-16 06:35:57\"}','127.0.0.1','2026-09-16 14:35:57',NULL),(222,1,'绠＄悊鍛橈紙admin锛?,'CREATE','user','user','14','quality','绠＄悊鍛橈紙admin锛?鏂板 鍛樺伐璐﹀彿銆宷uality銆?,NULL,'{\"username\": \"quality\", \"nickname\": \"璐ㄩ噺璐熻矗浜篭", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 14, \"avatar\": null, \"status\": 1, \"role\": \"QUALITY\", \"created_at\": \"2026-09-16 06:35:59\", \"updated_at\": \"2026-09-16 06:35:59\"}','127.0.0.1','2026-09-16 14:36:00',NULL),(223,1,'绠＄悊鍛橈紙admin锛?,'CREATE','user','user','15','production','绠＄悊鍛橈紙admin锛?鏂板 鍛樺伐璐﹀彿銆宲roduction銆?,NULL,'{\"username\": \"production\", \"nickname\": \"鐢熶骇璐熻矗浜篭", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 15, \"avatar\": null, \"status\": 1, \"role\": \"PRODUCTION\", \"created_at\": \"2026-09-16 06:36:01\", \"updated_at\": \"2026-09-16 06:36:01\"}','127.0.0.1','2026-09-16 14:36:02',NULL),(224,1,'绠＄悊鍛橈紙admin锛?,'CREATE','user','user','16','test_eng','绠＄悊鍛橈紙admin锛?鏂板 鍛樺伐璐﹀彿銆宼est_eng銆?,NULL,'{\"username\": \"test_eng\", \"nickname\": \"娴嬭瘯宸ョ▼甯圽", \"email\": null, \"phone\": null, \"remark\": null, \"id\": 16, \"avatar\": null, \"status\": 1, \"role\": \"TEST_ENGINEER\", \"created_at\": \"2026-09-16 06:36:04\", \"updated_at\": \"2026-09-16 06:36:04\"}','127.0.0.1','2026-09-16 14:36:04',NULL),(225,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:41:14',NULL),(226,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:41:40',NULL),(227,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:42:26',NULL),(228,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:43:24',NULL),(229,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:44:50',NULL),(230,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:44:51',NULL),(231,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:44:53',NULL),(232,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:45:10',NULL),(233,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:46:11',NULL),(234,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:47:11',NULL),(235,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:48:11',NULL),(236,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:49:10',NULL),(237,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:52:57',NULL),(238,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:53:00',NULL),(239,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:53:03',NULL),(240,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:57:54',NULL),(241,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:58:04',NULL),(242,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:58:10',NULL),(243,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:58:18',NULL),(244,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:58:26',NULL),(245,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:58:35',NULL),(246,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:58:44',NULL),(247,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:58:52',NULL),(248,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:59:01',NULL),(249,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:59:09',NULL),(250,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:59:17',NULL),(251,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:59:26',NULL),(252,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:59:34',NULL),(253,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:59:42',NULL),(254,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:59:51',NULL),(255,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 14:59:58',NULL),(256,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:00:06',NULL),(257,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:00:15',NULL),(258,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:00:23',NULL),(259,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:00:31',NULL),(260,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:00:40',NULL),(261,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:00:48',NULL),(262,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:01:09',NULL),(263,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:02:15',NULL),(264,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:03:19',NULL),(265,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:04:20',NULL),(266,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:05:20',NULL),(267,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:11:03',NULL),(268,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:16:37',NULL),(269,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:16:47',NULL),(270,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:16:54',NULL),(271,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:17:02',NULL),(272,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:17:12',NULL),(273,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:17:22',NULL),(274,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:17:32',NULL),(275,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:17:41',NULL),(276,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:17:52',NULL),(277,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:17:59',NULL),(278,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:18:08',NULL),(279,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:18:18',NULL),(280,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:18:26',NULL),(281,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:18:36',NULL),(282,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:18:44',NULL),(283,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:18:52',NULL),(284,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:19:01',NULL),(285,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:19:11',NULL),(286,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:19:19',NULL),(287,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:19:28',NULL),(288,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:19:36',NULL),(289,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:19:44',NULL),(290,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:27:29',NULL),(291,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:38:49',NULL),(292,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-16 15:39:31',NULL),(293,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:40:26',NULL),(294,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:46:56',NULL),(295,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:47:30',NULL),(296,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:47:56',NULL),(297,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:51:47',NULL),(298,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:53:40',NULL),(299,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:53:42',NULL),(300,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:54:14',NULL),(301,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:55:47',NULL),(302,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-16 15:55:47',NULL),(303,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 15:57:34',NULL),(304,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-16 15:57:35',NULL),(305,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:30',NULL),(306,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:30',NULL),(307,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:33',NULL),(308,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:33',NULL),(309,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:44',NULL),(310,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:45',NULL),(311,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:50',NULL),(312,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:50',NULL),(313,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:56',NULL),(314,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:27:56',NULL),(315,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:28:07',NULL),(316,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:28:07',NULL),(317,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:28:19',NULL),(318,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:28:26',NULL),(319,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:28:33',NULL),(320,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:28:40',NULL),(321,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:28:47',NULL),(322,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:28:54',NULL),(323,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:29:04',NULL),(324,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:29:10',NULL),(325,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:29:17',NULL),(326,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:29:24',NULL),(327,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:29:30',NULL),(328,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:29:37',NULL),(329,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:29:45',NULL),(330,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:29:52',NULL),(331,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:29:59',NULL),(332,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:30:05',NULL),(333,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 16:30:12',NULL),(334,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:31:17',NULL),(335,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:31:20',NULL),(336,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:31:27',NULL),(337,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:31:35',NULL),(338,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:31:44',NULL),(339,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:31:51',NULL),(340,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:32:01',NULL),(341,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:32:08',NULL),(342,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:32:20',NULL),(343,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:32:52',NULL),(344,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:33:02',NULL),(345,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:33:11',NULL),(346,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:33:46',NULL),(347,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:34:00',NULL),(348,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:34:13',NULL),(349,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:34:29',NULL),(350,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:34:50',NULL),(351,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:34:58',NULL),(352,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:35:13',NULL),(353,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:35:20',NULL),(354,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:35:27',NULL),(355,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:36:00',NULL),(356,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:36:18',NULL),(357,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:43:30',NULL),(358,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:43:38',NULL),(359,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:43:43',NULL),(360,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:43:50',NULL),(361,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:43:57',NULL),(362,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:45:16',NULL),(363,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:45:34',NULL),(364,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:45:37',NULL),(365,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:45:52',NULL),(366,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:46:04',NULL),(367,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:46:12',NULL),(368,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:46:34',NULL),(369,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:47:00',NULL),(370,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:47:07',NULL),(371,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:47:14',NULL),(372,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:47:21',NULL),(373,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:47:27',NULL),(374,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:47:34',NULL),(375,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:50:07',NULL),(376,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:50:16',NULL),(377,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:50:21',NULL),(378,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:50:27',NULL),(379,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:50:34',NULL),(380,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:50:42',NULL),(381,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:50:49',NULL),(382,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:50:56',NULL),(383,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:51:03',NULL),(384,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:51:09',NULL),(385,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:51:16',NULL),(386,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:51:24',NULL),(387,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:51:30',NULL),(388,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:51:37',NULL),(389,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:51:44',NULL),(390,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:51:51',NULL),(391,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:51:57',NULL),(392,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:52:06',NULL),(393,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:52:13',NULL),(394,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:52:20',NULL),(395,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:52:27',NULL),(396,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 17:52:34',NULL),(397,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:03:10',NULL),(398,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:12:08',NULL),(399,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:12:16',NULL),(400,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:12:21',NULL),(401,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:12:27',NULL),(402,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:12:34',NULL),(403,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:12:41',NULL),(404,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:12:47',NULL),(405,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:12:54',NULL),(406,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:13:01',NULL),(407,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:13:07',NULL),(408,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:13:14',NULL),(409,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:13:20',NULL),(410,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:13:27',NULL),(411,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:13:34',NULL),(412,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:13:40',NULL),(413,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:13:47',NULL),(414,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:13:54',NULL),(415,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:14:02',NULL),(416,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:14:09',NULL),(417,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:14:15',NULL),(418,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:14:22',NULL),(419,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-16 18:14:28',NULL),(420,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:37:17',NULL),(421,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:37:48',NULL),(422,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:38:14',NULL),(423,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:38:40',NULL),(424,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:39:10',NULL),(425,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:39:38',NULL),(426,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:45:15',NULL),(427,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:45:42',NULL),(428,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:46:08',NULL),(429,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:46:35',NULL),(430,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:47:06',NULL),(431,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:47:35',NULL),(432,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:49:31',NULL),(433,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:52:01',NULL),(434,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:55:21',NULL),(435,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:55:29',NULL),(436,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:55:35',NULL),(437,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:55:42',NULL),(438,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:55:47',NULL),(439,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:55:50',NULL),(440,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:55:57',NULL),(441,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:56:05',NULL),(442,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:56:13',NULL),(443,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:56:21',NULL),(444,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:56:28',NULL),(445,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:56:36',NULL),(446,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:56:44',NULL),(447,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:56:52',NULL),(448,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:56:59',NULL),(449,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:57:07',NULL),(450,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:57:14',NULL),(451,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:57:22',NULL),(452,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:57:31',NULL),(453,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:57:40',NULL),(454,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:57:48',NULL),(455,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:57:54',NULL),(456,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:57:56',NULL),(457,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 08:58:03',NULL),(458,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:01:32',NULL),(459,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:01:39',NULL),(460,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:01:44',NULL),(461,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:01:51',NULL),(462,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:01:57',NULL),(463,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:02:04',NULL),(464,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:02:10',NULL),(465,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:02:17',NULL),(466,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:02:23',NULL),(467,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:02:31',NULL),(468,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:03:04',NULL),(469,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:03:11',NULL),(470,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:03:17',NULL),(471,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:03:24',NULL),(472,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:03:30',NULL),(473,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:03:37',NULL),(474,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:03:43',NULL),(475,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:03:51',NULL),(476,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:03:57',NULL),(477,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:04:04',NULL),(478,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:04:11',NULL),(479,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:04:18',NULL),(480,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:07:12',NULL),(481,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:08:18',NULL),(482,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:08:45',NULL),(483,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:08:59',NULL),(484,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:11:53',NULL),(485,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-17 09:12:23',NULL),(486,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:15:29',NULL),(487,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:16:10',NULL),(488,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-17 09:16:51',NULL),(489,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:18:58',NULL),(490,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-17 09:19:42',NULL),(491,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:22:38',NULL),(492,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-17 09:23:32',NULL),(493,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:26:46',NULL),(494,1,'绠＄悊鍛橈紙admin锛?,'CREATE','incoming','incoming_inspection','JC20260917001','妫€楠屾姤鍛?JC20260917001','绠＄悊鍛?瀵瑰埌璐у崟 RC-TEST-001 鍒涘缓妫€楠屾姤鍛婏紝缁撴灉=ACCEPTED',NULL,NULL,'127.0.0.1','2026-09-17 09:26:52','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉'),(495,1,'绠＄悊鍛橈紙admin锛?,'CREATE','rma','rma_return','FC20260917001','杩斿巶鍗?FC20260917001','鍒涘缓杩斿巶閫€璐у崟锛孲N=TEST-SN-092657锛屽師鍥?鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉',NULL,NULL,'127.0.0.1','2026-09-17 09:27:00',NULL),(496,1,'绠＄悊鍛橈紙admin锛?,'CREATE','rma','rma_diagnosis','DG20260917001','璇婃柇鎶ュ憡 DG20260917001','璇婃柇杩斿巶鍗?FC20260917001锛岀粨鏋?REPAIRABLE',NULL,NULL,'127.0.0.1','2026-09-17 09:27:06','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉'),(497,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:28:24',NULL),(498,1,'绠＄悊鍛橈紙admin锛?,'CREATE','incoming','incoming_inspection','JC20260917002','妫€楠屾姤鍛?JC20260917002','绠＄悊鍛?瀵瑰埌璐у崟 RC-TEST-001 鍒涘缓妫€楠屾姤鍛婏紝缁撴灉=ACCEPTED',NULL,NULL,'127.0.0.1','2026-09-17 09:28:30','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉'),(499,1,'绠＄悊鍛橈紙admin锛?,'CREATE','rma','rma_return','FC20260917002','杩斿巶鍗?FC20260917002','鍒涘缓杩斿巶閫€璐у崟锛孲N=TEST-SN-092834锛屽師鍥?鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉',NULL,NULL,'127.0.0.1','2026-09-17 09:28:37',NULL),(500,1,'绠＄悊鍛橈紙admin锛?,'CREATE','rma','rma_diagnosis','DG20260917002','璇婃柇鎶ュ憡 DG20260917002','璇婃柇杩斿巶鍗?FC20260917002锛岀粨鏋?REPAIRABLE',NULL,NULL,'127.0.0.1','2026-09-17 09:28:39','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉'),(501,1,'绠＄悊鍛橈紙admin锛?,'ASSIGN','rma','rma_return','FC20260917002','杩斿巶鍗?FC20260917002','鍒嗛厤杩斿巶鍗曠粰鐢ㄦ埛 1',NULL,NULL,'127.0.0.1','2026-09-17 09:28:42','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉'),(502,1,'绠＄悊鍛橈紙admin锛?,'CREATE','rma','rma_repair','WX20260917001','缁翠慨宸ュ崟 WX20260917001','缁翠慨杩斿巶鍗?FC20260917002锛屾棫SN=TEST-SN-092834锛屾柊SN=鏃?,NULL,NULL,'127.0.0.1','2026-09-17 09:28:44','鑷姩鍖栨祴璇?鎵撳嵃楠岃瘉'),(503,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:32:57',NULL),(504,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-17 09:33:45',NULL),(505,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 09:37:25',NULL),(506,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 11:04:08',NULL),(507,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 11:04:44',NULL),(508,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 11:05:30',NULL),(509,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-17 11:06:34',NULL),(510,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:17:11',NULL),(511,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:17:35',NULL),(512,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:17:42',NULL),(513,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:17:51',NULL),(514,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:17:57',NULL),(515,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:18:03',NULL),(516,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:18:11',NULL),(517,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:18:19',NULL),(518,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:18:27',NULL),(519,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:18:34',NULL),(520,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:18:42',NULL),(521,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:18:50',NULL),(522,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:18:57',NULL),(523,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:19:05',NULL),(524,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:19:12',NULL),(525,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:19:20',NULL),(526,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:19:28',NULL),(527,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:19:35',NULL),(528,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:19:42',NULL),(529,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:19:51',NULL),(530,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:19:59',NULL),(531,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:20:07',NULL),(532,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:20:14',NULL),(533,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:20:22',NULL),(534,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:24:30',NULL),(535,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:27:43',NULL),(536,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:29:47',NULL),(537,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-17 12:30:26',NULL),(538,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:32:37',NULL),(539,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-17 12:33:00',NULL),(540,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:37:50',NULL),(541,1,'绠＄悊鍛橈紙admin锛?,'EXPORT','inventory','inventory_export',NULL,NULL,'绠＄悊鍛橈紙admin锛?瀵煎嚭 搴撳瓨鏄庣粏 Excel',NULL,'{\"filters\": {\"item_sn\": null, \"sku_id\": null, \"stock_status\": null, \"stock_condition\": null, \"operation_status\": null, \"last_order_no\": null, \"category_id\": null, \"keyword\": null}}','127.0.0.1','2026-09-17 12:38:15',NULL),(542,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:42:23',NULL),(543,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:42:33',NULL),(544,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:42:39',NULL),(545,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:42:45',NULL),(546,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:42:54',NULL),(547,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:43:01',NULL),(548,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:43:09',NULL),(549,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:43:17',NULL),(550,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:43:25',NULL),(551,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:43:34',NULL),(552,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:43:41',NULL),(553,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:43:49',NULL),(554,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:43:57',NULL),(555,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:44:04',NULL),(556,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:44:12',NULL),(557,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:44:19',NULL),(558,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:44:27',NULL),(559,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:44:36',NULL),(560,13,'浠撳簱绠＄悊鍛橈紙warehouse锛?,'LOGIN','auth','user','13','warehouse','浠撳簱绠＄悊鍛橈紙warehouse锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:44:43',NULL),(561,14,'璐ㄩ噺璐熻矗浜猴紙quality锛?,'LOGIN','auth','user','14','quality','璐ㄩ噺璐熻矗浜猴紙quality锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:44:51',NULL),(562,16,'娴嬭瘯宸ョ▼甯堬紙test_eng锛?,'LOGIN','auth','user','16','test_eng','娴嬭瘯宸ョ▼甯堬紙test_eng锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:44:59',NULL),(563,15,'鐢熶骇璐熻矗浜猴紙production锛?,'LOGIN','auth','user','15','production','鐢熶骇璐熻矗浜猴紙production锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:45:06',NULL),(564,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-17 12:46:38',NULL);
/*!40000 ALTER TABLE `sys_audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_config`
--

DROP TABLE IF EXISTS `sys_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '涓婚敭',
  `key` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '閰嶇疆閿?,
  `value` text COLLATE utf8mb4_unicode_ci COMMENT '閰嶇疆鍊?,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `ix_sys_config_key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_config`
--

LOCK TABLES `sys_config` WRITE;
/*!40000 ALTER TABLE `sys_config` DISABLE KEYS */;
INSERT INTO `sys_config` VALUES (1,'app_name','IMS','2026-09-07 03:51:34','2026-09-07 03:51:34'),(2,'app_subtitle','涓€鐗╀竴鐮佸簱瀛樼鐞嗙郴缁?,'2026-09-07 03:51:34','2026-09-07 03:51:34');
/*!40000 ALTER TABLE `sys_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_sequence`
--

DROP TABLE IF EXISTS `sys_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_sequence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `seq_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '搴忓垪绫诲瀷锛欽IN / JOUT',
  `seq_date` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鏃ユ湡 YYYYMMDD',
  `current_value` int(11) NOT NULL COMMENT '褰撳墠搴忓彿',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_seq_type_date` (`seq_type`,`seq_date`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_sequence`
--

LOCK TABLES `sys_sequence` WRITE;
/*!40000 ALTER TABLE `sys_sequence` DISABLE KEYS */;
INSERT INTO `sys_sequence` VALUES (1,'FC','20260908',2,'2026-09-08 05:13:53','2026-09-08 05:13:54'),(2,'JIN','20260908',1,'2026-09-08 05:16:30','2026-09-08 05:16:30'),(3,'JOUT','20260908',1,'2026-09-08 05:16:49','2026-09-08 05:16:49'),(4,'JC','20260917',2,'2026-09-17 01:26:51','2026-09-17 01:28:29'),(5,'FC','20260917',2,'2026-09-17 01:27:00','2026-09-17 01:28:36'),(6,'DG','20260917',2,'2026-09-17 01:27:05','2026-09-17 01:28:39'),(7,'WX','20260917',1,'2026-09-17 01:28:43','2026-09-17 01:28:43');
/*!40000 ALTER TABLE `sys_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sys_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '涓婚敭',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '鐧诲綍璐﹀彿',
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'bcrypt 瀵嗙爜鍝堝笇',
  `nickname` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鏄剧ず鏄电О',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '閭',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '鎵嬫満鍙?,
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '澶村儚 URL',
  `status` smallint(6) NOT NULL COMMENT '鐘舵€侊細1=姝ｅ父锛?=绂佺敤',
  `remark` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '澶囨敞',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鍒涘缓鏃堕棿',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '鏇存柊鏃堕棿',
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'STAFF' COMMENT '瑙掕壊锛欰DMIN/STAFF',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sys_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES (1,'admin','$2b$12$J2IvbL9q.dLDNB76OC8Zrumbag7BefY7Aw.K0zWTV.CiwekjZAP4y','绠＄悊鍛?,NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-08 05:05:46','ADMIN'),(2,'zwf','$2b$12$P9HWFKMLdrTtBq07.omx7ubKxR9XqSmnOZAzEw76YJRvs3zE.l5/m','宸︽枃宄?,NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-07 09:51:27','ADMIN'),(3,'yd','$2b$12$fnNhB1orAsncJCYQBFJ5suWVAKvqBL5vKKEvGhnMv8PwYzKpSgDqi','棰滃啲',NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-07 09:51:27','PRODUCTION'),(4,'qs','$2b$12$JpTqiPQ6aTrBCfI/vM3Uc..4jWiXcpeSBi0J3Ug6Qy.goweukpl0q','涔旀．',NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-07 09:51:27','PRODUCTION'),(5,'lfq','$2b$12$ZoDSIOYk26cUnNvHXX91iOV0OtljqqcrNpfHmrHNiQkOOsTMcBEwy','鍚曡姵寮?,NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-07 09:51:27','QUALITY'),(6,'lxj','$2b$12$RzGSR7Zc/rtCKj5MRUAVles8mEbsLH2gya0CZI8rhV0z/JczcLr4W','鍒樻檽濞?,NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-07 09:51:27','TEST_ENGINEER'),(7,'hb','$2b$12$KJRpIXb0ZBSBzBUuvDcpzed/iG2G.4Rj.K7KCDlAoB2n1NfZ2oSIO','浣曞',NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-07 09:51:27','TEST_ENGINEER'),(8,'zjf','$2b$12$Ndfj9RnyMcIrpB6lvC0/aeEehIL32xu9Ebi/zYGR37gnzUWA/jAEO','璧靛缓椋?,NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-07 09:51:27','TEST_ENGINEER'),(10,'zd','$2b$12$W3DnbhZpZYvyCvli8z8oq.GNue0AozqI1lndeCy/wbNevK6JCt.hC','璧典腹',NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-07 09:51:27','WAREHOUSE'),(11,'qz','$2b$12$oTERBt5KAw/70cTMVl23CuXBzrUMJ5zZsqYtKOvu5xgc9ZxCcBUza','缇や紬',NULL,NULL,NULL,1,NULL,'2026-09-07 09:51:27','2026-09-07 09:51:27','STAFF'),(12,'zlq','$2b$12$Kp/9JRInATCOfHXlMjp3kOkmUdOKnavlYloVl8ea5meEvwWYW//YS','宸︾暀鍚?,NULL,NULL,NULL,1,NULL,'2026-09-08 01:09:03','2026-09-08 01:09:03','TEST_ENGINEER'),(13,'warehouse','$2b$12$wqZPvwj87cBAgWBVvKxO0eGaYwku7RBMavB/NQZa2bmF5fexf8mAi','浠撳簱绠＄悊鍛?,NULL,NULL,NULL,1,NULL,'2026-09-16 06:35:57','2026-09-16 06:35:57','WAREHOUSE'),(14,'quality','$2b$12$RIpy2SNODVorHDxhjduhN.5hv3gdJRyGN2tJ0ov0rmZzM43ideGhm','璐ㄩ噺璐熻矗浜?,NULL,NULL,NULL,1,NULL,'2026-09-16 06:35:59','2026-09-16 06:35:59','QUALITY'),(15,'production','$2b$12$c9bx3X7F59y0ujAEI2MyIeuC2/pxjnuObhJu3yWr.lWHadrDBA2ju','鐢熶骇璐熻矗浜?,NULL,NULL,NULL,1,NULL,'2026-09-16 06:36:01','2026-09-16 06:36:01','PRODUCTION'),(16,'test_eng','$2b$12$AUZYTowrUrEZNV/qFaFRB.qB/OS3cllO0NJw5e7s/wKYP3x6pMM0S','娴嬭瘯宸ョ▼甯?,NULL,NULL,NULL,1,NULL,'2026-09-16 06:36:04','2026-09-16 06:36:04','TEST_ENGINEER');
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-17  4:49:02
