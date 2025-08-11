-- Create user and grant permissions (MySQL 8.0 syntax)
CREATE USER IF NOT EXISTS 'messaging_user'@'%' IDENTIFIED BY 'messaging_password';
GRANT ALL PRIVILEGES ON messaging_db.* TO 'messaging_user'@'%';
FLUSH PRIVILEGES;
