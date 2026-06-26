from pathlib import Path
import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

# =====================================
# LOGIN CHECK
# =====================================

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()

# =====================================
# LOAD CSS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSS_PATH = BASE_DIR / "assets" / "style.css"

if CSS_PATH.exists():
    with open(CSS_PATH) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# =====================================
# DATABASE
# =====================================
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=100
)

st.sidebar.title("Payroll System")

st.sidebar.success(
    f"Welcome {st.session_state.username}"
)

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.switch_page("app.py")
DB_PATH = BASE_DIR / "payroll.db"

conn = sqlite3.connect(DB_PATH)

# =====================================
# LOAD DATA
# =====================================

employees = pd.read_sql(
    "SELECT * FROM employees",
    conn
)

salaries = pd.read_sql(
    "SELECT * FROM salaries",
    conn
)

deductions = pd.read_sql(
    "SELECT * FROM deductions",
    conn
)

payroll = pd.read_sql(
    "SELECT * FROM payroll",
    conn
)

try:
    payments = pd.read_sql(
        "SELECT * FROM payments",
        conn
    )
except:
    payments = pd.DataFrame()

# =====================================
# TITLE
# =====================================

st.markdown("""
<h1 style='font-size:40px'>
📊 Reports Dashboard
</h1>

<p style='color:gray;font-size:18px'>
Payroll Reports & Export Center
</p>
""", unsafe_allow_html=True)

st.divider()

# =====================================
# SUMMARY CARDS
# =====================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Employees",
        len(employees)
    )

with c2:
    st.metric(
        "Payroll",
        f"Rs {payroll['net_salary'].sum():,.0f}"
        if not payroll.empty else "Rs 0"
    )

with c3:
    st.metric(
        "Gross Salary",
        f"Rs {salaries['gross_salary'].sum():,.0f}"
        if not salaries.empty else "Rs 0"
    )

with c4:
    st.metric(
        "Deductions",
        f"Rs {deductions['total_deduction'].sum():,.0f}"
        if not deductions.empty else "Rs 0"
    )

with c5:
    st.metric(
        "Payments",
        len(payments)
    )

st.divider()

# =====================================
# FILTERS
# =====================================

st.subheader("🔍 Search Reports")

search = st.text_input(
    "Search Employee Name"
)

if not employees.empty:

    departments = ["All"] + sorted(
        employees["department"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_department = st.selectbox(
        "Department",
        departments
    )

    if search:

        employees = employees[
            employees["name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if selected_department != "All":

        employees = employees[
            employees["department"]
            == selected_department
        ]

st.divider()

# =====================================
# EXPORT FUNCTION
# =====================================

def export_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False
        )

    return output.getvalue()

# =====================================
# EMPLOYEE REPORT
# =====================================

st.subheader("👨 Employee Report")

if not employees.empty:

    st.info(
        f"Total Employees: {len(employees)}"
    )

    st.dataframe(
        employees,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Employee Report",
        export_excel(employees),
        "employees.xlsx"
    )

else:
    st.warning("No Employee Data")

st.divider()

# =====================================
# SALARY REPORT
# =====================================

st.subheader("💰 Salary Report")

if not salaries.empty:

    st.dataframe(
        salaries,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Salary Report",
        export_excel(salaries),
        "salary.xlsx"
    )

else:
    st.warning("No Salary Data")

st.divider()

# =====================================
# DEDUCTION REPORT
# =====================================

st.subheader("➖ Deduction Report")

if not deductions.empty:

    st.dataframe(
        deductions,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Deduction Report",
        export_excel(deductions),
        "deductions.xlsx"
    )

else:
    st.warning("No Deduction Data")

st.divider()

# =====================================
# PAYROLL REPORT
# =====================================

st.subheader("🧾 Payroll Report")

if not payroll.empty:

    st.dataframe(
        payroll,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Payroll Report",
        export_excel(payroll),
        "payroll.xlsx"
    )

else:
    st.warning("No Payroll Data")

st.divider()

# =====================================
# PAYMENT REPORT
# =====================================

if not payments.empty:

    st.subheader("💳 Payment Report")

    st.dataframe(
        payments,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Payment Report",
        export_excel(payments),
        "payments.xlsx"
    )

st.divider()

# =====================================
# FOOTER
# =====================================

st.markdown("""
---
<center>
University Payroll Management System<br>
Professional Reporting Module
</center>
""", unsafe_allow_html=True)

conn.close()