CREATE DATABASE IF NOT EXISTS podcast_radio_database;

-- use the database
USE podcast_radio_database;

-- create radio table
CREATE TABLE IF NOT EXISTS radio (
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(256) NOT NULL,
description VARCHAR(256) NOT NULL,
region_id INT NOT NULL,
country_id INT NOT NULL,
image_id INT NOT NULL DEFAULT 0,
PRIMARY KEY (id),
FOREIGN KEY(country_id) REFERENCES country(id),
FOREIGN KEY(region_id) REFERENCES region(id)
);

-- insert data for SOUTH AFRICAN
INSERT INTO radio (region_id,  country_id, name, description)
VALUES
	(1, 1, 'SABC News International', ' Specializes in news and current affairs, providing local and international coverage.'),
	(1, 1, 'YFM', ' Primarily targets a young audience with a focus on youth-oriented music, including hip hop and electronic dance music.'),
	(1, 1, 'Good Hope FM', 'Offers a contemporary music mix, featuring local South African artists and popular international hits.'),
	(1, 1, 'Radio 702', 'Known for its talk radio format, featuring in-depth discussions and interviews on various current affairs topics.');

-- insert data for EAST AFRICA
INSERT INTO radio (region_id,  country_id, name, description)
VALUES
(2, 2, 'Kiss 100 FM', ' Kenyan pop and international hits.'),
(2, 2, 'Classic 105', ''),
(2, 2, 'Capital FM Kenya', 'Plays a mix of pop music, talk shows, and live sports coverage.'),
(2, 2, 'Ghetto Radio', 'playing Kenyan hip hop, reggae, and dancehall music'),
(2, 3, 'EBC', 'Ethiopia Broadcasting coorperation. Offers news, talk shows, and traditional Ethiopian music.'),
(2, 3, 'FBC', 'Fana Broadcasting Corporation. Offers news, talk shows, and Amharic music.');


-- insert data for NORTH AFRICA
INSERT INTO radio (region_id,  country_id, name, description)
VALUES
(3, 4, 'Nile FM', 'Features Arabic hits and Egyptian pop music.'),
(3, 4, 'Egyptian Radio', 'The national radio broadcaster of Egypt, offering a variety of programs including news, Quran recitation, religious programs, and Arabic music.'),
(3, 5, 'Hit Radio', 'Features a mix of Moroccan and international pop music.'),
(3, 5, 'Radio Maroc', 'he national radio broadcaster of Morocco, offering news, talk shows, and Moroccan music (including traditional genres like Rai and Berber music.');


-- insert data into WEST AFRICA
INSERT INTO radio (region_id, country_id, name, description)
VALUES
(4, 6, 'Cool FM', 'plays a mix of contemporary hits and Nigerian music.'),
(4, 6, 'Nigeria Info', 'provides in-depth coverage of local and international stories, along with talk shows and interviews. 
'),
(4, 6, 'Beat FM', 'Beat FM plays a mix of hip hop, Afrobeats, and other urban music genres.'),
(4, 6, 'Wazobia FM', ' plays a mix of Pidgin English language music and comedy skits.'),
(4, 7, 'Walf FM', 'Features diverse programs, including news, talk shows, sports, and music (Mbalax, hip hop, traditional music).'),
(4, 7, 'Sud FM', 'Features a mix of pop music, including local Senegalese artists and international hits.'),
(4, 7, 'Radio Senegal', 'The national radio broadcaster of Senegal, offering a variety of programs including news, talk shows, music (traditional and contemporary), and educational content.'),
(4, 7, 'iRadio', 'offers a mix of news, music (Mbalax, international music), talk shows, and live broadcasts.');

-- initialize the image_id with the correspoing radio id
UPDATE radio SET image_id = id;
