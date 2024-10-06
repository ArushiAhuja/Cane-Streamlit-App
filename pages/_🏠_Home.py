import streamlit as st

st.title("Welcome to Cane")

st.write("A vibrant and intuitive home screen designed for elders and disabled individuals.")
st.write("Please log in or sign up to get started.")

login_col, signup_col = st.columns(2)

with login_col:
    st.subheader("Log In")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")
    if st.button("Log In"):
        st.write(f"Logged in as {username}")

with signup_col:
    st.subheader("Sign Up")
    st.write("New here? Create an account to start using Cane.")
    if st.button("Sign Up"):
        st.write("Redirecting to sign-up page...")
