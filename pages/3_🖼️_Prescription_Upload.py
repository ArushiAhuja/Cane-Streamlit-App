import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
from gtts import gTTS
import io
import time
import os
from pdf2image import convert_from_path
import fitz  # PyMuPDF

# Set the Tesseract path
tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Initialize prescription history if not already initialized
if 'prescriptions' not in st.session_state:
    st.session_state['prescriptions'] = []

st.title("Upload and Extract Prescription")

# File uploader for image or PDF
uploaded_file = st.file_uploader("Upload Prescription (PDF, JPEG, PNG)", type=["pdf", "jpeg", "png"])

def extract_text_from_image(image):
    """Extract text from a single image."""
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_file):
    """Convert PDF to images and extract text from each image."""
    text = ""
    images = convert_from_path(pdf_file)
    for img in images:
        text += extract_text_from_image(img)
    return text

if uploaded_file is not None:
    try:
        extracted_text = ""
        if uploaded_file.type == "application/pdf":
            with st.spinner("Processing PDF..."):
                time.sleep(2)  # Simulate processing time
                pdf_path = os.path.join(os.getcwd(), uploaded_file.name)
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                extracted_text = extract_text_from_pdf(pdf_path)
                os.remove(pdf_path)  # Clean up the file after processing
        else:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Prescription", use_column_width=True)
            with st.spinner("Processing image..."):
                time.sleep(2)  # Simulate processing time
                extracted_text = extract_text_from_image(image)

        if extracted_text.strip() == "":
            st.warning("No text found in the uploaded file.")
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
