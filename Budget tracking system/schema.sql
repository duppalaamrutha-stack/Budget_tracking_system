CREATE DATABASE IF NOT EXISTS budget_tracking;
USE budget_tracking;

CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  type VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
  transaction_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  category_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  transaction_date DATE NOT NULL,
  description VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS budgets (
  budget_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  category_id INT NOT NULL,
  limit_amount DECIMAL(10,2) NOT NULL,
  month VARCHAR(20) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

INSERT IGNORE INTO users (user_id, name, email, password)
VALUES (1, 'Ravi', 'ravi@example.com', '$2b$12$EXAMPLEPLACEHOLDERHASHxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');

INSERT IGNORE INTO categories (category_id, name, type)
VALUES
  (1, 'Salary', 'Income'),
  (2, 'Rent', 'Expense'),
  (3, 'Food', 'Expense'),
  (4, 'Utilities', 'Expense'),
  (5, 'Investment', 'Income');

INSERT IGNORE INTO transactions (transaction_id, user_id, category_id, amount, transaction_date, description)
VALUES
  (101, 1, 1, 30000.00, '2025-04-01', 'Monthly Salary'),
  (102, 1, 2, 8000.00, '2025-04-02', 'April Rent'),
  (103, 1, 3, 1500.00, '2025-04-03', 'Groceries'),
  (104, 1, 4, 1200.00, '2025-04-06', 'Electricity bill'),
  (105, 1, 3, 1800.00, '2025-04-10', 'Food and groceries');

INSERT IGNORE INTO budgets (budget_id, user_id, category_id, limit_amount, month)
VALUES
  (1, 1, 2, 8000.00, 'April'),
  (2, 1, 3, 4000.00, 'April'),
  (3, 1, 4, 2500.00, 'April');

DROP PROCEDURE IF EXISTS monthly_spending_by_category;
DELIMITER $$
CREATE PROCEDURE monthly_spending_by_category(IN uid INT, IN month_num INT, IN year_num INT)
BEGIN
  SELECT c.name AS category_name, IFNULL(SUM(t.amount), 0) AS total_spent
  FROM categories c
  LEFT JOIN transactions t ON c.category_id = t.category_id
    AND t.user_id = uid
    AND MONTH(t.transaction_date) = month_num
    AND YEAR(t.transaction_date) = year_num
    AND c.type = 'Expense'
  WHERE c.type = 'Expense'
  GROUP BY c.category_id, c.name;
END$$
DELIMITER ;

DROP FUNCTION IF EXISTS budget_exceeded;
DELIMITER $$
CREATE FUNCTION budget_exceeded(uid INT, cat_id INT, check_month VARCHAR(20))
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
  DECLARE spent DECIMAL(10,2);
  DECLARE limit_amt DECIMAL(10,2);
  SELECT IFNULL(SUM(t.amount), 0) INTO spent
  FROM transactions t
  JOIN categories c ON t.category_id = c.category_id
  WHERE t.user_id = uid
    AND t.category_id = cat_id
    AND c.type = 'Expense'
    AND DATE_FORMAT(t.transaction_date, '%M') = check_month;

  SELECT b.limit_amount INTO limit_amt
  FROM budgets b
  WHERE b.user_id = uid AND b.category_id = cat_id AND b.month = check_month
  LIMIT 1;

  RETURN spent > limit_amt;
END$$
DELIMITER ;

CREATE OR REPLACE VIEW monthly_summary AS
SELECT u.user_id,
       MONTH(t.transaction_date) AS month_num,
       YEAR(t.transaction_date) AS year_num,
       SUM(CASE WHEN c.type = 'Income' THEN t.amount ELSE 0 END) AS total_income,
       SUM(CASE WHEN c.type = 'Expense' THEN t.amount ELSE 0 END) AS total_expense
FROM transactions t
JOIN users u ON t.user_id = u.user_id
JOIN categories c ON t.category_id = c.category_id
GROUP BY u.user_id, MONTH(t.transaction_date), YEAR(t.transaction_date);
