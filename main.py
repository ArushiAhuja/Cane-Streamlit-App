import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import re
import csv
import os
import time  # To simulate loading

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
    # Use Tesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    return text

# Function to match extracted text with medicine names in dataset
def identify_medicines_in_text(text):
    # Extract medicine names from the dataset
    medicine_names = meds_data['Name'].values
    matched_medicines = []
    
    # Search for each medicine name in the extracted text
    for med in medicine_names:
        if re.search(r'\b' + re.escape(med) + r'\b', text, re.IGNORECASE):
            matched_medicines.append(med)
    
    return matched_medicines

# Streamlit app layout
st.title("Cane: Medical Prescription Tracker")

# Add description text
st.markdown("""
**Welcome to Cane!** This app helps elders and disabled individuals track their medical prescriptions easily. 
Upload a prescription image or take a picture, and the app will extract the text and identify the medicines for you.
""")

# Add logo
logo_path = "Cane.png"  # Ensure this file is uploaded to your GitHub repository
if os.path.exists(logo_path):
    st.image(logo_path, caption="Cane Logo")

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
            uploaded_file = st.file_uploader("Upload a prescription image (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])
            
            # Option to take a picture using the webcam
            st.header("Or Take a Picture")
            camera_image = st.camera_input("Take a picture of your prescription")

            image = None  # Placeholder for the image
            
            # If either file uploaded or camera image is taken
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Prescription Image", use_column_width=True)
            elif camera_image:
                image = Image.open(camera_image)
                st.image(image, caption="Captured Prescription Image", use_column_width=True)
            
            # Show "Extract Text" button only if an image is available
            if image is not None:
                extract_button = st.button("Extract Text")

                # Handle text extraction on button click
                if extract_button:
                    with st.spinner("Processing the image and extracting text..."):
                        time.sleep(2)  # Simulate a delay for loading
                        extracted_text = extract_text_from_image(image)
                    
                    st.success("Text extraction complete!")
                    
                    # Display extracted text
                    st.subheader("Extracted Text from Prescription")
                    st.write(extracted_text)
                    
                    # Identify medicines in the extracted text
                    identified_medicines = identify_medicines_in_text(extracted_text)
                    
                    st.subheader("Identified Medicines")
                    if identified_medicines:
                        st.write(identified_medicines)
                    else:
                        st.write("No medicines were identified in the prescription.")
        else:
            st.sidebar.error("Invalid Username or Password")