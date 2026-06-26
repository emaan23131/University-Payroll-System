from pathlib import Path
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
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
# ==================================
# DATABASE
# ==================================

conn = sqlite3.connect(
    BASE_DIR / "payroll.db",
    check_same_thread=False
)

cur = conn.cursor()

# ==================================
# SUMMARY
# ==================================

total_records = cur.execute(
    "SELECT COUNT(*) FROM deductions"
).fetchone()[0]

total_deduction = cur.execute(
    "SELECT IFNULL(SUM(total_deduction),0) FROM deductions"
).fetchone()[0]

average_deduction = cur.execute(
    "SELECT IFNULL(AVG(total_deduction),0) FROM deductions"
).fetchone()[0]

# ==================================
# HEADER
# ==================================

st.title("➖ Deductions Management")
st.caption("Manage taxes and employee deductions.")

st.divider()

# ==================================
# CARDS
# ==================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Records",
        total_records
    )

with c2:
    st.metric(
        "Total Deductions",
        f"Rs {total_deduction:,.0f}"
    )

with c3:
    st.metric(
        "Average Deduction",
        f"Rs {average_deduction:,.0f}"
    )

st.divider()

# ==================================
# ADD DEDUCTION
# ==================================

st.subheader("➕ Add Deduction")

col1, col2 = st.columns(2)

with col1:

    employee_id = st.number_input(
        "Employee ID",
        min_value=1
    )

    income_tax = st.number_input(
        "Income Tax",
        min_value=0.0
    )

    insurance = st.number_input(
        "Insurance",
        min_value=0.0
    )

with col2:

    provident_fund = st.number_input(
        "Provident Fund",
        min_value=0.0
    )

    loan = st.number_input(
        "Loan Deduction",
        min_value=0.0
    )

    other = st.number_input(
        "Other Deduction",
        min_value=0.0
    )

total = (
    income_tax +
    insurance +
    provident_fund +
    loan +
    other
)

st.metric(
    "Total Deduction",
    f"Rs {total:,.0f}"
)

if st.button("Save Deduction"):

    emp = cur.execute(
        "SELECT * FROM employees WHERE employee_id=?",
        (employee_id,)
    ).fetchone()

    if emp:

        cur.execute("""
        INSERT INTO deductions(
        employee_id,
        income_tax,
        insurance,
        provident_fund,
        loan,
        other,
        total_deduction
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            employee_id,
            income_tax,
            insurance,
            provident_fund,
            loan,
            other,
            total
        ))

        conn.commit()

        st.success("Deduction saved successfully.")

    else:
        st.error("Employee not found.")

st.divider()

# ==================================
# SEARCH
# ==================================

st.subheader("🔍 Search Deduction")

search_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="search"
)

if st.button("Search"):

    record = cur.execute(
        """
        SELECT *
        FROM deductions
        WHERE employee_id=?
        """,
        (search_id,)
    ).fetchone()

    if record:

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Income Tax",
                f"Rs {record[2]:,.0f}"
            )

            st.metric(
                "Insurance",
                f"Rs {record[3]:,.0f}"
            )

            st.metric(
                "Provident Fund",
                f"Rs {record[4]:,.0f}"
            )

        with c2:
            st.metric(
                "Loan",
                f"Rs {record[5]:,.0f}"
            )

            st.metric(
                "Other",
                f"Rs {record[6]:,.0f}"
            )

            st.metric(
                "Total",
                f"Rs {record[7]:,.0f}"
            )

    else:
        st.error("Record not found.")

st.divider()

# ==================================
# UPDATE
# ==================================

st.subheader("✏ Update Deduction")

update_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="update"
)

new_tax = st.number_input(
    "Income Tax",
    min_value=0.0,
    key="tax"
)

new_insurance = st.number_input(
    "Insurance",
    min_value=0.0,
    key="ins"
)

new_pf = st.number_input(
    "Provident Fund",
    min_value=0.0,
    key="pf"
)

new_loan = st.number_input(
    "Loan",
    min_value=0.0,
    key="loan"
)

new_other = st.number_input(
    "Other",
    min_value=0.0,
    key="other"
)

new_total = (
    new_tax +
    new_insurance +
    new_pf +
    new_loan +
    new_other
)

if st.button("Update"):

    cur.execute("""
    UPDATE deductions
    SET
    income_tax=?,
    insurance=?,
    provident_fund=?,
    loan=?,
    other=?,
    total_deduction=?
    WHERE employee_id=?
    """,
    (
        new_tax,
        new_insurance,
        new_pf,
        new_loan,
        new_other,
        new_total,
        update_id
    ))

    conn.commit()

    st.success("Record updated.")

st.divider()

# ==================================
# DELETE
# ==================================

st.subheader("🗑 Delete Deduction")

delete_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="delete"
)

if st.button("Delete"):

    cur.execute(
        "DELETE FROM deductions WHERE employee_id=?",
        (delete_id,)
    )

    conn.commit()

    st.success("Record deleted.")

st.divider()

# ==================================
# RECORDS
# ==================================

st.subheader("📋 Deduction Records")

records = cur.execute(
    "SELECT * FROM deductions"
).fetchall()

if records:

    df = pd.DataFrame(
        records,
        columns=[
            "Deduction ID",
            "Employee ID",
            "Income Tax",
            "Insurance",
            "Provident Fund",
            "Loan",
            "Other",
            "Total Deduction"
        ]
    )

    search = st.text_input(
        "Search Employee ID"
    )

    if search:

        df = df[
            df["Employee ID"]
            .astype(str)
            .str.contains(search)
        ]

    st.dataframe(
        df,
        use_container_width=True
    )

    fig = px.bar(
        df,
        x="Employee ID",
        y="Total Deduction",
        text="Total Deduction",
        title="Employee Deduction Analysis"
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
        "📥 Download Excel Report",
        output.getvalue(),
        "deductions.xlsx"
    )

else:

    st.warning("No deduction records found.")

conn.close()