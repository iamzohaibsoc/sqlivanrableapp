# SQL Injection Laboratory — Vulnerable Flask Application

## Overview
This is an intentionally vulnerable Python Flask web application designed for educational purposes. 
It demonstrates 8 different SQL Injection vulnerability types matching the PortSwigger Web Academy curriculum.

**⚠️ WARNING:** This application contains deliberate security vulnerabilities. Do NOT deploy in production 
or expose to the internet. Use only in a controlled learning environment.

## Technology Stack
- **Backend:** Python 3.x + Flask
- **Database:** SQLite (built into Python)
- **Frontend:** HTML/Jinja2 Templates with White Traditional UI
- **Connector:** sqlite3 (Python standard library)

## Project Structure
```
sqli_app/
├── app.py                  # Main Flask application (8 vulnerable labs + 1 safe demo)
├── database.py             # Database initialization & seed data
├── requirements.txt        # Python dependencies
├── vuln.db                 # SQLite database (auto-created on first run)
└── templates/
    ├── base.html             # Base template with white traditional theme
    ├── index.html            # Home page with lab navigation
    ├── lab1_products.html    # Lab 1 — Hidden data bypass
    ├── lab2_login.html       # Lab 2 — Login bypass
    ├── lab3_union.html       # Lab 3 — UNION column count
    ├── lab4_text.html        # Lab 4 — Text column detection
    ├── lab5_tables.html      # Lab 5 — Cross-table data retrieval
    ├── lab6_multi.html       # Lab 6 — Multiple values in single column
    ├── lab7_version.html     # Lab 7 — DB version detection
    ├── lab8_schema.html      # Lab 8 — Database schema listing
    └── safe_demo.html        # Safe parameterized query demo
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python database.py
```

### 3. Run the Application
```bash
python app.py
```

### 4. Access in Browser
Open http://localhost:5000 in your web browser.

## The 8 SQL Injection Labs

| Lab | Route | Vulnerability | Payload Example |
|-----|-------|---------------|-----------------|
| 1 | `/lab1` | WHERE clause hidden data | `' OR 1=1--` |
| 2 | `/lab2` | Login bypass | `administrator'--` |
| 3 | `/lab3` | UNION column count | `' UNION SELECT NULL,NULL,NULL--` |
| 4 | `/lab4` | Text column detection | `' UNION SELECT 'a',NULL,NULL--` |
| 5 | `/lab5` | Cross-table data retrieval | `' UNION SELECT username,password,NULL FROM secret_users--` |
| 6 | `/lab6` | Multiple values in single column | `' UNION SELECT NULL,username\|\|':'\|\|password,NULL FROM secret_users--` |
| 7 | `/lab7` | DB version detection | `' UNION SELECT sqlite_version(),NULL,NULL--` |
| 8 | `/lab8` | Database schema listing | `' UNION SELECT name,NULL,NULL FROM sqlite_master WHERE type='table'--` |

## Safe Demo
Visit `/safe-demo` to see how the same functionality can be implemented securely using parameterized queries.

## Database Schema

### products
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Product name |
| description | TEXT | Product description |
| category | TEXT | Product category |
| released | INTEGER | 1=visible, 0=hidden |
| price | INTEGER | Product price |

### users
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | TEXT | Login username |
| password | TEXT | Login password |
| role | TEXT | User role |

### secret_users
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | TEXT | Secret username |
| password | TEXT | Secret password |

## UI Theme
- **Style:** White traditional academic theme
- **Colors:** White background, dark slate navigation, dark red (#8B0000) accents
- **Fonts:** Georgia/Times New Roman serif for traditional academic feel
- **Layout:** Card-based design with clean tables and code snippets

## Assignment Requirements Met
✅ All 8 PortSwigger SQLi lab types implemented  
✅ Intentionally vulnerable raw SQL (no parameterization)  
✅ SQLite database with realistic seed data  
✅ Clean white traditional UI  
✅ Query execution display for educational transparency  
✅ Side-by-side vulnerable vs safe code comparison  
✅ Safe demo route for defense education  
✅ Detailed vulnerability explanations on each page  

## License
For educational use only. Confidential — Cybersecurity Course Assignment.
