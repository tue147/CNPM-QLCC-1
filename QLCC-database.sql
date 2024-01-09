-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: cnpm-ittn.mysql.database.azure.com    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dich_vu`
--

DROP TABLE IF EXISTS `dich_vu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dich_vu` (
  `ID_DICH_VU` int NOT NULL,
  `TEN_DICH_VU` varchar(200) NOT NULL,
  `don_gia` int DEFAULT NULL,
  `BAT_BUOC` tinyint NOT NULL DEFAULT '0',
  `TINH` tinyint DEFAULT NULL,
  `HIEN_HANH` tinyint DEFAULT NULL,
  PRIMARY KEY (`ID_DICH_VU`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dich_vu`
--

LOCK TABLES `dich_vu` WRITE;
/*!40000 ALTER TABLE `dich_vu` DISABLE KEYS */;
INSERT INTO `dich_vu` VALUES (1,'Điện',3000,1,0,1),(2,'Nước',2500,1,0,1),(3,'Trông xe',25000,1,0,1),(4,'Ủng hộ chất độc màu da cam',NULL,0,0,1),(5,'Ủng hộ miền Trung lũ lụt',NULL,0,0,1),(6,'Dọn dẹp',50000,0,1,1),(7,'Bảo vệ',100000,1,1,1);
/*!40000 ALTER TABLE `dich_vu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ho_gd`
--

DROP TABLE IF EXISTS `ho_gd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ho_gd` (
  `ID_HO` int NOT NULL,
  `CHU_HO` varchar(200) NOT NULL,
  `ID_TAI_KHOAN` int NOT NULL,
  `SO_PHONG` int NOT NULL,
  `LOAI_PHONG` int NOT NULL,
  PRIMARY KEY (`ID_HO`),
  UNIQUE KEY `SO_PHONG_UNIQUE` (`SO_PHONG`),
  UNIQUE KEY `ID_TAI_KHOAN` (`ID_TAI_KHOAN`),
  KEY `fk_HO_GD_TAI_KHOAN1_idx` (`ID_TAI_KHOAN`),
  KEY `fk_HO_GD_LOAI_PHONG1_idx` (`LOAI_PHONG`),
  CONSTRAINT `fk_HO_GD_LOAI_PHONG1` FOREIGN KEY (`LOAI_PHONG`) REFERENCES `loai_phong` (`LOAI_PHONG`),
  CONSTRAINT `fk_HO_GD_TAI_KHOAN1` FOREIGN KEY (`ID_TAI_KHOAN`) REFERENCES `tai_khoan` (`ID_TAI_KHOAN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ho_gd`
--

LOCK TABLES `ho_gd` WRITE;
/*!40000 ALTER TABLE `ho_gd` DISABLE KEYS */;
INSERT INTO `ho_gd` VALUES (0,'Nguyễn Đăng Dương',6,101,0),(1,'Cao Minh Tuệ',2,301,1),(2,'Nghiêm Minh Hiếu',3,401,0),(3,'Đỗ Đức Mạnh',4,201,1),(4,'Nguyễn Đắc Tiến',7,102,0);
/*!40000 ALTER TABLE `ho_gd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lich_su_dich_vu`
--

DROP TABLE IF EXISTS `lich_su_dich_vu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lich_su_dich_vu` (
  `stt` bigint unsigned NOT NULL AUTO_INCREMENT,
  `ID_DICH_VU` int NOT NULL,
  `TEN_DICH_VU` varchar(200) NOT NULL,
  `don_gia` int DEFAULT NULL,
  `BAT_BUOC` tinyint NOT NULL DEFAULT '0',
  `NGAY_SUA_DOI` date DEFAULT NULL,
  `LOAI_SUA_DOI` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `TINH` tinyint DEFAULT NULL,
  PRIMARY KEY (`stt`),
  KEY `fk1` (`ID_DICH_VU`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lich_su_dich_vu`
--

LOCK TABLES `lich_su_dich_vu` WRITE;
/*!40000 ALTER TABLE `lich_su_dich_vu` DISABLE KEYS */;
INSERT INTO `lich_su_dich_vu` VALUES (1,2,'Nước',2500,1,'2023-10-01','ADD',0),(2,3,'Trông xe',25000,1,'2023-10-01','ADD',0),(3,4,'Ủng hộ chất độc màu da cam',NULL,0,'2023-10-01','ADD',0),(4,5,'Ủng hộ miền Trung lũ lụt',NULL,0,'2023-10-01','ADD',0),(5,1,'Điện',4000,1,'2023-10-01','UPDATE',0),(6,8,'Than',4000,1,'2023-10-01','Delete',0),(7,6,'Dọn dẹp',50000,0,'2023-10-01','ADD',1),(8,7,'Bảo vệ',100000,1,'2023-10-01','ADD',1),(14,1,'Điện',4000,1,'2023-10-01','ADD',0);
/*!40000 ALTER TABLE `lich_su_dich_vu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lich_su_ho_gd`
--

DROP TABLE IF EXISTS `lich_su_ho_gd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lich_su_ho_gd` (
  `stt` bigint unsigned NOT NULL AUTO_INCREMENT,
  `ID_HO` int NOT NULL,
  `CHU_HO` varchar(200) NOT NULL,
  `ID_TAI_KHOAN` int NOT NULL,
  `SO_PHONG` int NOT NULL,
  `LOAI_PHONG` int NOT NULL,
  `NGAY_SUA_DOI` date DEFAULT NULL,
  `LOAI_SUA_DOI` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`stt`),
  KEY `fk_HO_GD_TAI_KHOAN2_idx` (`ID_TAI_KHOAN`),
  KEY `fk_HO_GD_LOAI_PHONG2_idx` (`LOAI_PHONG`),
  CONSTRAINT `fk_HO_GD_LOAI_PHONG2` FOREIGN KEY (`LOAI_PHONG`) REFERENCES `loai_phong` (`LOAI_PHONG`),
  CONSTRAINT `fk_HO_GD_TAI_KHOAN2` FOREIGN KEY (`ID_TAI_KHOAN`) REFERENCES `tai_khoan` (`ID_TAI_KHOAN`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lich_su_ho_gd`
--

LOCK TABLES `lich_su_ho_gd` WRITE;
/*!40000 ALTER TABLE `lich_su_ho_gd` DISABLE KEYS */;
INSERT INTO `lich_su_ho_gd` VALUES (1,10,'Cao Minh Tuệ',2,5361,0,'2024-01-03','Add'),(2,10,'Cao Minh Tuệ',2,5361,0,'2024-01-10','Delete'),(3,0,'Nguyễn Đăng Dương',6,101,0,'2024-01-05','Update'),(4,2,'Nghiêm Minh Hiếu',3,401,0,'2023-12-31','ADD'),(5,3,'Đỗ Đức Mạnh',4,201,1,'2023-12-31','ADD'),(6,4,'Nguyễn Đắc Tiến',7,102,0,'2023-12-31','ADD'),(7,1,'Cao Minh Tuệ',2,301,0,'2023-12-31','ADD');
/*!40000 ALTER TABLE `lich_su_ho_gd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lich_su_nhan_khau`
--

DROP TABLE IF EXISTS `lich_su_nhan_khau`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lich_su_nhan_khau` (
  `stt` bigint unsigned NOT NULL AUTO_INCREMENT,
  `CCCD` varchar(12) NOT NULL,
  `HO_TEN` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `NGAY_SINH` date DEFAULT NULL,
  `QUAN_HE` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `TINH_TRANG_CU_TRU` tinyint NOT NULL DEFAULT '1',
  `ID_HO` int NOT NULL,
  `NGAY_SUA_DOI` date DEFAULT NULL,
  `LOAI_SUA_DOI` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`stt`),
  KEY `fk_NHAN_KHAU_HO_GD2_idx` (`ID_HO`),
  CONSTRAINT `fk_NHAN_KHAU_HO_GD2` FOREIGN KEY (`ID_HO`) REFERENCES `ho_gd` (`ID_HO`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lich_su_nhan_khau`
--

LOCK TABLES `lich_su_nhan_khau` WRITE;
/*!40000 ALTER TABLE `lich_su_nhan_khau` DISABLE KEYS */;
INSERT INTO `lich_su_nhan_khau` VALUES (1,'098767899876','Cao Minh Tệ','2023-07-02','chủ hộ',1,1,'2024-01-04','UPDATE'),(2,'098765432112','Vũ Minh Tệ','2023-07-02','chủ hộ',1,1,'2024-01-04','DELETE');
/*!40000 ALTER TABLE `lich_su_nhan_khau` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loai_phong`
--

DROP TABLE IF EXISTS `loai_phong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loai_phong` (
  `LOAI_PHONG` int NOT NULL,
  `TEN_PHONG` varchar(255) NOT NULL,
  `DIEN_TICH` int NOT NULL,
  `PHI_DICH_VU` int NOT NULL,
  PRIMARY KEY (`LOAI_PHONG`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loai_phong`
--

LOCK TABLES `loai_phong` WRITE;
/*!40000 ALTER TABLE `loai_phong` DISABLE KEYS */;
INSERT INTO `loai_phong` VALUES (0,'Thường',500,20000),(1,'VIP',1000,50000);
/*!40000 ALTER TABLE `loai_phong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhan_khau`
--

DROP TABLE IF EXISTS `nhan_khau`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhan_khau` (
  `CCCD` varchar(12) NOT NULL,
  `HO_TEN` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `NGAY_SINH` date DEFAULT NULL,
  `QUAN_HE` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `TINH_TRANG_CU_TRU` tinyint NOT NULL DEFAULT '1',
  `ID_HO` int NOT NULL,
  PRIMARY KEY (`CCCD`),
  KEY `fk_NHAN_KHAU_HO_GD1_idx` (`ID_HO`),
  CONSTRAINT `fk_NHAN_KHAU_HO_GD1` FOREIGN KEY (`ID_HO`) REFERENCES `ho_gd` (`ID_HO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhan_khau`
--

LOCK TABLES `nhan_khau` WRITE;
/*!40000 ALTER TABLE `nhan_khau` DISABLE KEYS */;
INSERT INTO `nhan_khau` VALUES ('098767899876','Cao Minh Tuệ','2023-07-02','chủ hộ',1,1),('123456789009','Nguyễn Đăng Dương','2023-06-02','chủ hộ',1,0),('131438088141','Khổng Thanh','1954-01-13','dì',1,2),('205919870329','Đặng Kiều','1999-09-23','chồng',0,1),('211854829326','Phương Phúc','1972-10-02','mẹ',0,4),('345678987545','Nghiêm Minh Hiếu','2023-01-02','chủ hộ',1,2),('347909178770','Đậu Dương','1988-11-21','em gái',1,4),('358081183630','Phạm Thảo','2022-10-22','mẹ',1,2),('406778451748','Trần Quyên','2020-12-02','con gái',0,3),('414961017558','Trang Mạnh','1987-08-05','em gái',1,0),('524405252759','Từ Khôi','1973-11-23','em trai',1,4),('535497129323','Châu Khang','1981-04-07','em gái',1,2),('576567859991','Nguyễn Đắc Tiến','2023-02-02','chủ hộ',1,4),('655460513941','Mã Thuận','2023-06-02','em gái',1,0),('664883124280','Lư Sang','1994-12-12','em gái',1,4),('757476274914','Đỗ Đức Mạnh','2023-04-02','chủ hộ',1,3),('773358584819','Lương Vi','1996-01-20','cô',0,1),('776280257925','Mạc Ân','1964-05-22','chồng',1,1),('785857927636','Giang Kiều','1985-04-03','con trai',1,2),('803877271353','Tiêu Dung','2008-12-14','con gái',0,0),('835872449423','Thi Nhàn','1982-03-26','chị gái',0,1),('839059677113','Bạch Quân','1957-02-27','chị gái',1,3),('896687799466','Liêu Phương','2003-02-02','con gái',1,3),('907321122993','Danh Phú','1974-01-05','con trai',0,3),('948884136064','Trang Hà','1996-11-12','bác',0,0);
/*!40000 ALTER TABLE `nhan_khau` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `STT` bigint NOT NULL AUTO_INCREMENT,
  `ID_TAI_KHOAN` int NOT NULL,
  `NOI_DUNG` varchar(10000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `NGAY` date DEFAULT NULL,
  PRIMARY KEY (`STT`),
  KEY `time` (`NGAY`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES (1,0,'Giá điện 3000 đồng 1 số','2023-12-31');
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tai_khoan`
--

DROP TABLE IF EXISTS `tai_khoan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tai_khoan` (
  `ID_TAI_KHOAN` int NOT NULL,
  `TEN_DANG_NHAP` varchar(16) NOT NULL,
  `MAT_KHAU` varchar(32) NOT NULL,
  `ADMIN` tinyint DEFAULT NULL,
  PRIMARY KEY (`ID_TAI_KHOAN`),
  UNIQUE KEY `TEN_DANG_NHAP` (`TEN_DANG_NHAP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tai_khoan`
--

LOCK TABLES `tai_khoan` WRITE;
/*!40000 ALTER TABLE `tai_khoan` DISABLE KEYS */;
INSERT INTO `tai_khoan` VALUES (0,'Alpha','123',0),(1,'admin','1',1),(2,'AnND','123',0),(3,'BinhND','123456',0),(4,'Beta','123',0),(6,'Gamma','abc123',0),(7,'Delta','hello',0),(8,'Zeta','abc123',0);
/*!40000 ALTER TABLE `tai_khoan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thu_chi`
--

DROP TABLE IF EXISTS `thu_chi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `thu_chi` (
  `STT` bigint unsigned NOT NULL AUTO_INCREMENT,
  `ID_DICH_VU` int NOT NULL,
  `ID_HO` int NOT NULL,
  `SO_LUONG` int DEFAULT '1',
  `GIA_TIEN` int NOT NULL,
  `DA_THU` int NOT NULL DEFAULT '0',
  `ngay_thu` date DEFAULT NULL,
  PRIMARY KEY (`STT`),
  KEY `fk_DIEN_NUOC_DICH_VU1_idx` (`ID_DICH_VU`),
  KEY `fk_THU_CHI_HO_GD1_idx` (`ID_HO`),
  CONSTRAINT `fk_DIEN_NUOC_DICH_VU1` FOREIGN KEY (`ID_DICH_VU`) REFERENCES `dich_vu` (`ID_DICH_VU`),
  CONSTRAINT `fk_THU_CHI_HO_GD1` FOREIGN KEY (`ID_HO`) REFERENCES `ho_gd` (`ID_HO`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thu_chi`
--

LOCK TABLES `thu_chi` WRITE;
/*!40000 ALTER TABLE `thu_chi` DISABLE KEYS */;
INSERT INTO `thu_chi` VALUES (1,1,0,20,60000,0,NULL),(2,1,1,10,30000,30000,'2024-01-04'),(3,2,1,10,25000,23000,'2024-01-04'),(4,3,1,5,125000,100000,'2024-01-04'),(5,1,2,20,60000,0,'2024-01-04'),(6,2,2,20,50000,0,'2024-01-04'),(7,3,2,1,25000,0,'2024-01-04'),(8,4,2,1,0,30000,'2024-01-04'),(9,5,2,1,0,25000,'2024-01-04'),(10,6,2,1,50000,0,'2024-01-04'),(11,7,2,1,100000,0,'2024-01-04');
/*!40000 ALTER TABLE `thu_chi` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-09 20:32:20
