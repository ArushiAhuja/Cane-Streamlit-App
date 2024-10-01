import streamlit as st
import os
import pandas as pd
import numpy as np
from PyPDF2 import PdfReader  # For extracting text from PDF
from gtts import gTTS  # Text-to-Speech
from sklearn.feature_extraction.text import CountVectorizer  # For the ML model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import shutil  # For file management

# Define paths for saving user data and prescriptions
user_data_dir = "user_data"
prescriptions_dir = "prescriptions"

# Create directories if they don't exist
os.makedirs(user_data_dir, exist_ok=True)
os.makedirs(prescriptions_dir, exist_ok=True)

# User authentication system (Simple)
users = {}

# Welcome message
st.title("Cane: Medical Prescription Tracker")
st.write("Welcome to Cane, a medical prescription tracker app designed for elders and disabled individuals!")

# Log in or Sign Up
auth_option = st.radio("Choose an option", ["Log In", "Sign Up"])

if auth_option == "Sign Up":
    st.subheader("Create a New Account")
    name = st.text_input("Enter your name")
    mobile = st.text_input("Mobile Number")
    dob = st.date_input("Date of Birth")
    medical_conditions = st.text_area("Medical Conditions/Disabilities")
    allergies = st.text_area("Allergies")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    
    if st.button("Sign Up"):
        # Save user details
        user_info = {"name": name, "mobile": mobile, "dob": str(dob), "medical_conditions": medical_conditions, "allergies": allergies}
        users[username] = {"password": password, "profile": user_info}
        st.success("Account created! Please log in.")
        
elif auth_option == "Log In":
    st.subheader("Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        if username in users and users[username]["password"] == password:
            st.success(f"Welcome back, {users[username]['profile']['name']}!")
            
            # After login: Show dashboard
            st.subheader("Dashboard")
            
            # Option to upload prescription
            if st.button("Upload Prescription"):
                st.info("Please upload your medical prescription in PDF format.")
                prescription_file = st.file_uploader("Choose a PDF", type="pdf")
                
                if prescription_file is not None:
                    # Save the file to user's folder
                    user_folder = os.path.join(prescriptions_dir, username)
                    os.makedirs(user_folder, exist_ok=True)
                    file_path = os.path.join(user_folder, prescription_file.name)
                    with open(file_path, "wb") as f:
                        f.write(prescription_file.read())
                    st.success("Prescription uploaded successfully!")
                    
                    # Extract text from the PDF
                    pdf_reader = PdfReader(file_path)
                    extracted_text = ""
                    for page in pdf_reader.pages:
                        extracted_text += page.extract_text()
                    
                    st.write("Extracted Prescription Text:")
                    st.write(extracted_text)
                    
                    # Convert text to audio
                    if st.button("Convert Prescription to Audio"):
                        tts = gTTS(extracted_text)
                        audio_path = os.path.join(user_folder, "prescription_audio.mp3")
                        tts.save(audio_path)
                        st.audio(audio_path, format='audio/mp3')
                        st.success("Audio version created!")
                    
                    # Notify guardian (Simulated)
                    if st.button("Notify Guardian"):
                        st.write("Notification sent to your guardian!")
                    
                    # ML Model: Identify medicines from prescription
                    st.subheader("Identify Medicines")
                    
                    # Placeholder ML model
                    def train_model():
                        # Sample dataset (to be replaced with a real dataset)
                        data = {
                            "text": ["Take aspirin daily", "Ibuprofen 200mg", "Paracetamol 500mg", "Take ibuprofen twice a day"],
                            "medicine": [1, 1, 1, 1]
                        }
                        df = pd.DataFrame(data)
                        
                        # Text vectorization
                        vectorizer = CountVectorizer()
                        X = vectorizer.fit_transform(df['text'])
                        y = df['medicine']
                        
                        # Train-test split
                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                        
                        # Model training
                        model = LogisticRegression()
                        model.fit(X_train, y_train)
                        
                        return model, vectorizer
                    
                    model, vectorizer = train_model()
                    st.write("Machine Learning model trained to identify medicines.")
                    
                    # Predict medicines in extracted text
                    if st.button("Identify Medicines"):
                        extracted_text_vectorized = vectorizer.transform([extracted_text])
                        prediction = model.predict(extracted_text_vectorized)
                        if prediction == 1:
                            st.success("Medicines identified in the prescription.")
                        else:
                            st.warning("No medicines found in the prescription.")
        
        else:
            st.error("Invalid username or password")

