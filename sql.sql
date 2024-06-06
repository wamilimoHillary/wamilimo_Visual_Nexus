-- Create database if not exists
CREATE DATABASE IF NOT EXISTS webgallery;

-- Switch to the created database
USE webgallery;

-- Create table for Structurefoods
CREATE TABLE IF NOT EXISTS foods (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    file_path VARCHAR(255),
    description VARCHAR(255),
    uploaded_at DATETIME
);

-- Create table for Structureplayers
CREATE TABLE IF NOT EXISTS players (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    file_path VARCHAR(255),
    description VARCHAR(255),
    uploaded_at DATETIME
);

-- Create table for users
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(255),
    user_password VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
