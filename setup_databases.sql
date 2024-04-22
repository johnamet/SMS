-- SQL script to create sms_test_db database if it does not exist
CREATE DATABASE IF NOT EXISTS sms_test_db;

-- SQL script to create sms_dev_db da7tabase if it does not exist
CREATE DATABASE IF NOT EXISTS sms_dev_db;

-- SQL script to create test_sms user if it does not exist
CREATE USER IF NOT EXISTS 'test_sms'@'localhost' IDENTIFIED BY 'test_sms_password';

-- SQL script to create dev_sms user if it does not exist
CREATE USER IF NOT EXISTS 'dev_sms'@'localhost' IDENTIFIED BY 'dev_sms_password';

-- SQL script to grant all privileges on sms_test_db to test_sms user
GRANT ALL PRIVILEGES ON sms_test_db.* TO 'test_sms'@'localhost';

-- SQL script to grant all privileges on sms_dev_db to dev_sms user
GRANT ALL PRIVILEGES ON sms_dev_db.* TO 'dev_sms'@'localhost';

-- SQL script to grant SELECT privilege on performance_schema to both users
GRANT SELECT ON performance_schema.* TO 'test_sms'@'localhost';
GRANT SELECT ON performance_schema.* TO 'dev_sms'@'localhost';
