-- Create the database
CREATE DATABASE IF NOT EXISTS podcast_radio_database;

-- Use the created database
USE podcast_radio_database;

--create region table
CREATE TABLE IF NOT EXISTS region (
    id int NOT NULL AUTO_INCREMENT,
    name VARCHAR(65) NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO region (name) VALUES ("South Africa"), ("East Africa"), ("North Africa"), ("West Africa");

-- Create the category table
CREATE TABLE IF NOT EXISTS category (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    PRIMARY KEY (id)
);
-- Insert data into the category table
INSERT INTO category (name) VALUES ("Tech & Science"), ("Celebrity & Entertainment"), ("News & Politics"), ("Comedy");

CREATE TABLE IF NOT EXISTS country (
    id int NOT NULL AUTO_INCREMENT,
    name VARCHAR(65) NOT NULL,
    region_id INT NOT NULL, 
    PRIMARY KEY(id),
    FOREIGN KEY(region_id) REFERENCES region(id)
);

INSERT INTO country (region_id, name)
VALUES (1, "South Africa"), (2, "Kenya"), (2, "Ethiopia"), (3, "Egypt"), (3, "Morocco"), (4, "Nigeria"), (4, "Senegal");

CREATE TABLE IF NOT EXISTS podcast (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    category_id INT NOT NULL,
    region_id INT NOT NULL,
    country_id INT NOT NULL,
    image_id INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    FOREIGN KEY(category_id) REFERENCES category(id),
    FOREIGN KEY(country_id) REFERENCES country(id),
    FOREIGN KEY(region_id) REFERENCES region(id)
);

-- Insert data for south African
INSERT INTO podcast (category_id, region_id,  country_id, name, description)
VALUES
    (1, 1, 1, 'Africa Tech Today', 'interviews with founders of startups and discussions on the latest trends.'),
    (1, 1, 1, 'The Business of Innovation in Africa', 'interviews with entrepreneurs, investors, and policymakers.'),
    (1, 1, 1, 'TXRD Podcast', 'interviews with experts in a variety of fields, as well as discussions on current events and trends.'),
    (2, 1, 1, 'Express Yourself', 'interview-based podcast features South African personalities.'),
    (2, 1, 1, 'Behind the Curtain with MacGyver', 'features South African personalities, often media personalities or entertainers0.'),
    (3, 1, 1, 'The Daily Maverick', 'In-depth interviews and discussions on current events in South Africa.'),
    (3, 1, 1, 'Checkpoint', 'investigative journalism podcast from the South African Broadcasting Corporation (SABC).'),
    (4, 1, 1, 'Ya Rassi!', 'stand-up comedy routines from some of South Africa''s best comedians.'),
    (4, 1, 1, 'Black Man With a Podcast', 'hosted by South African comedian and radio personality, Trevor Noah.');


-- Insert data for for East African
INSERT INTO podcast (category_id, region_id, country_id, name, description)
VALUES
    (1, 2, 2, 'The Nairobi Tech Podcast', 'Exploring the tech scene in Kenya.'),
    (1, 2, 3, 'iCognito', 'focuses on science, technology, engineering, and mathematics (STEM) education.'),
    (2, 2, 2, 'KenyaBuzz', 'Covers entertainment news, celebrity gossip, and interviews with Kenyan celebrities.'),
    (2, 2, 3, 'Afripods Music', 'explores African music, featuring interviews with musicians from across the region.'),
    (3, 2, 3, 'Ethiopia Insight Podcast', 'Ethiopia Insight covers politics, economy, and society in Ethiopia.'),
    (3, 2, 2, 'The Kenya Podcast', 'this podcast provides news and analysis on current events in Kenya, with a focus on politics, business, and social issues.'),
    (4, 2, 3, 'Insanity by Chance', 'The hosts, Hanna and Mikiyas, are a married couple who use their humor to talk about relationships, life in Ethiopia, and anything else that comes to mind.'),
    (4, 2, 2, 'The Lazarus Effect', 'The hosts, Eddy and Juress, interview celebrities and other interesting people, but they always keep things light and funny.');

-- Insert data for North African
INSERT INTO podcast (category_id, region_id, country_id, name, description)
VALUES
    (1, 3, 4, 'The Nile Valley Podcast', 'This podcast explores the intersection of technology, science, and society in the Arab world. The hosts discuss a wide range of topics, from the latest tech startups to the history of science in the region.'),
    (1, 3, 4, 'Innovation for Change', 'This podcast is produced by the American University in Cairo and features interviews with experts on science, technology, and innovation in Egypt and the Middle East.'),
    (1, 3, 5, 'Tech Talk Morocco', 'The hosts interview entrepreneurs, investors, and other experts in the Moroccan tech scene.'),
    (2, 3, 4, 'The Big Idea', 'This podcast features interviews with some of the biggest names in Egyptian entertainment, including actors, directors, and musicians.'),
    (2, 3, 5, 'Mashael', 'This Moroccan talk show features interviews with celebrities, athletes, and other public figures. The host, Yannick Noah, is a former professional tennis player and singer.'),
    (3, 3, 4, 'Onza', 'Egyptian news podcast that covers a wide range of topics, from politics and current events to business and culture. The hosts provide in-depth analysis and commentary on the issues of the day.'),
    (3, 3, 5, 'Maroc Diplomatique', 'podcast focuses on Morocco''s foreign policy and its role in international affairs.'),
    (4, 3, 4, 'Abla Fahita Show', 'Egyptian comedy show hosted by the comedian Abla Fahita. The show features a mix of stand-up comedy, sketches, and celebrity interviews'),
    (4, 3, 5, 'Le Podcast de Mehdi', 'This French-language podcast is hosted by the witty Mehdi ML. He offers a humorous take on current events, pop culture, and social issues in Morocco and beyond.');

-- Insert data for West Africa
INSERT INTO podcast (category_id, region_id, country_id, name, description)
VALUES
    (1, 4, 6, 'Techbytes', 'Damilare and Omoruyi, the hosts of Techbytes, delve into various tech topics relevant to a Nigerian audience.'),
    (1, 4, 7, '', ''),
    (2, 4, 6, 'Tea with Aifa', 'Hosted by Aifa Adamma. The show features in-depth interviews with celebrities from the Nigerian entertainment industry, including actors, musicians, comedians, and social media influencers.'),
    (2, 4, 7, 'People of Dakar', 'his Senegalese podcast offers a window into the lives of fascinating individuals who are shaping Senegalese culture and society.'),
    (3, 4, 6, 'The Nigerian Daily Podcast', 'This daily podcast by The Nigerian Daily Newspaper offers concise and informative updates on current events in Nigeria. '),
    (3, 4, 7, 'Jokko Papers', 'prominent Senegalese investigative journalism podcast. Jokko Papers tackles political corruption, social injustices, and human rights abuses in Senegal.'),
    (4, 4, 6, 'Laugh Out Loud with Basketmouth', 'This side-splitting podcast is hosted by Basketmouth, a legendary Nigerian comedian.'),
    (4, 4, 7, 'Le Podcast de Youssou Ndour', 'Senegalese musician Youssou Ndour offers a unique blend of comedy and music.'); 

-- Initialize image_id with the corresponding podcast id
UPDATE podcast SET image_id = id;