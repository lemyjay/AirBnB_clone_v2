-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create user if if doesn't exist
CREATE USER IF NOT EXIST 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnd_dev'@'localhost';

-- Grant select privilege on performance_schema to the user
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';