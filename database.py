import sqlite3
from pathlib import Path


def create_database():

    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "payroll.db"

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # =========================================
    # EMPLOYEES TABLE
    # =========================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees(

        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        age INTEGER,

        gender TEXT,

        department TEXT,

        designation TEXT,

        phone TEXT,

        email TEXT,

        address TEXT,

        emp_type TEXT

    )
    """)

    # =========================================
    # SALARIES TABLE
    # =========================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS salaries(

        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id INTEGER,

        basic_salary REAL,

        allowance REAL,

        bonus REAL,

        gross_salary REAL,

        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)

    )
    """)

    # =========================================
    # DEDUCTIONS TABLE
    # =========================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS deductions(

        deduction_id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id INTEGER,

        income_tax REAL,

        insurance REAL,

        provident_fund REAL,

        loan REAL,

        other REAL,

        total_deduction REAL,

        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)

    )
    """)

    # =========================================
    # PAYROLL TABLE
    # =========================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payroll(

        payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id INTEGER,

        gross_salary REAL,

        total_deduction REAL,

        net_salary REAL,

        pay_date TEXT,

        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)

    )
    """)

    # =========================================
    # PAYMENTS TABLE
    # =========================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments(

        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,

        employee_id INTEGER,

        payment_method TEXT,

        bank_name TEXT,

        transaction_id TEXT,

        payment_status TEXT,

        payment_date TEXT,

        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)

    )
    """)

    # =========================================
    # USERS TABLE
    # =========================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        user_id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT,

        role TEXT

    )
    """)

    # =========================================
    # SETTINGS TABLE
    # =========================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings(

        setting_id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_name TEXT,

        company_logo TEXT,

        currency TEXT,

        tax_rate REAL,

        pf_rate REAL,

        theme TEXT

    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database Created Successfully")


if __name__ == "__main__":
    create_database()