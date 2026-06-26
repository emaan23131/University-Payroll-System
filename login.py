import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "assets" / "style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown("""
<h1 style='text-align:center'>
🔐 Payroll Login
</h1>
""", unsafe_allow_html=True)

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    if username == "admin" and password == "admin123":

        st.session_state.logged_in = True
        st.session_state.username = username

        st.switch_page("app.py")

    else:
        st.error("Invalid Username or Password")