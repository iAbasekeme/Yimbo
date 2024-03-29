-- Create the database
CREATE DATABASE IF NOT EXISTS podcast_database;

-- Use the created database
USE podcast_database;

--create region table
CREATE TABLE IF NOT EXISTS region (
	id 	int NOT NULL AUTO_INCREMENT,
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
  PRIMARY KEY (id),
  FOREIGN KEY(category_id) REFERENCES category(id),
  FOREIGN KEY(country_id) REFERENCES country(id),
  FOREIGN KEY(region_id) REFERENCES region(id)
);

-- Insert data for south African
INSERT INTO podcast (category_id, region_id,  country_id, name, description)
VALUES
  (1, 1, 1, 'Africa Tech Today', 'interviews with founders of startups and discussions on the latest trends.'),
  (1, 1, 1, 'The Business of Innovation in Africa', ' interviews with entrepreneurs, investors, and policymakers.'),
  (1, 1, 1, 'TXRD Podcast', 'interviews with experts in a variety of fields, as well as discussions on current events and trends.'),
  (2, 1, 1, 'Express Yourself', 'interview-based podcast features South African personalities.'),
  (2, 1, 1, 'Behind the Curtain with MacGyver', 'features South African personalities, often media personalities or entertainers0.')
  (3, 1, 1, 'The Daily Maverick', 'In-depth interviews and discussions on current events in South Africa..');
  (3, 1, 1, 'Checkpoint', 'investigative journalism podcast from the South African Broadcasting Corporation (SABC).')
  (4, 1, 1, 'Ya Rassi!', 'stand-up comedy routines from some of South Africa''s best comedians.')
  (4, 1, 1, 'Black Man With a Podcast', 'hosted by South African comedian and radio personality, Trevor Noah.')


-- Insert data for for East African
INSERT INTO podcast (category_id, region_id, country_id, name, description)
VALUES
  (1, 2, 2, 'The Nairobi Tech Podcast', 'Exploring the tech scene in Kenya.'),
  (1, 2, 3, 'iCognito', 'focuses on science, technology, engineering, and mathematics (STEM) education.'),
  (2, 2, 2, 'KenyaBuzz', 'Covers entertainment news, celebrity gossip, and interviews with Kenyan celebrities.'),
  (2, 2, 3, 'Afripods Music', 'explores African music, featuring interviews with musicians from across the region.'),
  (3, 2, 3, 'Ethiopia Insight Podcast', 'Ethiopia Insight covers politics, economy, and society in Ethiopia.'),
  (3, 2, 2, 'The Kenya Podcast', 'this podcast provides news and analysis on current events in Kenya, with a focus on politics, business, and social issues.'),
  (4, 2, 3, 'Insanity by Chance', 'The hosts, Hanna and Mikiyas, are a married couple who use their humor to talk about relationships, life in Ethiopia, and anything else that comes to mind.')
  (4, 2, 2, 'The Lazarus Effect', 'The hosts, Eddy and Juress, interview celebrities and other interesting people, but they always keep things light and funny.')

-- Insert data for North African
INSERT INTO podcast (category_id, region_id, country_id, name, description)
VALUES
  (1, 3, 4, 'The Nile Valley Podcast', 'Hosted by former Obama staffers, this podcast discusses politics and current events.'),
  (3, 3, 7, 'The Daily', 'A daily news podcast by The New York Times, covering top news stories and analysis.'),
  (3, 3, 1, 'The Rachel Maddow Show', 'The audio version of the popular MSNBC show, featuring in-depth political analysis.');

-- Insert data for comedy podcasts
INSERT INTO podcast (category_id, region_id, country_id, name, description)
VALUES
  (4, 3, 2, 'My Favorite Murder', 'Two comedians discuss true crime cases with humor and friendship.'),
  (4, 3, 3, 'The Daily Show with Trevor Noah', 'Satirical news program with comedic commentary on current events.'),
  (4, 1, 4, 'How Did This Get Made?', 'Features comedians discussing movies that are so bad they''re good (or just plain bad)');
