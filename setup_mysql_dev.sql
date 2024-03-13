CREATE DATABASE IF NOT EXISTS yimbo_dev_db
CREATE USER IF NOT EXISTS 'yimbo_dev'@'localhost' IDENTIFIED BY 'yimbo_dev_pwd'
GRANT ALL PRIVILEGES ON yimbo_dev_db.* to 'yimbo_dev'@'localhost'
