CREATE DATABASE IF NOT EXISTS parcel_management;

USE parcel_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL
);

CREATE TABLE parcels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender VARCHAR(100),
    receiver VARCHAR(100),
    status ENUM('received', 'in_transit', 'delivered') DEFAULT 'received',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transaction_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_id INT,
    status ENUM('received', 'in_transit', 'delivered'),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parcel_id) REFERENCES parcels(id)
);
