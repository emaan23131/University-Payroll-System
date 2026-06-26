from pathlib import Path
import streamlit as st
import sqlite3
import pandas as pd

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
conn = sqlite3.connect(
    BASE_DIR / "payroll.db",
    check_same_thread=False
)

cur = conn.cursor()

# =====================================
# HEADER
# =====================================

st.title("🧾 Employee Payslip")
st.caption("Generate employee salary slips.")

st.divider()

# =====================================
# SEARCH EMPLOYEE
# =====================================

employee_id = st.number_input(
    "Employee ID",
    min_value=1,
    step=1
)

if st.button("Generate Payslip"):

    employee = cur.execute(
        """
        SELECT *
        FROM employees
        WHERE employee_id=?
        """,
        (employee_id,)
    ).fetchone()

    salary = cur.execute(
        """
        SELECT *
        FROM salaries
        WHERE employee_id=?
        """,
        (employee_id,)
    ).fetchone()

    deduction = cur.execute(
        """
        SELECT *
        FROM deductions
        WHERE employee_id=?
        """,
        (employee_id,)
    ).fetchone()

    payroll = cur.execute(
        """
        SELECT *
        FROM payroll
        WHERE employee_id=?
        ORDER BY payroll_id DESC
        LIMIT 1
        """,
        (employee_id,)
    ).fetchone()

    if employee and salary and deduction and payroll:

        st.success("Payslip Generated Successfully")

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:
            st.info(f"Employee ID: {employee[0]}")
            st.info(f"Name: {employee[1]}")
            st.info(f"Department: {employee[4]}")
            st.info(f"Type: {employee[5]}")

        with c2:
            st.info(f"Email: {employee[2]}")
            st.info(f"Phone: {employee[3]}")
            st.info(f"Pay Date: {payroll[5]}")

        st.markdown("## 💰 Salary Details")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Basic Salary",
                f"Rs {salary[2]:,.0f}"
            )

        with col2:
            st.metric(
                "Allowance",
                f"Rs {salary[3]:,.0f}"
            )

        with col3:
            st.metric(
                "Bonus",
                f"Rs {salary[4]:,.0f}"
            )

        st.markdown("## ➖ Deductions")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Tax",
                f"Rs {deduction[2]:,.0f}"
            )

        with c2:
            st.metric(
                "Insurance",
                f"Rs {deduction[3]:,.0f}"
            )

        with c3:
            st.metric(
                "Loan",
                f"Rs {deduction[5]:,.0f}"
            )

        st.markdown("---")

        st.metric(
            "Net Salary",
            f"Rs {payroll[4]:,.0f}"
        )

        st.success("Payment Status: Paid ✅")

    else:

        st.error(
            "Employee, Salary, Deduction or Payroll record not found."
        )

conn.close()