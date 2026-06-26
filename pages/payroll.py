from pathlib import Path
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import date
from io import BytesIO

# ==================================
# LOGIN CHECK
# ==================================

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()

# ==================================
# LOAD CSS
# ==================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSS_PATH = BASE_DIR / "assets" / "style.css"

if CSS_PATH.exists():
    with open(CSS_PATH) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==================================
# DATABASE
# ==================================
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

# ==================================
# SUMMARY
# ==================================

total_payroll = cur.execute(
    "SELECT COUNT(*) FROM payroll"
).fetchone()[0]

total_salary = cur.execute(
    "SELECT IFNULL(SUM(net_salary),0) FROM payroll"
).fetchone()[0]

average_salary = cur.execute(
    "SELECT IFNULL(AVG(net_salary),0) FROM payroll"
).fetchone()[0]

# ==================================
# HEADER
# ==================================

st.title("💰 Payroll Management")
st.caption("Generate and manage employee payroll.")

st.divider()

# ==================================
# CARDS
# ==================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Payroll Records",
        total_payroll
    )

with c2:
    st.metric(
        "Total Payroll",
        f"Rs {total_salary:,.0f}"
    )

with c3:
    st.metric(
        "Average Salary",
        f"Rs {average_salary:,.0f}"
    )

st.divider()

# ==================================
# GENERATE PAYROLL
# ==================================

st.subheader("🧾 Generate Payroll")

employee_id = st.number_input(
    "Employee ID",
    min_value=1
)

if st.button("Fetch Employee"):

    employee = cur.execute(
        "SELECT * FROM employees WHERE employee_id=?",
        (employee_id,)
    ).fetchone()

    salary = cur.execute(
        "SELECT * FROM salaries WHERE employee_id=?",
        (employee_id,)
    ).fetchone()

    deduction = cur.execute(
        "SELECT * FROM deductions WHERE employee_id=?",
        (employee_id,)
    ).fetchone()

    if employee and salary and deduction:

        st.session_state.emp = employee
        st.session_state.salary = salary
        st.session_state.deduction = deduction

    else:
        st.error("Employee, salary or deduction record missing.")

# ==================================
# SHOW PAYROLL
# ==================================

if "emp" in st.session_state:

    employee = st.session_state.emp
    salary = st.session_state.salary
    deduction = st.session_state.deduction

    gross_salary = salary[5]
    total_deduction = deduction[7]
    net_salary = gross_salary - total_deduction

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Gross Salary",
            f"Rs {gross_salary:,.0f}"
        )

        st.metric(
            "Employee",
            employee[1]
        )

    with c2:
        st.metric(
            "Deduction",
            f"Rs {total_deduction:,.0f}"
        )

        st.metric(
            "Net Salary",
            f"Rs {net_salary:,.0f}"
        )

    pay_date = st.date_input(
        "Pay Date",
        value=date.today()
    )

    if st.button("Generate Payroll"):

        cur.execute(
            """
            INSERT INTO payroll(
            employee_id,
            gross_salary,
            total_deduction,
            net_salary,
            pay_date
            )
            VALUES(?,?,?,?,?)
            """,
            (
                employee[0],
                gross_salary,
                total_deduction,
                net_salary,
                str(pay_date)
            )
        )

        conn.commit()

        st.success("Payroll generated successfully.")

st.divider()

# ==================================
# SEARCH
# ==================================

st.subheader("🔍 Search Payroll")

search = st.number_input(
    "Employee ID",
    min_value=1,
    key="search"
)

if st.button("Search Payroll"):

    data = cur.execute(
        """
        SELECT *
        FROM payroll
        WHERE employee_id=?
        """,
        (search,)
    ).fetchone()

    if data:

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Gross Salary",
                f"Rs {data[2]:,.0f}"
            )

            st.metric(
                "Net Salary",
                f"Rs {data[4]:,.0f}"
            )

        with c2:
            st.metric(
                "Deduction",
                f"Rs {data[3]:,.0f}"
            )

            st.metric(
                "Pay Date",
                data[5]
            )

    else:
        st.error("Payroll not found.")

st.divider()

# ==================================
# DELETE
# ==================================

st.subheader("🗑 Delete Payroll")

delete_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="delete"
)

if st.button("Delete Payroll"):

    cur.execute(
        """
        DELETE FROM payroll
        WHERE employee_id=?
        """,
        (delete_id,)
    )

    conn.commit()

    st.success("Payroll deleted.")

st.divider()

# ==================================
# TABLE
# ==================================

st.subheader("📋 Payroll Records")

records = cur.execute(
    """
    SELECT *
    FROM payroll
    ORDER BY payroll_id DESC
    """
).fetchall()

if records:

    df = pd.DataFrame(
        records,
        columns=[
            "Payroll ID",
            "Employee ID",
            "Gross Salary",
            "Deduction",
            "Net Salary",
            "Pay Date"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    fig = px.bar(
        df,
        x="Employee ID",
        y="Net Salary",
        text="Net Salary",
        title="Net Salary Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False
        )

    st.download_button(
        "📥 Download Payroll Report",
        output.getvalue(),
        "payroll.xlsx"
    )

else:
    st.warning("No payroll records found.")

conn.close()