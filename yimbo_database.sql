-- MySQL dump 10.13  Distrib 5.7.42, for Linux (x86_64)
--
-- Host: localhost    Database: podcast_radio_database
-- ------------------------------------------------------
-- Server version	5.7.42

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
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Tech & Science'),(2,'Celebrity & Entertainment'),(3,'News & Politics'),(4,'Comedy');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(65) NOT NULL,
  `region_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `region_id` (`region_id`),
  CONSTRAINT `country_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;
INSERT INTO `country` VALUES (1,'South Africa',1),(2,'Kenya',2),(3,'Ethiopia',2),(4,'Egypt',3),(5,'Morocco',3),(6,'Nigeria',4),(7,'Senegal',4);
/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genre`
--

DROP TABLE IF EXISTS `genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `genre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `picture` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genre`
--

LOCK TABLES `genre` WRITE;
/*!40000 ALTER TABLE `genre` DISABLE KEYS */;
INSERT INTO `genre` VALUES (8,'Pop','Pop.jpg'),(9,'Rap','rap.jpg'),(10,'Mbalakh','mbalax.jpg'),(11,'Afrobeats','Afro.jpg'),(13,'Reggae','reggae.jpg'),(14,'Soul','soul.jpg'),(15,'Dancehall','dancehall.jpg'),(16,'Afrobeat','afrobeats.jpg'),(17,'Zouk','zouk.jpg'),(18,'French Urban Pop','French Urban Pop.jpg'),(19,' Nigerian R&B','niga.jpg'),(20,' Jolofbeats','Jolofbeats.jpg');
/*!40000 ALTER TABLE `genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `music`
--

DROP TABLE IF EXISTS `music`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `music` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `artist_name` varchar(100) NOT NULL,
  `duration` varchar(100) NOT NULL,
  `genre_id` int(11) DEFAULT NULL,
  `music_file` varchar(250) NOT NULL,
  `picture` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `music_ibfk_1` FOREIGN KEY (`genre_id`) REFERENCES `genre` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `music`
--

LOCK TABLES `music` WRITE;
/*!40000 ALTER TABLE `music` DISABLE KEYS */;
INSERT INTO `music` VALUES (1,'Lees Waxul','Youssou Ndour & Yande Codou Sene','06:14',10,'Lees_Waxul18181.mp3','lees_waxul.jpg'),(2,'Boulko Tek Missér','Wally B. Seck','04:44',10,'Wally_B._Seck_-_Boulko_Tek_Misser.mp3','wally_seck.jpg'),(3,'Tyla - Water','Tyla','03:39',11,'Tyla_-_Water_Official_Music_Video.mp3','Tyla_-_Water.jpg'),(4,'Coup du marteau','Tam sir','03:06',18,'Tam_Sir_-_Coup_du_marteau_feat._Team_Paiya_Ste_Milano_Renard_Barakissa_Tazeboy_PSK.mp3','coup_du_marteau.jpg'),(5,'Gimme Love','Litovibes','02:29',14,'Litovibes_-_Gimme_Love_Official_Visualizer.mp3','Litovibes.jpg'),(6,'Rush','Ayra Starr','03:05',19,'Ayra_Starr_-_Rush_Official_Music_Video.mp3','Ayra_Starr_-_Rush.jpg'),(7,'People','Libianca','03:17',19,'Libianca_-_People_Official_Video.mp3','Libianca_-_People.jpg'),(8,'Egwu','Chiké & Mohbad','02:25',11,'Chike__Mohbad_-_Egwu_Official_Video.mp3','Chike__Mohbad_-_Egwu.jpg'),(9,'Spyro ft Tiwa Savage - Who is Your Guy Remix','Spyro','03:29',11,'Spyro_ft_Tiwa_Savage_-_Who_is_your_Guy_Remix_Official_Video.mp3','Spyro_ft_Tiwa_Savage_-_Who_is_Your_Guy_Remix.jpg'),(10,'Soso','Omah Lay','03:04',8,'Omah_Lay_-_soso_Official_Music_Video.mp3','Omah_Lay_-_soso.jpg'),(11,'Calm Down','Rema','03:39',11,'Rema_-_Calm_Down_Official_Music_Video.mp3','Rema_-_Calm_Down.jpg'),(12,'IBLISS','King Baba','03:44',9,'King_Baba_-_IBLISS_clip_officiel.mp3','King_Baba_-_IBLISS.jpg'),(13,'Paris Dakar','Pape Diouf','04:06',10,'Pape_Diouf_-_Paris_Dakar__Clip_officiel_.mp3','Pape_Diouf_-_Paris_Dakar.jpg'),(14,'DIOKH KO LOVE','Iss 814','02:24',8,'Iss_814_DIOKH_KO_LOVE_Official_Video.mp3','Iss_814_DIOKH_KO_LOV.jpg'),(15,'Thiopet Yobu ','Jeeba','03:19',20,'Jeeba_-_Thiopet_Yobu_Clip_Officiel.mp3','Jeeba_-_Thiopet_Yobu.jpg'),(16,'Superman Love','Pape Diouf','04:09',10,'Pape_Diouf_-_Superman_Love_Clip_Officiel.mp3','Pape_Diouf_-_Superman_Love.jpg'),(17,'Hey Ya','Wally B. Seck ','03:57',8,'Wally_B._Seck_Hey_Ya.mp3','Wally_B._Seck_Hey_Ya.jpg'),(19,'Zungushiwa','Ssaru','03:17',11,'Zungushiwa_CD_1_TRACK_1_320.mp3','maxresdefault.jpg'),(20,'Ojapiano','Kcee','02:52',8,'Kcee_-_Ojapiano_Official_Video.mp3','Kcee_-_Ojapiano.jpg'),(21,'Anabella','Khaid','02:05',8,'Khaid_-_Anabella_Official_Music_Video.mp3','Khaid_-_Anabella.jpg'),(22,'Wada du game move','Wada Du Game','02:51',9,'Wada_du_game_move_Clip_officielRAP_GUINEEN_RAP_AFRICAIN.mp3','wada.jpg'),(23,'KokoLoko','Rvenio','03:03',11,'Rvenio_-_KokoLoko_Official_Music_Video.mp3','Rvenio_-_KokoLoko.jpg'),(24,'Queen of the Dancehall','Spice','02:37',15,'Spice_-_Queen_of_the_Dancehall_Official_Video.mp3','Spice_-_Queen_of_the_Dancehall.jpg'),(25,'Drag Dem Bat ','Vybz Kartel','03:23',15,'Vybz_Kartel_-_Drag_Dem_Bat_Official_Music_Video.mp3','Vybz_Kartel_-_Drag_Dem_Bat.jpg'),(26,'Run Dancehall','Vybz Kartel','02:32',15,'Vybz_Kartel_-_Run_Dancehall_Official_Video_ft._Lisa_Mercedez.mp3','Vybz_Kartel_-_Run_Dancehall.jpg'),(27,'Etana - Reggae','Etana','06:00',13,'Etana_-_Reggae_Official_Music_Video.mp3','Etana_-_Reggae.jpg'),(28,'Mad Head','Popcaan, Shane O','02:41',13,'Popcaan_Shane_O_-_Mad_Head_Official_Music_Video.mp3','Popcaan_Shane_O_-_Mad_Head.jpg'),(29,'Rasta Reggae Music ','Lutan Fyah','04:14',13,'Lutan_Fyah_-_Rasta_Reggae_Music_Official_Music_Video.mp3','Lutan_Fyah_-_Rasta_Reggae_Music.jpg');
/*!40000 ALTER TABLE `music` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `podcast`
--

DROP TABLE IF EXISTS `podcast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `podcast` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(1024) NOT NULL,
  `category_id` int(11) NOT NULL,
  `region_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `image_id` varchar(255) NOT NULL,
  `audio_id` int(11) NOT NULL,
  `picture` varchar(250) DEFAULT 'none',
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `country_id` (`country_id`),
  KEY `region_id` (`region_id`),
  CONSTRAINT `podcast_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `podcast_ibfk_2` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`),
  CONSTRAINT `podcast_ibfk_3` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `podcast`
--

LOCK TABLES `podcast` WRITE;
/*!40000 ALTER TABLE `podcast` DISABLE KEYS */;
INSERT INTO `podcast` VALUES (1,'Africa Tech Today','interviews with founders of startups and discussions on the latest trends.',1,1,1,'1',1,'1_African_tech_today.png'),(2,'The Business of Innovation in Africa','interviews with entrepreneurs, investors, and policymakers.',1,1,1,'2',2,'2_BusinessOfInnovationInAfricaPodcast.png'),(3,'TXRD Podcast','interviews with experts in a variety of fields, as well as discussions on current events and trends.',1,1,1,'3',3,'3_TXRDPodcast.png'),(4,'Express Yourself','interview-based podcast features South African personalities.',2,1,1,'4',4,'4_expressyourself.png'),(5,'Behind the Curtain with MacGyver','features South African personalities, often media personalities or entertainers0.',2,1,1,'5',5,'5_behindTheCurtains.png'),(6,'The Daily Maverick','In-depth interviews and discussions on current events in South Africa.',3,1,1,'6',6,'6_TheDailyMaverick.png'),(7,'Checkpoint','investigative journalism podcast from the South African Broadcasting Corporation (SABC).',3,1,1,'7',7,'7_checkPoint.png'),(8,'Ya Rassi!','stand-up comedy routines from some of South Africa\'s best comedians.',4,1,1,'8',8,'8_YaRassi.png'),(9,'Black Man With a Podcast','hosted by South African comedian and radio personality, Trevor Noah.',4,1,1,'9',9,'9_blackManWithAPodcast.png'),(10,'The Nairobi Tech Podcast','Exploring the tech scene in Kenya.',1,2,2,'10',10,'10_TheNairobiTechPodcast.png'),(11,'iCognito','focuses on science, technology, engineering, and mathematics (STEM) education.',1,2,3,'11',11,'11_iCognito.png'),(12,'KenyaBuzz','Covers entertainment news, celebrity gossip, and interviews with Kenyan celebrities.',2,2,2,'12',12,'12_KenyaBuzz.png'),(13,'Afripods Music','explores African music, featuring interviews with musicians from across the region.',2,2,3,'13',13,'13_Afripod_music_podcast.png'),(14,'Ethiopia Insight Podcast','Ethiopia Insight covers politics, economy, and society in Ethiopia.',3,2,3,'14',14,'14_EthiopiaInsightPodcast.png'),(15,'The Kenya Podcast','this podcast provides news and analysis on current events in Kenya, with a focus on politics, business, and social issues.',3,2,2,'15',15,'15_theKenyaPodcast.png'),(16,'Insanity by Chance','The hosts, Hanna and Mikiyas, are a married couple who use their humor to talk about relationships, life in Ethiopia, and anything else that comes to mind.',4,2,3,'16',16,'16_InsanityByChance.png'),(17,'The Lazarus Effect','The hosts, Eddy and Juress, interview celebrities and other interesting people, but they always keep things light and funny.',4,2,2,'17',17,'17_TheLazarusEffect.png'),(18,'The Nile Valley Podcast','This podcast explores the intersection of technology, science, and society in the Arab world. The hosts discuss a wide range of topics, from the latest tech startups to the history of science in the region.',1,3,4,'18',18,'18_TheNileValleyPodcast.png'),(19,'Innovation for Change','This podcast is produced by the American University in Cairo and features interviews with experts on science, technology, and innovation in Egypt and the Middle East.',1,3,4,'19',19,'19_InnovationForChange.png'),(20,'Tech Talk Morocco','The hosts interview entrepreneurs, investors, and other experts in the Moroccan tech scene.',1,3,5,'20',20,'20_TechTalkMorocco.png'),(21,'The Big Idea','This podcast features interviews with some of the biggest names in Egyptian entertainment, including actors, directors, and musicians.',2,3,4,'21',21,'21_TheBigIdea.png'),(22,'Mashael','This Moroccan talk show features interviews with celebrities, athletes, and other public figures. The host, Yannick Noah, is a former professional tennis player and singer.',2,3,5,'22',22,'22_Mashael.png'),(23,'Onza','Egyptian news podcast that covers a wide range of topics, from politics and current events to business and culture. The hosts provide in-depth analysis and commentary on the issues of the day.',3,3,4,'23',23,'23_Onza.png'),(24,'Maroc Diplomatique','podcast focuses on Morocco\'s foreign policy and its role in international affairs.',3,3,5,'24',24,'24_MarocDiplomatique.png'),(25,'Abla Fahita Show','Egyptian comedy show hosted by the comedian Abla Fahita. The show features a mix of stand-up comedy, sketches, and celebrity interviews',4,3,4,'25',25,'25_AblaFahitaShow.png'),(26,'Le Podcast de Mehdi','This French-language podcast is hosted by the witty Mehdi ML. He offers a humorous take on current events, pop culture, and social issues in Morocco and beyond.',4,3,5,'26',26,'26_LePodcastdeMehdi.png'),(27,'Techbytes','Damilare and Omoruyi, the hosts of Techbytes, delve into various tech topics relevant to a Nigerian audience.',1,4,6,'27',27,'27_Techbytes.png'),(28,'','',1,4,7,'28',28,NULL),(29,'Tea with Aifa','Hosted by Aifa Adamma. The show features in-depth interviews with celebrities from the Nigerian entertainment industry, including actors, musicians, comedians, and social media influencers.',2,4,6,'29',29,NULL),(30,'People of Dakar','his Senegalese podcast offers a window into the lives of fascinating individuals who are shaping Senegalese culture and society.',2,4,7,'30',30,'30_PeopleofDakar.png'),(31,'The Nigerian Daily Podcast','This daily podcast by The Nigerian Daily Newspaper offers concise and informative updates on current events in Nigeria. ',3,4,6,'31',31,NULL),(32,'Jokko Papers','prominent Senegalese investigative journalism podcast. Jokko Papers tackles political corruption, social injustices, and human rights abuses in Senegal.',3,4,7,'32',32,NULL),(33,'Laugh Out Loud with Basketmouth','This side-splitting podcast is hosted by Basketmouth, a legendary Nigerian comedian.',4,4,6,'33',33,NULL),(34,'Le Podcast de Youssou Ndour','Senegalese musician Youssou Ndour offers a unique blend of comedy and music.',4,4,7,'34',34,NULL);
/*!40000 ALTER TABLE `podcast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radio`
--

DROP TABLE IF EXISTS `radio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `description` varchar(256) NOT NULL,
  `region_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  `image_id` int(11) NOT NULL DEFAULT '0',
  `audio_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `country_id` (`country_id`),
  KEY `region_id` (`region_id`),
  CONSTRAINT `radio_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`),
  CONSTRAINT `radio_ibfk_2` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radio`
--

LOCK TABLES `radio` WRITE;
/*!40000 ALTER TABLE `radio` DISABLE KEYS */;
INSERT INTO `radio` VALUES (1,'SABC News International',' Specializes in news and current affairs, providing local and international coverage.',1,1,1,1),(2,'YFM',' Primarily targets a young audience with a focus on youth-oriented music, including hip hop and electronic dance music.',1,1,2,2),(3,'Good Hope FM','Offers a contemporary music mix, featuring local South African artists and popular international hits.',1,1,3,3),(4,'Radio 702','Known for its talk radio format, featuring in-depth discussions and interviews on various current affairs topics.',1,1,4,4),(5,'Kiss 100 FM',' Kenyan pop and international hits.',2,2,5,5),(6,'Classic 105','',2,2,6,6),(7,'Capital FM Kenya','Plays a mix of pop music, talk shows, and live sports coverage.',2,2,7,7),(8,'Ghetto Radio','playing Kenyan hip hop, reggae, and dancehall music',2,2,8,8),(9,'EBC','Ethiopia Broadcasting coorperation. Offers news, talk shows, and traditional Ethiopian music.',2,3,9,9),(10,'FBC','Fana Broadcasting Corporation. Offers news, talk shows, and Amharic music.',2,3,10,10),(11,'SABC News International',' Specializes in news and current affairs, providing local and international coverage.',1,1,11,11),(12,'YFM',' Primarily targets a young audience with a focus on youth-oriented music, including hip hop and electronic dance music.',1,1,12,12),(13,'Good Hope FM','Offers a contemporary music mix, featuring local South African artists and popular international hits.',1,1,13,13),(14,'Radio 702','Known for its talk radio format, featuring in-depth discussions and interviews on various current affairs topics.',1,1,14,14),(15,'Kiss 100 FM',' Kenyan pop and international hits.',2,2,15,15),(16,'Classic 105','',2,2,16,16),(17,'Capital FM Kenya','Plays a mix of pop music, talk shows, and live sports coverage.',2,2,17,17),(18,'Ghetto Radio','playing Kenyan hip hop, reggae, and dancehall music',2,2,18,18),(19,'EBC','Ethiopia Broadcasting coorperation. Offers news, talk shows, and traditional Ethiopian music.',2,3,19,19),(20,'FBC','Fana Broadcasting Corporation. Offers news, talk shows, and Amharic music.',2,3,20,20),(21,'Nile FM','Features Arabic hits and Egyptian pop music.',3,4,21,21),(22,'Egyptian Radio','The national radio broadcaster of Egypt, offering a variety of programs including news, Quran recitation, religious programs, and Arabic music.',3,4,22,22),(23,'Hit Radio','Features a mix of Moroccan and international pop music.',3,5,23,23),(24,'Radio Maroc','he national radio broadcaster of Morocco, offering news, talk shows, and Moroccan music (including traditional genres like Rai and Berber music.',3,5,24,24),(25,'Cool FM','plays a mix of contemporary hits and Nigerian music.',4,6,25,25),(26,'Nigeria Info','provides in-depth coverage of local and international stories, along with talk shows and interviews. \n',4,6,26,26),(27,'Beat FM','Beat FM plays a mix of hip hop, Afrobeats, and other urban music genres.',4,6,27,27),(28,'Wazobia FM',' plays a mix of Pidgin English language music and comedy skits.',4,6,28,28),(29,'Walf FM','Features diverse programs, including news, talk shows, sports, and music (Mbalax, hip hop, traditional music).',4,7,29,29),(30,'Sud FM','Features a mix of pop music, including local Senegalese artists and international hits.',4,7,30,30),(31,'Radio Senegal','The national radio broadcaster of Senegal, offering a variety of programs including news, talk shows, music (traditional and contemporary), and educational content.',4,7,31,31),(32,'iRadio','offers a mix of news, music (Mbalax, international music), talk shows, and live broadcasts.',4,7,32,32);
/*!40000 ALTER TABLE `radio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(65) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
INSERT INTO `region` VALUES (1,'South Africa'),(2,'East Africa'),(3,'North Africa'),(4,'West Africa');
/*!40000 ALTER TABLE `region` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-09  1:08:57
