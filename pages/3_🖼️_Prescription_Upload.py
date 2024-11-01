import streamlit as st
import easyocr
from PIL import Image
import pandas as pd
from gtts import gTTS
import io
import time
import os
from pdf2image import convert_from_path
import pymysql  # For SQL integration
from sqlalchemy import create_engine  # For SQLAlchemy integration
from dotenv import load_dotenv  # For loading environment variables
import hashlib

# Load environment variables for SQL credentials
load_dotenv()

# Set up connection to SQL database
DATABASE_URL = os.getenv("DATABASE_URL")  # Use your database URL
engine = create_engine(DATABASE_URL)

# Initialize session state for prescriptions and username
if 'prescriptions' not in st.session_state:
    st.session_state['prescriptions'] = []
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Title for the page
st.title("Upload and Extract Prescription")

# File uploader for image or multi-page PDF
uploaded_file = st.file_uploader("Upload Prescription (PDF, JPEG, PNG)", type=["pdf", "jpeg", "png"])

# Function to extract text from image
def extract_text_from_image(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    text = ' '.join([res[1] for res in result])
    return text

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    images = convert_from_path(pdf_file)
    for img in images:
        text += extract_text_from_image(img)
    return text

# File processing logic
if uploaded_file is not None:
    try:
        extracted_text = ""
        if uploaded_file.type == "application/pdf":
            st.spinner("Processing PDF...")
            pdf_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            extracted_text = extract_text_from_pdf(pdf_path)
            os.remove(pdf_path)  # Clean up
        else:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Prescription", use_column_width=True)
            st.spinner("Processing image...")
            extracted_text = extract_text_from_image(image)

        if extracted_text.strip() == "":
            st.warning("No text found in the uploaded file.")
        else:
            st.success("Text extraction complete!")
            st.text_area("Extracted Text", extracted_text)
        
        # Text-to-speech conversion
        st.write("Convert extracted text to audio:")
        if st.button("Convert to Audio"):
            tts = gTTS(text=extracted_text, lang='en', slow=False)
            audio_file = io.BytesIO()
            tts.write_to_fp(audio_file)
            st.audio(audio_file, format='audio/mp3')

        # Allow user to name and save prescription
        prescription_name = st.text_input("Enter a name for this prescription:")
        if st.button("Save Prescription"):
            if prescription_name:
                st.session_state['prescriptions'].append({
                    "name": prescription_name,
                    "text": extracted_text,
                    "user": st.session_state['username']
                })
                # Save to SQL table
                with engine.connect() as conn:
                    conn.execute("INSERT INTO prescriptions (user, name, text) VALUES (%s, %s, %s)",
                                 (st.session_state['username'], prescription_name, extracted_text))
                st.success(f"Prescription '{prescription_name}' saved successfully!")
            else:
                st.warning("Please enter a name for the prescription before saving.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.write("Please upload a file to proceed.")
