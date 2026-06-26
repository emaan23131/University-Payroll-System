import sqlite3

conn = sqlite3.connect("payroll.db")
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cur.fetchall()

print("Tables in Database:")

for table in tables:
    print(table)

conn.close()