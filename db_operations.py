import sqlite3

DB = "payroll.db"

def get_connection():
    return sqlite3.connect(DB)