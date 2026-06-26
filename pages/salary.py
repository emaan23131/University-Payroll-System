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
# SUMMARY DATA
# ==================================

salary_count = cur.execute(
    "SELECT COUNT(*) FROM salaries"
).fetchone()[0]

total_salary = cur.execute(
    "SELECT IFNULL(SUM(gross_salary),0) FROM salaries"
).fetchone()[0]

average_salary = cur.execute(
    "SELECT IFNULL(AVG(gross_salary),0) FROM salaries"
).fetchone()[0]

# ==================================
# HEADER
# ==================================

st.title("💰 Salary Management")
st.caption("Manage employee salaries and payroll.")

st.divider()

# ==================================
# CARDS
# ==================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Salary Records",
        salary_count
    )

with c2:
    st.metric(
        "Total Salary",
        f"Rs {total_salary:,.0f}"
    )

with c3:
    st.metric(
        "Average Salary",
        f"Rs {average_salary:,.0f}"
    )

st.divider()

# ==================================
# ADD SALARY
# ==================================

st.subheader("➕ Add Salary")

col1, col2 = st.columns(2)

with col1:

    employee_id = st.number_input(
        "Employee ID",
        min_value=1
    )

    basic_salary = st.number_input(
        "Basic Salary",
        min_value=0.0
    )

with col2:

    allowance = st.number_input(
        "Allowance",
        min_value=0.0
    )

    bonus = st.number_input(
        "Bonus",
        min_value=0.0
    )

tax = basic_salary * 0.05

gross_salary = (
    basic_salary +
    allowance +
    bonus -
    tax
)

st.metric(
    "Net Salary",
    f"Rs {gross_salary:,.0f}"
)

if st.button("Save Salary"):

    employee = cur.execute(
        """
        SELECT * FROM employees
        WHERE employee_id=?
        """,
        (employee_id,)
    ).fetchone()

    if employee:

        cur.execute(
            """
            INSERT INTO salaries(
            employee_id,
            basic_salary,
            allowance,
            bonus,
            gross_salary
            )
            VALUES(?,?,?,?,?)
            """,
            (
                employee_id,
                basic_salary,
                allowance,
                bonus,
                gross_salary
            )
        )

        conn.commit()

        st.success(
            "Salary Saved Successfully."
        )

    else:
        st.error("Employee not found.")

st.divider()

# ==================================
# SEARCH
# ==================================

st.subheader("🔍 Search Salary")

search_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="search"
)

if st.button("Search Salary"):

    result = cur.execute(
        """
        SELECT * FROM salaries
        WHERE employee_id=?
        """,
        (search_id,)
    ).fetchone()

    if result:

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Basic Salary",
                f"Rs {result[2]:,.0f}"
            )

            st.metric(
                "Allowance",
                f"Rs {result[3]:,.0f}"
            )

        with c2:
            st.metric(
                "Bonus",
                f"Rs {result[4]:,.0f}"
            )

            st.metric(
                "Gross Salary",
                f"Rs {result[5]:,.0f}"
            )

    else:
        st.error("Record not found.")

st.divider()

# ==================================
# UPDATE
# ==================================

st.subheader("✏ Update Salary")

update_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="update"
)

new_basic = st.number_input(
    "New Basic Salary",
    min_value=0.0,
    key="basic"
)

if st.button("Update Salary"):

    cur.execute(
        """
        UPDATE salaries
        SET basic_salary=?
        WHERE employee_id=?
        """,
        (
            new_basic,
            update_id
        )
    )

    conn.commit()

    st.success("Salary Updated")

st.divider()

# ==================================
# DELETE
# ==================================

st.subheader("🗑 Delete Salary")

delete_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="delete"
)

if st.button("Delete Salary"):

    cur.execute(
        """
        DELETE FROM salaries
        WHERE employee_id=?
        """,
        (delete_id,)
    )

    conn.commit()

    st.success("Salary Deleted")

st.divider()

# ==================================
# SALARY TABLE
# ==================================

st.subheader("📋 Salary Records")

data = cur.execute(
    """
    SELECT *
    FROM salaries
    """
).fetchall()

if data:

    df = pd.DataFrame(
        data,
        columns=[
            "Salary ID",
            "Employee ID",
            "Basic Salary",
            "Allowance",
            "Bonus",
            "Gross Salary"
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

    st.info(
        f"Total Records: {len(df)}"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    fig = px.bar(
        df,
        x="Employee ID",
        y="Gross Salary",
        text="Gross Salary",
        title="Salary Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Excel Download

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

    st.download_button(
        "📥 Download Salary Report",
        export_excel(df),
        "salary_report.xlsx"
    )

else:

    st.warning("No salary records found.")

conn.close()