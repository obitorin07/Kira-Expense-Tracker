-- DROP DATABASE IF EXISTS expense_tracker;
-- CREATE DATABASE expense_tracker;
-- USE expense_tracker;

-- -- Create Expenses Table
-- CREATE TABLE IF NOT EXISTS expenses (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     date_time DATETIME NOT NULL,
--     category VARCHAR(50) NOT NULL,
--     amount DECIMAL(10,2) NOT NULL,
--     description TEXT,
--     payment_method VARCHAR(20)
-- );

-- -- Create Budget Table
-- CREATE TABLE IF NOT EXISTS budget (
--     month_year VARCHAR(7) PRIMARY KEY,
--     total_budget DECIMAL(10,2) NOT NULL
-- );
BEGIN;

USE expense_tracker;

SELECT * FROM BUDGET; 
SELECT * FROM EXPENSES;

-- update expenses set category ='Food & Groceries' where id = 9;
-- truncate table expenses;

-- SELECT * FROM EXPENSES where date(date_time) = date_sub(current_date() , interval 1 day);