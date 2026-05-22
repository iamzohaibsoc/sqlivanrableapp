from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = 'sqli-lab-secret-key-2024'

# Initialize database on startup
@app.before_request
def setup():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

# ===================== HOME PAGE =====================
@app.route('/')
def index():
    return render_template('index.html')

# ===================== LAB 1: WHERE CLAUSE HIDDEN DATA =====================
@app.route('/lab1', methods=['GET', 'POST'])
def lab1():
    products = []
    query_executed = ""
    category = request.form.get('category', '') if request.method == 'POST' else ''

    conn = get_db_connection()
    cursor = conn.cursor()

    # VULNERABLE: Raw string concatenation - NO parameterization
    if request.method == 'POST':
        query = f"SELECT * FROM products WHERE category='{category}' AND released=1"
        query_executed = query
        try:
            cursor.execute(query)
            products = cursor.fetchall()
        except Exception as e:
            flash(f'SQL Error: {str(e)}', 'danger')
    else:
        # Default view - show only released products
        query = "SELECT * FROM products WHERE released=1"
        query_executed = query
        cursor.execute(query)
        products = cursor.fetchall()

    conn.close()
    return render_template('lab1_products.html', 
                         products=products, 
                         query=query_executed,
                         category=category,
                         lab_num=1,
                         lab_title="Hidden Data Bypass",
                         payload="' OR 1=1--",
                         description="Bypass the released=1 filter to see hidden products")

# ===================== LAB 2: LOGIN BYPASS =====================
@app.route('/lab2', methods=['GET', 'POST'])
def lab2():
    result = None
    query_executed = ""
    username = request.form.get('username', '') if request.method == 'POST' else ''
    password = request.form.get('password', '') if request.method == 'POST' else ''

    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        # VULNERABLE: Raw string concatenation in login query
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        query_executed = query

        try:
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                result = {
                    'success': True,
                    'username': user['username'],
                    'role': user['role']
                }
            else:
                result = {'success': False}
        except Exception as e:
            flash(f'SQL Error: {str(e)}', 'danger')
            result = {'success': False, 'error': str(e)}

        conn.close()

    return render_template('lab2_login.html',
                         result=result,
                         query=query_executed,
                         username=username,
                         lab_num=2,
                         lab_title="Login Bypass",
                         payload="administrator'--",
                         description="Bypass password check and login as any user")

# ===================== LAB 3: UNION COLUMN COUNT =====================
@app.route('/lab3', methods=['GET', 'POST'])
def lab3():
    products = []
    query_executed = ""
    error_msg = None
    search = request.form.get('search', '') if request.method == 'POST' else ''

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # VULNERABLE: Raw string concatenation
        query = f"SELECT id, name, description FROM products WHERE name LIKE '%{search}%'"
        query_executed = query
        try:
            cursor.execute(query)
            products = cursor.fetchall()
        except Exception as e:
            error_msg = str(e)
            flash(f'SQL Error: {str(e)}', 'danger')
    else:
        query = "SELECT id, name, description FROM products LIMIT 5"
        query_executed = query
        cursor.execute(query)
        products = cursor.fetchall()

    conn.close()
    return render_template('lab3_union.html',
                         products=products,
                         query=query_executed,
                         search=search,
                         error=error_msg,
                         lab_num=3,
                         lab_title="UNION Column Count",
                         payload="' UNION SELECT NULL,NULL,NULL--",
                         description="Determine how many columns the query returns")

# ===================== LAB 4: FINDING TEXT COLUMN =====================
@app.route('/lab4', methods=['GET', 'POST'])
def lab4():
    products = []
    query_executed = ""
    error_msg = None
    search = request.form.get('search', '') if request.method == 'POST' else ''

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # VULNERABLE: Returns columns of mixed types (id=integer, name=text, price=integer)
        query = f"SELECT id, name, price FROM products WHERE name LIKE '%{search}%'"
        query_executed = query
        try:
            cursor.execute(query)
            products = cursor.fetchall()
        except Exception as e:
            error_msg = str(e)
            flash(f'SQL Error: {str(e)}', 'danger')
    else:
        query = "SELECT id, name, price FROM products LIMIT 5"
        query_executed = query
        cursor.execute(query)
        products = cursor.fetchall()

    conn.close()
    return render_template('lab4_text.html',
                         products=products,
                         query=query_executed,
                         search=search,
                         error=error_msg,
                         lab_num=4,
                         lab_title="Text Column Detection",
                         payload="' UNION SELECT 'a',NULL,NULL--",
                         description="Identify which column can hold text data")

# ===================== LAB 5: RETRIEVING DATA FROM OTHER TABLES =====================
@app.route('/lab5', methods=['GET', 'POST'])
def lab5():
    products = []
    query_executed = ""
    error_msg = None
    search = request.form.get('search', '') if request.method == 'POST' else ''

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # VULNERABLE: 3 columns (id, name, description) - allows UNION with secret_users
        query = f"SELECT id, name, description FROM products WHERE name LIKE '%{search}%'"
        query_executed = query
        try:
            cursor.execute(query)
            products = cursor.fetchall()
        except Exception as e:
            error_msg = str(e)
            flash(f'SQL Error: {str(e)}', 'danger')
    else:
        query = "SELECT id, name, description FROM products LIMIT 5"
        query_executed = query
        cursor.execute(query)
        products = cursor.fetchall()

    conn.close()
    return render_template('lab5_tables.html',
                         products=products,
                         query=query_executed,
                         search=search,
                         error=error_msg,
                         lab_num=5,
                         lab_title="Cross-Table Data Retrieval",
                         payload="' UNION SELECT username,password,NULL FROM secret_users--",
                         description="Dump credentials from the secret_users table")

# ===================== LAB 6: MULTIPLE VALUES IN SINGLE COLUMN =====================
@app.route('/lab6', methods=['GET', 'POST'])
def lab6():
    products = []
    query_executed = ""
    error_msg = None
    search = request.form.get('search', '') if request.method == 'POST' else ''

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # VULNERABLE: Only 1 text column (name) - forces concatenation use
        query = f"SELECT id, name, price FROM products WHERE name LIKE '%{search}%'"
        query_executed = query
        try:
            cursor.execute(query)
            products = cursor.fetchall()
        except Exception as e:
            error_msg = str(e)
            flash(f'SQL Error: {str(e)}', 'danger')
    else:
        query = "SELECT id, name, price FROM products LIMIT 5"
        query_executed = query
        cursor.execute(query)
        products = cursor.fetchall()

    conn.close()
    return render_template('lab6_multi.html',
                         products=products,
                         query=query_executed,
                         search=search,
                         error=error_msg,
                         lab_num=6,
                         lab_title="Multiple Values in Single Column",
                         payload="' UNION SELECT NULL,username||':'||password,NULL FROM secret_users--",
                         description="Concatenate username and password into one column")

# ===================== LAB 7: DB VERSION =====================
@app.route('/lab7', methods=['GET', 'POST'])
def lab7():
    products = []
    query_executed = ""
    error_msg = None
    search = request.form.get('search', '') if request.method == 'POST' else ''

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # VULNERABLE: 3 columns - can inject sqlite_version()
        query = f"SELECT id, name, description FROM products WHERE name LIKE '%{search}%'"
        query_executed = query
        try:
            cursor.execute(query)
            products = cursor.fetchall()
        except Exception as e:
            error_msg = str(e)
            flash(f'SQL Error: {str(e)}', 'danger')
    else:
        query = "SELECT id, name, description FROM products LIMIT 5"
        query_executed = query
        cursor.execute(query)
        products = cursor.fetchall()

    conn.close()
    return render_template('lab7_version.html',
                         products=products,
                         query=query_executed,
                         search=search,
                         error=error_msg,
                         lab_num=7,
                         lab_title="Database Version Detection",
                         payload="' UNION SELECT sqlite_version(),NULL,NULL--",
                         description="Extract the SQLite database version string")

# ===================== LAB 8: LISTING DATABASE CONTENTS =====================
@app.route('/lab8', methods=['GET', 'POST'])
def lab8():
    products = []
    query_executed = ""
    error_msg = None
    search = request.form.get('search', '') if request.method == 'POST' else ''

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # VULNERABLE: 3 columns - can query sqlite_master
        query = f"SELECT id, name, description FROM products WHERE name LIKE '%{search}%'"
        query_executed = query
        try:
            cursor.execute(query)
            products = cursor.fetchall()
        except Exception as e:
            error_msg = str(e)
            flash(f'SQL Error: {str(e)}', 'danger')
    else:
        query = "SELECT id, name, description FROM products LIMIT 5"
        query_executed = query
        cursor.execute(query)
        products = cursor.fetchall()

    conn.close()
    return render_template('lab8_schema.html',
                         products=products,
                         query=query_executed,
                         search=search,
                         error=error_msg,
                         lab_num=8,
                         lab_title="Database Schema Listing",
                         payload="' UNION SELECT name,NULL,NULL FROM sqlite_master WHERE type='table'--",
                         description="List all tables and their schemas in the database")

# ===================== SAFE VERSION DEMO =====================
@app.route('/safe-demo', methods=['GET', 'POST'])
def safe_demo():
    products = []
    query_executed = ""
    category = request.form.get('category', '') if request.method == 'POST' else ''

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # SECURE: Parameterized query - IMMUNE to SQL injection
        query = "SELECT * FROM products WHERE category=? AND released=1"
        query_executed = f"SELECT * FROM products WHERE category='{category}' AND released=1 (SECURE - parameterized)"
        cursor.execute(query, (category,))
        products = cursor.fetchall()
    else:
        query = "SELECT * FROM products WHERE released=1"
        query_executed = query
        cursor.execute(query)
        products = cursor.fetchall()

    conn.close()
    return render_template('safe_demo.html',
                         products=products,
                         query=query_executed,
                         category=category)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
