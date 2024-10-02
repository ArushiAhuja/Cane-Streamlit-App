import streamlit as st
import pandas as pd
import easyocr  # Replaced pytesseract with easyocr
from PIL import Image
import re
import csv
import os

# Initialize session state for camera and text extraction
if 'camera_opened' not in st.session_state:
    st.session_state['camera_opened'] = False
if 'captured_image' not in st.session_state:
    st.session_state['captured_image'] = None
if 'extracted_text' not in st.session_state:
    st.session_state['extracted_text'] = None

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

# Function to extract text from images using EasyOCR
def extract_text_from_image(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    text = ' '.join([res[1] for res in result])
    return text

# Function to match extracted text with medicine names in dataset
def identify_medicines_in_text(text):
    medicine_names = meds_data['Name'].values
    matched_medicines = []
    for med in medicine_names:
        if re.search(r'\b' + re.escape(med) + r'\b', text, re.IGNORECASE):
            matched_medicines.append(med)
    return matched_medicines

# Streamlit app layout
st.title("Cane: Prescription Tracker")
st.subheader("Helping you manage prescriptions. Simple, reliable, and designed for everyone.")

st.image("Cane.png", caption="Cane: Your Prescription Manager", use_column_width=True)

# User Authentication: Sign-up or Login
st.sidebar.title("Login or Sign-up")
choice = st.sidebar.selectbox("Choose Action", ["Login", "Sign-up"])

if choice == "Sign-up":
    st.sidebar.subheader("Create a New Account")
    new_user = st.sidebar.text_input("Username")
    new_password = st.sidebar.text_input("Password", type='password')
    
    if st.sidebar.button("Sign Up"):
        if new_user and new_password:
            save_user_data(new_user, new_password)
            st.sidebar.success("Account created! Please login now.")
        else:
            st.sidebar.error("Please provide both username and password.")

if choice == "Login":
    st.sidebar.subheader("Login to Your Account")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    
    if st.sidebar.button("Login"):
        if verify_user(username, password):
            st.sidebar.success("Logged in successfully!")
            
            # Upload prescription
            st.header("Upload Your Prescription Image")
            uploaded_file = st.file_uploader("Upload an image of your prescription", type=["png", "jpg", "jpeg", "pdf"])
            
            # Step 1: Handle the 'Take a Photo' button click
            if st.button("Take a Photo"):
                st.session_state['camera_opened'] = True

            # Step 2: Show the camera if 'camera_opened' is True
            if st.session_state['camera_opened']:
                picture = st.camera_input("Camera Window")
                
                # Step 3: After taking a picture, store it in session state
                if picture:
                    st.session_state['captured_image'] = picture
                    st.session_state['camera_opened'] = False

            # Step 4: If there's a captured image, display it and show extract text button
            if st.session_state['captured_image']:
                image = Image.open(st.session_state['captured_image'])
                st.image(image, caption="Captured Prescription", use_column_width=True)
                
                # Step 5: Extract text button and display the extracted text
                if st.button("Extract Text from Photo"):
                    extracted_text = extract_text_from_image(image)
                    st.session_state['extracted_text'] = extracted_text

            # Step 6: If there's extracted text, display it
            if st.session_state['extracted_text']:
                st.subheader("Extracted Text from Prescription")
                st.write(st.session_state['extracted_text'])
                
                # Identify medicines in the extracted text
                identified_medicines = identify_medicines_in_text(st.session_state['extracted_text'])
                
                st.subheader("Identified Medicines")
                if identified_medicines:
                    st.write(identified_medicines)
                else:
                    st.write("No medicines were identified in the prescription.")

            if uploaded_file:
                # Process uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Prescription", use_column_width=True)

                # Show extract button after uploading the image
                if st.button("Extract Text from Upload"):
                    extracted_text = extract_text_from_image(image)
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
            st.sidebar.error("Invalid username or password.")
