-- Creates tables only if they do not exist
-- Database: green_energy_data

-- Select database
USE green_energy_data;

-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ENERGY USAGE TABLE

CREATE TABLE IF NOT EXISTS energy_usage (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    month VARCHAR(20) NOT NULL,
    electricity_kwh FLOAT NOT NULL,
    water_liters FLOAT NOT NULL,
    solar_units FLOAT DEFAULT 0,
    carbon_footprint FLOAT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_energy_user 
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

