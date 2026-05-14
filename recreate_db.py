import mysql.connector
import os

# Connect without database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345'
)
cursor = conn.cursor()

# Drop and recreate database
cursor.execute('DROP DATABASE IF EXISTS bank')
cursor.execute('CREATE DATABASE bank DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cursor.execute('USE bank')

# Create tables
cursor.execute('''
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    balance DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
''')

cursor.execute('''
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    type ENUM('deposit','withdraw','transfer_in','transfer_out') NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    related_account_id INT NULL,
    description VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
)
''')

conn.commit()
cursor.close()
conn.close()

print("Database recreated successfully!")