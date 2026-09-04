mysqldump: [Warning] Using a password on the command line interface can be insecure.
mysqldump: Error: 'Access denied; you need (at least one of) the PROCESS privilege(s) for this operation' when trying to dump tablespaces
-- MySQL dump 10.13  Distrib 5.7.37, for Win64 (x86_64)
--
-- Host: localhost    Database: ims
-- ------------------------------------------------------
-- Server version	5.7.37-log

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
INSERT INTO `alembic_version` VALUES ('q1r2s3t4u5v6');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inbound_order`
--

LOCK TABLES `inbound_order` WRITE;
/*!40000 ALTER TABLE `inbound_order` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inbound_order_item`
--

LOCK TABLES `inbound_order_item` WRITE;
/*!40000 ALTER TABLE `inbound_order_item` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inbound_order_line`
--

LOCK TABLES `inbound_order_line` WRITE;
/*!40000 ALTER TABLE `inbound_order_line` DISABLE KEYS */;
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
  UNIQUE KEY `ix_incoming_inspection_inspection_no` (`inspection_no`),
  KEY `inspector_id` (`inspector_id`),
  KEY `ix_incoming_inspection_receipt_id` (`receipt_id`),
  CONSTRAINT `incoming_inspection_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `incoming_receipt` (`id`),
  CONSTRAINT `incoming_inspection_ibfk_2` FOREIGN KEY (`inspector_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incoming_inspection`
--

LOCK TABLES `incoming_inspection` WRITE;
/*!40000 ALTER TABLE `incoming_inspection` DISABLE KEYS */;
INSERT INTO `incoming_inspection` VALUES (1,1,'JC20260904001',1,'2026-09-04','ACCEPTED',5,0,'','A03楠屾敹娴嬭瘯',NULL,'2026-09-04 14:34:15','2026-09-04 14:34:15'),(2,3,'JC20260904002',1,'2026-09-04','CONCESSION_ACCEPTED',3,1,'澶栬杞诲井鐟曠柕','A05楠屾敹璁╂鎺ユ敹',NULL,'2026-09-04 14:36:31','2026-09-04 14:36:31');
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_incoming_receipt_receipt_no` (`receipt_no`),
  KEY `inspector_id` (`inspector_id`),
  KEY `ix_incoming_receipt_supplier_id` (`supplier_id`),
  KEY `ix_incoming_receipt_sku_id` (`sku_id`),
  KEY `ix_incoming_receipt_status` (`status`),
  CONSTRAINT `incoming_receipt_ibfk_1` FOREIGN KEY (`supplier_id`) REFERENCES `partner` (`id`),
  CONSTRAINT `incoming_receipt_ibfk_2` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`),
  CONSTRAINT `incoming_receipt_ibfk_3` FOREIGN KEY (`inspector_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incoming_receipt`
--

LOCK TABLES `incoming_receipt` WRITE;
/*!40000 ALTER TABLE `incoming_receipt` DISABLE KEYS */;
INSERT INTO `incoming_receipt` VALUES (1,'RC20260904001',4,6,'BATCH-20260810',30,'涓?,'ACCEPTED','2026-08-10',1,'2026-09-04','A03楠屾敹娴嬭瘯','宸插叆U9','2026-09-04 13:40:56','2026-09-04 14:34:15'),(2,'RC20260904002',4,7,'BATCH-20260812',194,'涓?,'REJECTED','2026-08-12',NULL,NULL,'A06楠屾敹娴嬭瘯','宸插叆U9','2026-09-04 13:40:56','2026-09-04 14:34:19'),(3,'RC20260904003',4,8,'BATCH-20260817',12,'涓?,'ACCEPTED','2026-08-17',1,'2026-09-04','A05楠屾敹璁╂鎺ユ敹','宸插叆U9','2026-09-04 13:40:56','2026-09-04 14:36:31'),(4,'RC20260904004',4,9,'BATCH-20260817',48,'涓?,'PENDING_INSPECTION','2026-08-17',NULL,NULL,NULL,'宸插叆U9','2026-09-04 13:40:56','2026-09-04 13:40:56'),(5,'RC20260904005',4,10,'BATCH-20260817',48,'涓?,'PENDING_INSPECTION','2026-08-17',NULL,NULL,NULL,'鏈鍏紝涓嶅叆绯荤粺','2026-09-04 13:40:56','2026-09-04 13:40:56'),(6,'RC20260904006',4,6,'TEST-20260904',10,'涓?,'PENDING_INSPECTION','2026-09-04',NULL,NULL,NULL,'A01楠屾敹娴嬭瘯','2026-09-04 14:34:10','2026-09-04 14:34:10');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incoming_return`
--

LOCK TABLES `incoming_return` WRITE;
/*!40000 ALTER TABLE `incoming_return` DISABLE KEYS */;
INSERT INTO `incoming_return` VALUES (1,2,'TH20260904001',2,'A06楠屾敹娴嬭瘯-閫€璐?,'2026-09-04','PENDING',1,'A06楠屾敹娴嬭瘯',NULL,'2026-09-04 14:34:19','2026-09-04 14:34:19');
/*!40000 ALTER TABLE `incoming_return` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_daily_summary`
--

LOCK TABLES `inventory_daily_summary` WRITE;
/*!40000 ALTER TABLE `inventory_daily_summary` DISABLE KEYS */;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_inventory_item_item_sn` (`item_sn`),
  KEY `ix_inventory_item_sku_id` (`sku_id`),
  KEY `ix_inventory_item_stock_status` (`stock_status`),
  CONSTRAINT `inventory_item_ibfk_1` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_item`
--

LOCK TABLES `inventory_item` WRITE;
/*!40000 ALTER TABLE `inventory_item` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_item_history`
--

LOCK TABLES `inventory_item_history` WRITE;
/*!40000 ALTER TABLE `inventory_item_history` DISABLE KEYS */;
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
  PRIMARY KEY (`id`),
  KEY `ix_inventory_item_snapshot_item_sn` (`item_sn`),
  KEY `ix_inventory_item_snapshot_snapshot_at` (`snapshot_at`),
  KEY `ix_inventory_item_snapshot_snapshot_month` (`snapshot_month`),
  KEY `ix_inventory_item_snapshot_snapshot_date` (`snapshot_date`),
  KEY `ix_inventory_item_snapshot_snapshot_type` (`snapshot_type`),
  KEY `ix_inventory_item_snapshot_date_type` (`snapshot_date`,`snapshot_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_item_snapshot`
--

LOCK TABLES `inventory_item_snapshot` WRITE;
/*!40000 ALTER TABLE `inventory_item_snapshot` DISABLE KEYS */;
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
  `outbound_scrapped` int(11) NOT NULL DEFAULT '0',
  `outbound_gifted` int(11) NOT NULL DEFAULT '0',
  `outbound_rnd` int(11) NOT NULL DEFAULT '0',
  `outbound_trial` int(11) NOT NULL DEFAULT '0',
  `outbound_sold_offline` int(11) NOT NULL DEFAULT '0',
  `outbound_repair` int(11) NOT NULL DEFAULT '0',
  `outbound_borrowed` int(11) NOT NULL DEFAULT '0',
  `outbound_sold` int(11) NOT NULL DEFAULT '0',
  `outbound_presold` int(11) NOT NULL DEFAULT '0',
  `outbound_sample` int(11) NOT NULL DEFAULT '0',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outbound_order`
--

LOCK TABLES `outbound_order` WRITE;
/*!40000 ALTER TABLE `outbound_order` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outbound_order_item`
--

LOCK TABLES `outbound_order_item` WRITE;
/*!40000 ALTER TABLE `outbound_order_item` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner`
--

LOCK TABLES `partner` WRITE;
/*!40000 ALTER TABLE `partner` DISABLE KEYS */;
INSERT INTO `partner` VALUES (1,'鏈寚瀹氾紙鍘嗗彶鏁版嵁锛?,1,0,NULL,1,'2026-09-04 13:06:48','2026-09-04 13:06:48'),(4,'瑗垮畨鐢垫皵渚涘簲鍟?,1,1,NULL,1,'2026-09-04 13:40:56','2026-09-04 13:40:56');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner_group`
--

LOCK TABLES `partner_group` WRITE;
/*!40000 ALTER TABLE `partner_group` DISABLE KEYS */;
INSERT INTO `partner_group` VALUES (1,'榛樿鍒嗙粍','2026-09-04 13:06:48','2026-09-04 13:06:48');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_category`
--

LOCK TABLES `product_category` WRITE;
/*!40000 ALTER TABLE `product_category` DISABLE KEYS */;
INSERT INTO `product_category` VALUES (2,'绌哄紑/鏂矾鍣?,'2026-09-04 13:40:56','2026-09-04 13:40:56');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_sku`
--

LOCK TABLES `product_sku` WRITE;
/*!40000 ALTER TABLE `product_sku` DISABLE KEYS */;
INSERT INTO `product_sku` VALUES (6,'绌哄紑',2,'303-060','BOTH',1,NULL,'2026-09-04 13:40:56','2026-09-04 13:40:56','涓?,'303-060','ABB S204-B1','RAW_MATERIAL'),(7,'绌哄紑',2,'303-074','BOTH',1,NULL,'2026-09-04 13:40:56','2026-09-04 13:40:56','涓?,'303-074','鏂借€愬痉 IC65N 2P C4A','RAW_MATERIAL'),(8,'绌哄紑',2,'303-107','BOTH',1,NULL,'2026-09-04 13:40:56','2026-09-04 13:40:56','涓?,'303-107','ABB S202-C10','RAW_MATERIAL'),(9,'绌哄紑',2,'303-108','BOTH',1,NULL,'2026-09-04 13:40:56','2026-09-04 13:40:56','涓?,'303-108','ABB S202-C4','RAW_MATERIAL'),(10,'鐔旀柇鍣ㄥ骇',2,'303-111','BOTH',1,NULL,'2026-09-04 13:40:56','2026-09-04 13:40:56','涓?,'303-111','姝ｆ嘲/RT28-32X 2P','RAW_MATERIAL');
/*!40000 ALTER TABLE `product_sku` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_inventory`
--

LOCK TABLES `raw_material_inventory` WRITE;
/*!40000 ALTER TABLE `raw_material_inventory` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_inventory_log`
--

LOCK TABLES `raw_material_inventory_log` WRITE;
/*!40000 ALTER TABLE `raw_material_inventory_log` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_audit_log`
--

LOCK TABLES `sys_audit_log` WRITE;
/*!40000 ALTER TABLE `sys_audit_log` DISABLE KEYS */;
INSERT INTO `sys_audit_log` VALUES (1,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-04 13:14:12',NULL),(2,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-04 13:14:41',NULL),(3,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'127.0.0.1','2026-09-04 14:05:42',NULL),(4,1,'绠＄悊鍛橈紙admin锛?,'LOGIN','auth','user','1','admin','绠＄悊鍛橈紙admin锛?鐧诲綍 绯荤粺',NULL,NULL,'::1','2026-09-04 14:10:07',NULL);
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
INSERT INTO `sys_config` VALUES (1,'app_name','IMS','2026-09-04 13:06:53','2026-09-04 13:06:53'),(2,'app_subtitle','涓€鐗╀竴鐮佸簱瀛樼鐞嗙郴缁?,'2026-09-04 13:06:53','2026-09-04 13:06:53');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_sequence`
--

LOCK TABLES `sys_sequence` WRITE;
/*!40000 ALTER TABLE `sys_sequence` DISABLE KEYS */;
INSERT INTO `sys_sequence` VALUES (2,'RC','20260904',6,'2026-09-04 13:40:56','2026-09-04 14:34:10'),(4,'JC','20260904',2,'2026-09-04 14:34:15','2026-09-04 14:36:31'),(5,'TH','20260904',1,'2026-09-04 14:34:19','2026-09-04 14:34:19');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES (1,'admin','$2b$12$4/y/SC2Txh9YGY1Wv6XXfOO6KDhHcs9G5cDf51m04jJQlwDYNbr5G','绠＄悊鍛?,NULL,NULL,NULL,1,NULL,'2026-09-04 13:13:56','2026-09-04 13:13:56','ADMIN');
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

-- Dump completed on 2026-09-04 14:42:45
