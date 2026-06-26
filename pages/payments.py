
import streamlit as st


if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()
with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
from pathlib import Path
import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ===========================
# DATABASE
# ===========================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "payroll.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

st.title("💳 Payment Management")
st.markdown("---")
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
# ===========================
# FETCH PAYROLL
# ===========================

st.subheader("🔍 Fetch Employee Payroll")

employee_id = st.number_input(
    "Employee ID",
    min_value=1,
    step=1
)

if st.button("Fetch Payroll"):

    employee = cur.execute("""
    SELECT * FROM employees
    WHERE employee_id=?
    """,(employee_id,)).fetchone()

    payroll = cur.execute("""
    SELECT * FROM payroll
    WHERE employee_id=?
    ORDER BY payroll_id DESC
    LIMIT 1
    """,(employee_id,)).fetchone()

    if employee is None:

        st.error("Employee Not Found")

    elif payroll is None:

        st.error("Payroll Record Not Found")

    else:

        st.session_state.employee_id = employee_id
        st.session_state.employee_name = employee[1]
        st.session_state.net_salary = payroll[4]

# ===========================
# PAYMENT FORM
# ===========================

if "employee_name" in st.session_state:

    st.success("Employee Found")

    st.write("### Employee Details")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"👤 Name : {st.session_state.employee_name}")

    with col2:
        st.success(f"💰 Net Salary : Rs. {st.session_state.net_salary:,.0f}")

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Bank Transfer",
            "Cash",
            "JazzCash",
            "EasyPaisa"
        ]
    )

    bank_name = st.text_input(
        "Bank Name"
    )

    transaction_id = st.text_input(
        "Transaction ID"
    )

    payment_status = st.selectbox(
        "Payment Status",
        [
            "Paid",
            "Pending"
        ]
    )

    payment_date = st.date_input(
        "Payment Date",
        value=date.today()
    )

    if st.button("💾 Save Payment"):

        cur.execute("""
        INSERT INTO payments(
        employee_id,
        net_salary,
        payment_method,
        bank_name,
        transaction_id,
        payment_status,
        payment_date
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            st.session_state.employee_id,
            st.session_state.net_salary,
            payment_method,
            bank_name,
            transaction_id,
            payment_status,
            str(payment_date)
        ))

        conn.commit()

        st.success("Payment Saved Successfully")

# ===========================
# PAYMENT HISTORY
# ===========================

st.markdown("---")

st.subheader("📋 Payment History")

records = cur.execute("""
SELECT
payment_id,
employee_id,
net_salary,
payment_method,
bank_name,
transaction_id,
payment_status,
payment_date
FROM payments
ORDER BY payment_id DESC
""").fetchall()

if records:

    df = pd.DataFrame(
        records,
        columns=[
            "Payment ID",
            "Employee ID",
            "Net Salary",
            "Method",
            "Bank",
            "Transaction ID",
            "Status",
            "Payment Date"
        ]
    )

    st.dataframe(df, use_container_width=True)

else:

    st.warning("No Payment Records Found")

# ===========================
# DELETE PAYMENT
# ===========================

st.markdown("---")

st.subheader("🗑 Delete Payment")

delete_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="delete_payment"
)

if st.button("Delete Payment"):

    cur.execute("""
    DELETE FROM payments
    WHERE employee_id=?
    """,(delete_id,))

    conn.commit()

    st.success("Payment Deleted Successfully")