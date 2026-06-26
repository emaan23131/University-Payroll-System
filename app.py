import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Payroll Management System",
    page_icon="💰",
    layout="wide"
)

# =====================
# LOAD CSS
# =====================

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "assets" / "style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# =====================
# SESSION
# =====================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =====================
# LOGIN SCREEN
# =====================

if not st.session_state.logged_in:

    c1, c2, c3 = st.columns([1,2,1])

    with c2:

        st.markdown("""
        <h1 style='text-align:center'>
        💰 Payroll System
        </h1>

        <h3 style='text-align:center;color:gray'>
        Admin Login
        </h3>
        """, unsafe_allow_html=True)

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login", use_container_width=True):

            if username == "admin" and password == "admin123":

                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()

            else:
                st.error("Invalid Username or Password")

    st.stop()

# =====================
# SIDEBAR
# =====================

st.sidebar.title("💰 Payroll System")

st.sidebar.success(
    f"Welcome {st.session_state.username}"
)

if st.sidebar.button("Logout"):

    st.session_state.clear()
    st.rerun()

# =====================
# HOME PAGE
# =====================

st.title("🏠 Payroll Management System")

st.markdown("""
### Welcome to the University Payroll Software

Select any page from the sidebar.
""")