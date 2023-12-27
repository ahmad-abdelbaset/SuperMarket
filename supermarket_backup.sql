-- MySQL dump 10.13  Distrib 8.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: supermarket
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `BarCode` varchar(20) NOT NULL,
  `Description` varchar(120) DEFAULT NULL,
  `BuyingPrice` decimal(7,2) DEFAULT NULL,
  `SellingPrice` decimal(7,2) NOT NULL,
  `quantity` int DEFAULT NULL,
  `ExpDate` date DEFAULT NULL,
  PRIMARY KEY (`BarCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES ('01100','test_product',NULL,50.00,10,'2023-10-03'),('01300','test1_product',NULL,20.00,80,'2023-11-23'),('044100','test2_product',NULL,13.00,25,'2024-01-01'),('55464',NULL,NULL,50.00,NULL,NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sellingdetails`
--

DROP TABLE IF EXISTS `sellingdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sellingdetails` (
  `HistoryID` int DEFAULT NULL,
  `BarCode` varchar(20) DEFAULT NULL,
  KEY `HistoryID` (`HistoryID`),
  KEY `BarCode` (`BarCode`),
  CONSTRAINT `sellingdetails_ibfk_1` FOREIGN KEY (`HistoryID`) REFERENCES `sellinghistory` (`HistoryID`),
  CONSTRAINT `sellingdetails_ibfk_2` FOREIGN KEY (`BarCode`) REFERENCES `products` (`BarCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sellingdetails`
--

LOCK TABLES `sellingdetails` WRITE;
/*!40000 ALTER TABLE `sellingdetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `sellingdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sellinghistory`
--

DROP TABLE IF EXISTS `sellinghistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sellinghistory` (
  `HistoryID` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(20) NOT NULL,
  `TimeStamp` timestamp NOT NULL,
  PRIMARY KEY (`HistoryID`),
  KEY `UserName` (`UserName`),
  CONSTRAINT `sellinghistory_ibfk_1` FOREIGN KEY (`UserName`) REFERENCES `users` (`UserName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sellinghistory`
--

LOCK TABLES `sellinghistory` WRITE;
/*!40000 ALTER TABLE `sellinghistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `sellinghistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserName` varchar(20) NOT NULL,
  `Password` varchar(30) DEFAULT NULL,
  `AdminPermissions` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`UserName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('mohanad','1994',1),('test','0000',0),('test2','1111',1),('w1','1234',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-27 18:52:02
