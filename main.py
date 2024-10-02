import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import re
import csv
import os
import time  # For adding the loading indicator

# Load medicine dataset
meds_data = pd.read_csv('meds.csv')

# Function to save user data to CSV
def save_user_data(username, password):
    if not os.path.exists('users.csv'):
        with open('users.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Password'])
            writer.writerow([username, password])
    else:
        with open('users.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, password])

# Function to verify user login
def verify_user(username, password):
    if not os.path.exists('users.csv'):
        return False
    with open('users.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Username'] == username and row['Password'] == password:
                return True
    return False

# Function to extract text from images
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to match extracted text with medicine names in dataset
def identify_medicines_in_text(text):
    medicine_names = meds_data['Name'].values
    matched_medicines = []
    for med in medicine_names:
        if re.search(r'\b' + re.escape(med) + r'\b', text, re.IGNORECASE):
            matched_medicines.append(med)
    return matched_medicines

# Main App Code
st.title("Cane: Medical Prescription Tracker")

st.markdown("""
**Welcome to Cane!** This app helps elders and disabled individuals track their medical prescriptions easily. 
Upload a prescription image or take a picture, and the app will extract the text and identify the medicines for you.
""")

# Adding the logo
logo_path = 'Cane.png'
if os.path.exists(logo_path):
    st.image(logo_path, caption="Cane Logo", use_column_width=True)
else:
    st.write("Logo not found! Make sure 'cane_logo.png' is in the correct folder.")

# User Authentication: Sign-up or Login
st.sidebar.title("Login/Sign-up")
choice = st.sidebar.selectbox("Login or Sign-up", ["Login", "Sign-up"])

if choice == "Sign-up":
    st.sidebar.subheader("Create an Account")
    new_user = st.sidebar.text_input("Username")
    new_password = st.sidebar.text_input("Password", type='password')
    
    if st.sidebar.button("Sign Up"):
        save_user_data(new_user, new_password)
        st.sidebar.success("Account created successfully! Please login.")

if choice == "Login":
    st.sidebar.subheader("Login to Your Account")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')

    if st.sidebar.button("Login"):
        if verify_user(username, password):
            st.sidebar.success("Logged in successfully!")
            
            # Upload prescription
            st.header("Upload Your Prescription")
            uploaded_file = st.file_uploader("Upload a prescription image", type=["png", "jpg", "jpeg"])

            if uploaded_file is not None:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Prescription", use_column_width=True)

                # Button to extract text
                if st.button("Extract Text"):
                    with st.spinner("Extracting text, please wait..."):
                        time.sleep(2)  # Simulate the processing time
                        extracted_text = extract_text_from_image(image)
                    
                    st.subheader("Extracted Text from Prescription")
                    st.write(extracted_text)
                    
                    # Identify medicines
                    identified_medicines = identify_medicines_in_text(extracted_text)
                    st.subheader("Identified Medicines")
                    if identified_medicines:
                        st.write(identified_medicines)
                    else:
                        st.write("No medicines were identified in the prescription.")
        else:
            st.sidebar.error("Invalid Username or Password")