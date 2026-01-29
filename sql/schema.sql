-- ATM Transaction Monitoring & Fraud Detection
-- Database Schema

DROP DATABASE IF EXISTS atm_monitoring;

CREATE DATABASE atm_monitoring;
USE atm_monitoring;

-- Customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50)
);

-- ATMs table
CREATE TABLE atms (
    atm_id INT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    country VARCHAR(50)
);

-- Transactions table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    atm_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    transaction_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (atm_id) REFERENCES atms(atm_id)
);