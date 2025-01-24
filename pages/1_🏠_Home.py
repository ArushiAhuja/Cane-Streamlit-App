import streamlit as st


if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {}

if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None

st.title("Welcome to Cane")

login_col, signup_col = st.columns(2)


def log_out():
    st.session_state['logged_in_user'] = None
    st.success("Logged out successfully.")


if st.session_state['logged_in_user']:
    st.write(f"Logged in as {st.session_state['logged_in_user']}")
    if st.button("Log Out"):
        log_out()
else:
    
    with login_col:
        st.subheader("Log In")
        login_username = st.text_input("Login Username", placeholder="Enter your username")
        login_password = st.text_input("Login Password", placeholder="Enter your password", type="password")
        
        if st.button("Log In"):
            if login_username in st.session_state['users_db'] and st.session_state['users_db'][login_username] == login_password:
                st.success(f"Logged in as {login_username}")
                st.session_state['logged_in_user'] = login_username  # Save logged in user in session state
            else:
                st.error("Invalid username or password")

   
    with signup_col:
        st.subheader("Sign Up")
        signup_username = st.text_input("Sign Up Username", placeholder="Create a username")
        signup_password = st.text_input("Sign Up Password", placeholder="Create a password", type="password")
        
        if st.button("Sign Up"):
            if signup_username in st.session_state['users_db']:
                st.error("Username already exists. Try logging in.")
            else:
                
                st.session_state['users_db'][signup_username] = signup_password
                st.success(f"Account created for {signup_username}. You can now log in.")
