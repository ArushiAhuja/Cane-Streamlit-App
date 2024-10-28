import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
from gtts import gTTS
import io
import time
import os

# Set the Tesseract path
tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Initialize prescription history if not already initialized
if 'prescriptions' not in st.session_state:
    st.session_state['prescriptions'] = []

st.title("Upload and Extract Prescription")

# File uploader for image or PDF
uploaded_file = st.file_uploader("Upload Prescription (PDF, JPEG, PNG)", type=["pdf", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Show uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Prescription", use_column_width=True)
        
        # Extract text from prescription
        st.write("Extracting text...")
        with st.spinner("Processing..."):
            time.sleep(2)  # Simulate processing time
            extracted_text = pytesseract.image_to_string(image)
            if extracted_text.strip() == "":
                st.warning("No text found in the uploaded image.")
            else:
                st.success("Text extraction complete!")
                st.text_area("Extracted Text", extracted_text)
        
        # Audio conversion
        st.write("Convert extracted text to audio:")
        if st.button("Convert to Audio"):
            tts = gTTS(text=extracted_text, lang='en')
            audio_file = io.BytesIO()
            tts.write_to_fp(audio_file)
            st.audio(audio_file, format='audio/mp3')
        
        # Text matching using meds.csv
        st.write("Matching extracted text with the medication dataset...")
        meds = pd.read_csv('meds.csv')  # Load the meds dataset
        # Check if any words from the extracted text match the meds dataset
        matched_meds = meds[meds['Name'].apply(lambda x: any(term in extracted_text.split() for term in x.split()))]
        if not matched_meds.empty:
            st.write("Matched Medications:", matched_meds)
        else:
            st.info("No medical terms found in the prescription. Showing the extracted text.")
        
        # Save prescription to history
        if st.button("Save Prescription"):
            st.session_state['prescriptions'].append({
                "name": uploaded_file.name,
                "text": extracted_text
            })
            st.success("Prescription saved successfully!")
    
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.write("Please upload a file to proceed.")
