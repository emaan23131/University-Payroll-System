import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from pathlib import Path



if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()
# ==========================
# LOAD CSS
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "assets" / "style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================
# DATABASE
# ==========================

DB_PATH = BASE_DIR / "payroll.db"

conn = sqlite3.connect(DB_PATH)

# ==========================
# LOAD DATA
# ==========================
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
employees = pd.read_sql("SELECT * FROM employees", conn)
salary = pd.read_sql("SELECT * FROM salaries", conn)
deduction = pd.read_sql("SELECT * FROM deductions", conn)
payroll = pd.read_sql("SELECT * FROM payroll", conn)

try:
    payment = pd.read_sql("SELECT * FROM payments", conn)
except:
    payment = pd.DataFrame()

# ==========================
# TITLE
# ==========================

st.title("📊 Analytics Dashboard")
st.markdown("---")

# ==========================
# SUMMARY CARDS
# ==========================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "👨 Employees",
        len(employees)
    )

with c2:
    st.metric(
        "💰 Gross Salary",
        f"Rs {salary['gross_salary'].sum():,.0f}"
        if not salary.empty else "Rs 0"
    )

with c3:
    st.metric(
        "➖ Deductions",
        f"Rs {deduction['total_deduction'].sum():,.0f}"
        if not deduction.empty else "Rs 0"
    )

with c4:
    st.metric(
        "💵 Net Payroll",
        f"Rs {payroll['net_salary'].sum():,.0f}"
        if not payroll.empty else "Rs 0"
    )

with c5:
    st.metric(
        "💳 Payments",
        len(payment)
    )

st.divider()

# ==========================
# CHARTS
# ==========================

left, right = st.columns(2)

with left:

    st.subheader("Employees by Department")

    if not employees.empty:

        dept = (
            employees.groupby("department")
            .size()
            .reset_index(name="Employees")
        )

        fig = px.bar(
            dept,
            x="department",
            y="Employees",
            text="Employees",
            title="Department Statistics"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with right:

    st.subheader("Payment Status")

    if not payment.empty and "payment_status" in payment.columns:

        status = (
            payment.groupby("payment_status")
            .size()
            .reset_index(name="Count")
        )

        fig = px.pie(
            status,
            names="payment_status",
            values="Count",
            hole=0.45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# ==========================
# MONTHLY PAYROLL
# ==========================

st.subheader("Monthly Payroll")

if (
    not payroll.empty
    and "pay_date" in payroll.columns
    and "net_salary" in payroll.columns
):

    payroll["pay_date"] = pd.to_datetime(
        payroll["pay_date"]
    )

    payroll["Month"] = (
        payroll["pay_date"]
        .dt.strftime("%b")
    )

    monthly = (
        payroll.groupby("Month")["net_salary"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Month",
        y="net_salary",
        markers=True,
        title="Monthly Payroll Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================
# TABLES
# ==========================

c1, c2 = st.columns(2)

with c1:

    st.subheader("👨 Recent Employees")

    if not employees.empty:

        st.dataframe(
            employees.tail(5),
            use_container_width=True
        )

with c2:

    st.subheader("💳 Recent Payments")

    if not payment.empty:

        st.dataframe(
            payment.tail(5),
            use_container_width=True
        )

conn.close()