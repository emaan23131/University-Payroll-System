import sqlite3
from pathlib import Path
import streamlit as st

# ==========================
# DATABASE PATH
# ==========================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "payroll.db"


# ==========================
# DATABASE CONNECTION
# ==========================

def get_connection():
    return sqlite3.connect(DB_PATH)


# ==========================
# LOGIN FUNCTION
# ==========================

def login(username, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM users
    WHERE username=?
    AND password=?
    """, (username, password))

    user = cur.fetchone()

    conn.close()

    return user


# ==========================
# CHECK USER EXISTS
# ==========================

def user_exists(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM users
    WHERE username=?
    """, (username,))

    user = cur.fetchone()

    conn.close()

    return user


# ==========================
# CREATE NEW USER
# ==========================

def create_user(username, password, role="Administrator"):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users(
        username,
        password,
        role
    )
    VALUES(?,?,?)
    """, (
        username,
        password,
        role
    ))

    conn.commit()
    conn.close()


# ==========================
# CHECK LOGIN STATUS
# ==========================

def is_logged_in():

    return st.session_state.get("logged_in", False)


# ==========================
# LOGOUT
# ==========================

def logout():

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()


# ==========================
# LOGIN REQUIRED
# ==========================

def login_required():

    if not is_logged_in():

        st.warning("Please Login First")

        st.stop()