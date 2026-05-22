import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'vuln.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS secret_users")
    cursor.execute("DROP TABLE IF EXISTS categories")

    # Create products table for Lab 1, 3, 4, 5, 6, 7, 8
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            category TEXT,
            released INTEGER DEFAULT 1,
            price INTEGER
        )
    ''')

    # Create users table for Lab 2 (login)
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    # Create secret_users table for Lab 5, 6
    cursor.execute('''
        CREATE TABLE secret_users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    ''')

    # Insert sample products
    products = [
        (1, 'Laptop Pro', 'High-performance laptop for professionals', 'Electronics', 1, 1200),
        (2, 'Wireless Mouse', 'Ergonomic wireless mouse', 'Electronics', 1, 25),
        (3, 'Gaming Chair', 'Comfortable gaming chair', 'Furniture', 1, 300),
        (4, 'Secret Project X', 'Classified product - not released', 'Electronics', 0, 9999),
        (5, 'Internal Tool Beta', 'Internal testing tool', 'Software', 0, 0),
        (6, 'Office Desk', 'Standard office desk', 'Furniture', 1, 450),
        (7, 'Unreleased Phone', 'Next-gen smartphone prototype', 'Electronics', 0, 899),
        (8, 'Conference Table', 'Large meeting table', 'Furniture', 1, 800),
    ]
    cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?,?)', products)

    # Insert users for Lab 2
    users = [
        (1, 'administrator', 'supersecret123', 'admin'),
        (2, 'john_doe', 'password123', 'user'),
        (3, 'jane_smith', 'qwerty456', 'user'),
        (4, 'guest', 'guestpass', 'guest'),
    ]
    cursor.executemany('INSERT INTO users VALUES (?,?,?,?)', users)

    # Insert secret_users for Lab 5, 6
    secret_users = [
        (1, 'admin', 'admin_pass_2024'),
        (2, 'root', 'toor_root_99'),
        (3, 'backup_admin', 'bkup_$$secure'),
        (4, 'dev_user', 'dev_env_123'),
    ]
    cursor.executemany('INSERT INTO secret_users VALUES (?,?,?)', secret_users)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
