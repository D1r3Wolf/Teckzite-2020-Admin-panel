-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: localhost    Database: tz2020
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.10-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admins` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(120) NOT NULL,
  `name` varchar(120) NOT NULL,
  `mail` varchar(120) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `collegeid` varchar(10) NOT NULL,
  `totp_setup` int(2) NOT NULL,
  `totp_secret` varchar(20) NOT NULL,
  `priority` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'<User name>','<Password Hash>','<Name>','<Mail Address>','<Phone num>','<ID num>',0,'',0);
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departments` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `dept_name` varchar(50) NOT NULL,
  `login_creds` int(15) NOT NULL,
  `deleted` int(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dept_name` (`dept_name`),
  KEY `login_creds` (`login_creds`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_classes`
--

DROP TABLE IF EXISTS `event_classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_classes` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `eveid` int(15) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eveid` (`eveid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_classes`
--

LOCK TABLES `event_classes` WRITE;
/*!40000 ALTER TABLE `event_classes` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_contacts`
--

DROP TABLE IF EXISTS `event_contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_contacts` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `eveid` int(15) NOT NULL,
  `name` varchar(20) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `email` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eveid` (`eveid`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_contacts`
--

LOCK TABLES `event_contacts` WRITE;
/*!40000 ALTER TABLE `event_contacts` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_notifications`
--

DROP TABLE IF EXISTS `event_notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_notifications` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `eveid` int(15) NOT NULL,
  `title` varchar(40) NOT NULL,
  `content` varchar(300) NOT NULL,
  `time_stamp` int(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eveid` (`eveid`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_notifications`
--

LOCK TABLES `event_notifications` WRITE;
/*!40000 ALTER TABLE `event_notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_rules`
--

DROP TABLE IF EXISTS `event_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_rules` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `eveid` int(15) NOT NULL,
  `rules` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eveid` (`eveid`)
) ENGINE=InnoDB AUTO_INCREMENT=194 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_rules`
--

LOCK TABLES `event_rules` WRITE;
/*!40000 ALTER TABLE `event_rules` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_rules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `event_name` varchar(120) NOT NULL,
  `dept_id` int(15) NOT NULL,
  `min_part` int(2) NOT NULL DEFAULT -1,
  `max_part` int(2) NOT NULL DEFAULT -1,
  `event_place` varchar(15) NOT NULL DEFAULT '',
  `about` varchar(5000) NOT NULL DEFAULT '',
  `login_creds` int(15) NOT NULL,
  `deleted` int(1) NOT NULL,
  `visible` int(1) NOT NULL DEFAULT 1,
  `priority` int(100) NOT NULL DEFAULT 100,
  PRIMARY KEY (`id`),
  UNIQUE KEY `event_name` (`event_name`),
  KEY `dept_id` (`dept_id`),
  KEY `login_creds` (`login_creds`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_teams`
--

DROP TABLE IF EXISTS `events_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events_teams` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `eveid` int(15) NOT NULL,
  `teamid` int(15) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eveid` (`eveid`),
  KEY `teamid` (`teamid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_teams`
--

LOCK TABLES `events_teams` WRITE;
/*!40000 ALTER TABLE `events_teams` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizers`
--

DROP TABLE IF EXISTS `organizers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `organizers` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `collegeid` varchar(7) NOT NULL,
  `eveid` int(15) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eveid` (`eveid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizers`
--

LOCK TABLES `organizers` WRITE;
/*!40000 ALTER TABLE `organizers` DISABLE KEYS */;
/*!40000 ALTER TABLE `organizers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `teamid` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `tzid` varchar(10) NOT NULL,
  `uname` varchar(120) NOT NULL,
  `email` varchar(120) NOT NULL,
  `phone` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tzid` (`tzid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_teams`
--

DROP TABLE IF EXISTS `users_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_teams` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `uid` int(15) NOT NULL,
  `teamid` int(15) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`),
  KEY `teamid` (`teamid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_teams`
--

LOCK TABLES `users_teams` WRITE;
/*!40000 ALTER TABLE `users_teams` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workshop_contacts`
--

DROP TABLE IF EXISTS `workshop_contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workshop_contacts` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `workshopid` int(15) NOT NULL,
  `name` varchar(20) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `email` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workshopid` (`workshopid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workshop_contacts`
--

LOCK TABLES `workshop_contacts` WRITE;
/*!40000 ALTER TABLE `workshop_contacts` DISABLE KEYS */;
/*!40000 ALTER TABLE `workshop_contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workshop_notifications`
--

DROP TABLE IF EXISTS `workshop_notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workshop_notifications` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `workshopid` int(15) NOT NULL,
  `title` varchar(40) NOT NULL,
  `content` varchar(300) NOT NULL,
  `time_stamp` int(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workshopid` (`workshopid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workshop_notifications`
--

LOCK TABLES `workshop_notifications` WRITE;
/*!40000 ALTER TABLE `workshop_notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `workshop_notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workshop_rules`
--

DROP TABLE IF EXISTS `workshop_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workshop_rules` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `workshopid` int(15) NOT NULL,
  `rules` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workshopid` (`workshopid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workshop_rules`
--

LOCK TABLES `workshop_rules` WRITE;
/*!40000 ALTER TABLE `workshop_rules` DISABLE KEYS */;
/*!40000 ALTER TABLE `workshop_rules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workshop_topics`
--

DROP TABLE IF EXISTS `workshop_topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workshop_topics` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `workshopid` int(15) NOT NULL,
  `topics` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workshopid` (`workshopid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workshop_topics`
--

LOCK TABLES `workshop_topics` WRITE;
/*!40000 ALTER TABLE `workshop_topics` DISABLE KEYS */;
/*!40000 ALTER TABLE `workshop_topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workshops`
--

DROP TABLE IF EXISTS `workshops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workshops` (
  `id` int(15) NOT NULL AUTO_INCREMENT,
  `workshop_name` varchar(120) NOT NULL,
  `about` varchar(5000) NOT NULL DEFAULT '',
  `login_creds` int(15) NOT NULL,
  `deleted` int(1) NOT NULL,
  `visible` int(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `workshop_name` (`workshop_name`),
  KEY `login_creds` (`login_creds`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workshops`
--

LOCK TABLES `workshops` WRITE;
/*!40000 ALTER TABLE `workshops` DISABLE KEYS */;
/*!40000 ALTER TABLE `workshops` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-20 23:09:45
