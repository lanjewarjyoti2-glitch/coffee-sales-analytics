CREATE DATABASE IF NOT EXISTS coffee_sales_db;

USE coffee_sales_db;

CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATE,
    sale_datetime DATETIME,
    coffee_name VARCHAR(50),
    cash_type VARCHAR(20),
    money FLOAT
);