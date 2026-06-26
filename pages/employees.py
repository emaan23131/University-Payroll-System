
import streamlit as st
import sqlite3
import pandas as pd


if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    st.stop()
# ----------------------
# LOGIN CHECK
# ----------------------

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ----------------------
# PAGE CONFIG
# ----------------------

st.set_page_config(
    page_title="Employee Management",
    page_icon="👨‍💼",
    layout="wide"
)

# ----------------------
# LOAD CSS
# ----------------------

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ----------------------
# DATABASE
# ----------------------
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
    "payroll.db",
    check_same_thread=False
)

cur = conn.cursor()

# ----------------------
# COUNTS
# ----------------------

total_emp = cur.execute(
    "SELECT COUNT(*) FROM employees"
).fetchone()[0]

faculty = cur.execute(
    "SELECT COUNT(*) FROM employees WHERE employee_type='Faculty'"
).fetchone()[0]

staff = cur.execute(
    "SELECT COUNT(*) FROM employees WHERE employee_type='Staff'"
).fetchone()[0]

# ----------------------
# HEADER
# ----------------------

st.markdown("""
<h1 style='font-size:40px'>
👨‍💼 Employee Management
</h1>

<p style='color:gray;font-size:18px'>
Manage all employees and departments.
</p>
""", unsafe_allow_html=True)

st.write("")

# ----------------------
# CARDS
# ----------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card green">
    <h4>Total Employees</h4>
    <h1>{total_emp}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card blue">
    <h4>Faculty</h4>
    <h1>{faculty}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card purple">
    <h4>Staff</h4>
    <h1>{staff}</h1>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------------
# ADD EMPLOYEE
# ----------------------

st.markdown("## ➕ Add New Employee")

col1, col2 = st.columns(2)

with col1:

    emp_id = st.number_input(
        "Employee ID",
        min_value=1,
        step=1
    )

    name = st.text_input(
        "Employee Name"
    )

    email = st.text_input(
        "Email"
    )

with col2:

    phone = st.text_input(
        "Phone"
    )

    department = st.text_input(
        "Department"
    )

    emp_type = st.selectbox(
        "Employee Type",
        ["Faculty", "Staff"]
    )

if st.button("Add Employee"):

    try:

        cur.execute("""
        INSERT INTO employees(
        employee_id,
        name,
        email,
        phone,
        department,
        employee_type
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            emp_id,
            name,
            email,
            phone,
            department,
            emp_type
        ))

        conn.commit()

        st.success("✅ Employee Added Successfully")

    except Exception as e:
        st.error(e)

st.divider()

# ----------------------
# SEARCH
# ----------------------

st.markdown("## 🔍 Search Employee")

search_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="search"
)

if st.button("Search"):

    employee = cur.execute("""
    SELECT * FROM employees
    WHERE employee_id=?
    """,
    (search_id,)
    ).fetchone()

    if employee:

        st.success("Employee Found")

        st.write({
            "ID": employee[0],
            "Name": employee[1],
            "Email": employee[2],
            "Phone": employee[3],
            "Department": employee[4],
            "Type": employee[5]
        })

    else:

        st.error("Employee Not Found")

st.divider()

# ----------------------
# UPDATE
# ----------------------

st.markdown("## ✏ Update Department")

update_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="update"
)

new_department = st.text_input(
    "New Department"
)

if st.button("Update Employee"):

    cur.execute("""
    UPDATE employees
    SET department=?
    WHERE employee_id=?
    """,
    (
        new_department,
        update_id
    ))

    conn.commit()

    st.success("Department Updated")

st.divider()

# ----------------------
# DELETE
# ----------------------

st.markdown("## 🗑 Delete Employee")

delete_id = st.number_input(
    "Employee ID",
    min_value=1,
    key="delete"
)

if st.button("Delete Employee"):

    cur.execute("""
    DELETE FROM employees
    WHERE employee_id=?
    """,
    (delete_id,)
    )

    conn.commit()

    st.success("Employee Deleted")

st.divider()

# ----------------------
# EMPLOYEE TABLE
# ----------------------

st.markdown("## 📋 Employee Records")

data = cur.execute("""
SELECT employee_id,
       name,
       email,
       phone,
       department,
       employee_type
FROM employees
""").fetchall()

if data:

    df = pd.DataFrame(
        data,
        columns=[
            "Employee ID",
            "Name",
            "Email",
            "Phone",
            "Department",
            "Type"
        ]
    )

    search = st.text_input(
        "Search Employee Name"
    )

    if search:

        df = df[
            df["Name"].str.contains(
                search,
                case=False
            )
        ]

    st.info(
        f"Total Employees: {len(df)}"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.warning(
        "No Employees Found"
    )