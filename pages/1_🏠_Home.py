import streamlit as st

# Simulate a simple user database with a dictionary for demo purposes
users_db = {}

st.title("Welcome to Cane")

login_col, signup_col = st.columns(2)

# Login Section
with login_col:
    st.subheader("Log In")
    login_username = st.text_input("Login Username", placeholder="Enter your username")
    login_password = st.text_input("Login Password", placeholder="Enter your password", type="password")
    
    if st.button("Log In"):
        if login_username in users_db and users_db[login_username] == login_password:
            st.success(f"Logged in as {login_username}")
        else:
            st.error("Invalid username or password")

# Sign-Up Section
with signup_col:
    st.subheader("Sign Up")
    signup_username = st.text_input("Sign Up Username", placeholder="Create a username")
    signup_password = st.text_input("Sign Up Password", placeholder="Create a password", type="password")
    
    if st.button("Sign Up"):
        if signup_username in users_db:
            st.error("Username already exists. Try logging in.")
        else:
            users_db[signup_username] = signup_password
            st.success(f"Account created for {signup_username}. You can now log in.")
