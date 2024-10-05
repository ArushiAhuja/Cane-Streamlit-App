import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import re
import csv
import os
import time

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
    return pytesseract.image_to_string(image)

# Function to match extracted text with medicine names in dataset
def identify_medicines_in_text(text):
    medicine_names = meds_data['Name'].values
    matched_medicines = [med for med in medicine_names if re.search(r'\b' + re.escape(med) + r'\b', text, re.IGNORECASE)]
    return matched_medicines

# Function to save prescription data for the user
def save_prescription(username, extracted_text):
    if not os.path.exists('prescriptions.csv'):
        with open('prescriptions.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'PrescriptionText'])
            writer.writerow([username, extracted_text])
    else:
        with open('prescriptions.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, extracted_text])

# Function to retrieve previous prescriptions for a user
def get_previous_prescriptions(username):
    if not os.path.exists('prescriptions.csv'):
        return []
    prescriptions = []
    with open('prescriptions.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Username'] == username:
                prescriptions.append(row['PrescriptionText'])
    return prescriptions

# Streamlit app layout
st.title("Cane: Medical Prescription Tracker")

st.markdown("""
**Welcome to Cane!** Upload or take a photo of your prescription, extract the text, and track your medications. 
""")

logo_path = "Cane.png"  # Ensure this file is uploaded to your GitHub repository
if os.path.exists(logo_path):
    st.image(logo_path, caption="Cane Logo")

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

            # Maintain image upload and extraction state
            if 'image' not in st.session_state:
                st.session_state['image'] = None
            if 'extracted_text' not in st.session_state:
                st.session_state['extracted_text'] = ""

            # Display previous prescriptions
            st.header("Previous Prescriptions")
            previous_prescriptions = get_previous_prescriptions(username)
            if previous_prescriptions:
                for idx, prescription in enumerate(previous_prescriptions, start=1):
                    st.subheader(f"Prescription {idx}")
                    st.text(prescription)
            else:
                st.write("No previous prescriptions found.")

            # Extract Text button is visible immediately
            st.header("Upload or Take a Picture of Your Prescription")
            
            st.markdown("### Step 1: Upload an image or take a photo")
            uploaded_file = st.file_uploader("Upload an image (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])
            camera_image = st.camera_input("Take a picture of your prescription")

            if uploaded_file:
                st.session_state['image'] = Image.open(uploaded_file)
                st.image(st.session_state['image'], caption="Uploaded Prescription", use_column_width=True)
            elif camera_image:
                st.session_state['image'] = Image.open(camera_image)
                st.image(st.session_state['image'], caption="Captured Prescription", use_column_width=True)

            # Extract Text button (always visible)
            if st.button("Extract Text"):
                if st.session_state['image']:
                    # Simulate loading with a spinner
                    with st.spinner("Extracting text, please wait..."):
                        time.sleep(2)  # Simulate delay for text extraction
                        st.session_state['extracted_text'] = extract_text_from_image(st.session_state['image'])
                    st.success("Text extraction complete!")

            # Show extracted text in a text area (editable)
            if st.session_state['extracted_text']:
                st.subheader("Extracted Text (You can edit it)")
                edited_text = st.text_area("Edit the extracted text:", st.session_state['extracted_text'])

                # Save the extracted and edited text
                if st.button("Save Prescription"):
                    save_prescription(username, edited_text)
                    st.success("Prescription saved successfully!")
                    
                # Identify medicines in the extracted text
                st.subheader("Identified Medicines")
                identified_medicines = identify_medicines_in_text(edited_text)
                if identified_medicines:
                    st.write(identified_medicines)
                else:
                    st.write("No medicines identified in the prescription.")
        else:
            st.sidebar.error("Invalid Username or Password")
