from pathlib import Path
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ==========================
# LOAD CSS
# ==========================


if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()
BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "assets" / "style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================
# DATABASE
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
DB_PATH = BASE_DIR / "payroll.db"

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

cur = conn.cursor()

# ==========================
# COUNTS
# ==========================

employee_count = cur.execute(
    "SELECT COUNT(*) FROM employees"
).fetchone()[0]

salary_count = cur.execute(
    "SELECT COUNT(*) FROM salaries"
).fetchone()[0]

deduction_count = cur.execute(
    "SELECT COUNT(*) FROM deductions"
).fetchone()[0]

payroll_count = cur.execute(
    "SELECT COUNT(*) FROM payroll"
).fetchone()[0]

# ==========================
# HEADER
# ==========================

st.markdown("""
<h1 style='font-size:40px'>
👋 Welcome Back Admin
</h1>

<p style='color:gray;font-size:20px'>
Payroll Management Dashboard
</p>
""", unsafe_allow_html=True)

st.write("")

# ==========================
# CARDS
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card green">
        <h4>Employees</h4>
        <h1>{employee_count}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card blue">
        <h4>Salaries</h4>
        <h1>{salary_count}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card orange">
        <h4>Deductions</h4>
        <h1>{deduction_count}</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card purple">
        <h4>Payroll</h4>
        <h1>{payroll_count}</h1>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================
# CHART
# ==========================

chart_data = pd.DataFrame({
    "Category": [
        "Employees",
        "Salaries",
        "Deductions",
        "Payroll"
    ],
    "Count": [
        employee_count,
        salary_count,
        deduction_count,
        payroll_count
    ]
})

fig = px.bar(
    chart_data,
    x="Category",
    y="Count",
    text="Count",
    title="System Statistics"
)

fig.update_layout(
    height=400,
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# RECENT EMPLOYEES
# ==========================

st.subheader("📋 Recent Employees")

employees = cur.execute("""
SELECT employee_id,
       name,
       department,
       employee_type
FROM employees
ORDER BY employee_id DESC
LIMIT 10
""").fetchall()

if employees:

    df = pd.DataFrame(
        employees,
        columns=[
            "ID",
            "Name",
            "Department",
            "Type"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.warning("No employees found.")

# ==========================
# QUICK INFORMATION
# ==========================

st.subheader("Quick Information")

c1, c2 = st.columns(2)

with c1:
    st.success("""
    ✅ Employee Management

    ✅ Salary Management

    ✅ Payroll Processing

    ✅ Reports
    """)

with c2:
    st.info("""
    📊 Analytics

    📄 Payslips

    💰 Payments

    🏫 University Payroll System
    """)

conn.close()