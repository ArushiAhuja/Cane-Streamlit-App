import streamlit as st
import sqlite3
import hashlib

# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create users table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a new user
def add_user(username, password):
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()

# Function to validate user credentials
def validate_user(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    return c.fetchone() is not None

st.title("User Authentication")

# Registration section
st.subheader("Register")
username_reg = st.text_input("Username (Register)")
password_reg = st.text_input("Password (Register)", type="password")

if st.button("Register"):
    if username_reg and password_reg:
        try:
            add_user(username_reg, password_reg)
            st.success("User registered successfully!")
        except sqlite3.IntegrityError:
            st.error("Username already exists. Please choose a different one.")
    else:
        st.error("Please enter both username and password.")

# Login section
st.subheader("Login")
username_log = st.text_input("Username (Login)")
password_log = st.text_input("Password (Login)", type="password")

if st.button("Login"):
    if validate_user(username_log, password_log):
        st.success("Login successful!")
        # Redirect to main app or perform actions upon successful login
        st.session_state['username'] = username_log  # Store username in session state
        st.write("Welcome, ", username_log)
    else:
        st.error("Invalid username or password.")

conn.close()
