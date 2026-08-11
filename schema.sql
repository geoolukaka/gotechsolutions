-- GoTech Solutions - contact form MySQL schema
-- The backend auto-creates this table on startup, so running this file by
-- hand is optional -- useful if you want to create the database/user first
-- or inspect the schema up front.

CREATE DATABASE IF NOT EXISTS gotech_contact
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE gotech_contact;

CREATE TABLE IF NOT EXISTS submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(200) NOT NULL,
    phone VARCHAR(30),
    service VARCHAR(60),
    message TEXT NOT NULL,
    page VARCHAR(500),
    ip_address VARCHAR(64)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Optional: a dedicated least-privilege application user instead of root.
-- CREATE USER 'gotech_app'@'%' IDENTIFIED BY 'choose-a-strong-password';
-- GRANT SELECT, INSERT ON gotech_contact.* TO 'gotech_app'@'%';
-- FLUSH PRIVILEGES;
