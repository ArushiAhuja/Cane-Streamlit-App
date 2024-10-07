import streamlit as st

# Initialize users database in session state if not already done
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {}

st.title("Welcome to Cane")

login_col, signup_col = st.columns(2)

# Login Section
with login_col:
    st.subheader("Log In")
    login_username = st.text_input("Login Username", placeholder="Enter your username")
    login_password = st.text_input("Login Password", placeholder="Enter your password", type="password")
    
    if st.button("Log In"):
        # Check if username exists and password is correct
        if login_username in st.session_state['users_db'] and st.session_state['users_db'][login_username] == login_password:
            st.success(f"Logged in as {login_username}")
            st.session_state['logged_in_user'] = login_username  # Save logged in user in session state
        else:
            st.error("Invalid username or password")

# Sign-Up Section
with signup_col:
    st.subheader("Sign Up")
    signup_username = st.text_input("Sign Up Username", placeholder="Create a username")
    signup_password = st.text_input("Sign Up Password", placeholder="Create a password", type="password")
    
    if st.button("Sign Up"):
        # Check if the username already exists
        if signup_username in st.session_state['users_db']:
            st.error("Username already exists. Try logging in.")
        else:
            # Add new user to session state
            st.session_state['users_db'][signup_username] = signup_password
            st.success(f"Account created for {signup_username}. You can now log in.")
