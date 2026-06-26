from database import create_database
import sqlite3

create_database()

conn = sqlite3.connect("payroll.db")
cur = conn.cursor()

# Default Admin
cur.execute("""
INSERT OR IGNORE INTO users(
username,
password,
role
)
VALUES(
'admin',
'admin123',
'Administrator'
)
""")

# Default Company Settings
cur.execute("""
INSERT OR IGNORE INTO settings(
setting_id,
company_name,
company_logo,
currency,
tax_rate,
pf_rate,
theme
)
VALUES(
1,
'ABC Company',
'',
'PKR',
10,
5,
'Mint Green'
)
""")

conn.commit()
conn.close()

print("✅ Setup Completed Successfully")