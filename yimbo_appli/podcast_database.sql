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

INSERT INTO podcast (category_id, region_id,  country_id, name, description)
VALUES
  (1, 2, 3, 'Reply All', 'Explores internet stories.'),
  (1, 1, 4, 'The Vergecast', 'Insightful analysis on tech news and internet culture.'),
  (1, 4, 2, 'TechStuff', 'Explores tech history, science, and impact.'),
  (1, 2, 1, 'Accidental Tech Podcast (ATP)', 'Focuses on Apple, tech, and programming news and debates.'),
  (1, 1, 3, 'Clockwise', 'Fast-paced discussions on tech topics, perfect for busy enthusiasts.');

-- Insert data for Celebrity & Entertainment podcasts
INSERT INTO podcast (category_id, region_id, country_id, name, description)
VALUES
  (2, 4, 4, 'My Dad Wrote A Porno', 'Hilariously dissects absurd erotic fiction.'),
  (2, 3, 4, 'The Joe Rogan Experience', 'Features comedian Joe Rogan''s long-form, humorous conversations.'),
  (2, 2, 5, '2 Dope Queens', 'Stand-up performances, storytelling, and interviews with comedians.'),
  (2, 1, 5, 'The Dollop with Dave Anthony and Gareth Reynolds', 'Comedians explore weird historical stories.'),
  (2, 2, 7, 'Conan O''Brien Needs A Friend', 'Conan O''Brien interviews celebrities for genuine friendship.');

-- Insert data for News & Politics podcasts
INSERT INTO podcast (category_id, region_id, country_id, name, description)
VALUES
  (3, 4, 7, 'Save America', 'Hosted by former Obama staffers, this podcast discusses politics and current events.'),
  (3, 4, 7, 'The Daily', 'A daily news podcast by The New York Times, covering top news stories and analysis.'),
  (3, 3, 1, 'The Rachel Maddow Show', 'The audio version of the popular MSNBC show, featuring in-depth political analysis.');

-- Insert data for comedy podcasts
INSERT INTO podcast (category_id, region_id, country_id, name, description)
VALUES
  (4, 3, 2, 'My Favorite Murder', 'Two comedians discuss true crime cases with humor and friendship.'),
  (4, 3, 3, 'The Daily Show with Trevor Noah', 'Satirical news program with comedic commentary on current events.'),
  (4, 1, 4, 'How Did This Get Made?', 'Features comedians discussing movies that are so bad they''re good (or just plain bad)');
