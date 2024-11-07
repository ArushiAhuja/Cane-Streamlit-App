import streamlit as st
import easyocr
from PIL import Image
import pandas as pd
from gtts import gTTS
import io
import time
import os
from pdf2image import convert_from_path

# Initialize prescription history if not already initialized
if 'prescriptions' not in st.session_state:
    st.session_state['prescriptions'] = []

st.title("Upload and Extract Prescription")

# File uploader for image or PDF (allowing multiple files)
uploaded_files = st.file_uploader("Upload Prescription (PDF, JPEG, PNG)", type=["pdf", "jpeg", "png"], accept_multiple_files=True)

def extract_text_from_image(image):
    """Extract text from a single image using easyocr."""
    reader = easyocr.Reader(['en'])  # Specify the language(s) you want to use
    result = reader.readtext(image)
    text = ' '.join([res[1] for res in result])
    return text

def extract_text_from_pdf(pdf_file):
    """Convert PDF to images and extract text from each image using easyocr."""
    text = ""
    images = convert_from_path(pdf_file)
    for img in images:
        text += extract_text_from_image(img)
    return text

if uploaded_files:
    try:
        extracted_text = ""
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    pdf_path = os.path.join(os.getcwd(), uploaded_file.name)
                    with open(pdf_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    extracted_text += extract_text_from_pdf(pdf_path) + "\n"
                    os.remove(pdf_path)  # Clean up the file after processing
            else:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Uploaded Prescription: {uploaded_file.name}", use_column_width=True)
                with st.spinner(f"Processing image: {uploaded_file.name}..."):
                    extracted_text += extract_text_from_image(image) + "\n"

        if extracted_text.strip() == "":
            st.warning("No text found in the uploaded files.")
        else:
            st.success("Text extraction complete!")
            st.text_area("Extracted Text", extracted_text)
            
            # Audio conversion
            st.write("Convert extracted text to audio:")
            if st.button("Convert to Audio"):
                tts = gTTS(text=extracted_text, lang='en', slow=False)  # Set slow to False for natural pronunciation
                audio_file = io.BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file, format='audio/mp3')
            
            # Input for naming the prescription
            prescription_name = st.text_input("Name your Prescription:", "")
            
            # Text matching using meds.csv
            st.write("Matching extracted text with the medication dataset...")
            meds = pd.read_csv('meds.csv')  # Load the meds dataset
            matched_meds = meds[meds['Name'].apply(lambda x: any(term in extracted_text.split() for term in x.split()))]
            if not matched_meds.empty:
                st.write("Matched Medications:", matched_meds)
            else:
                st.info("No medical terms found in the prescription. Showing the extracted text.")
            
            # Save prescription to history with a name
            if st.button("Save Prescription"):
                if prescription_name.strip() == "":
                    st.warning("Please enter a name for your prescription before saving.")
                else:
                    st.session_state['prescriptions'].append({
                        "name": prescription_name,
                        "text": extracted_text
                    })
                    st.success("Prescription saved successfully!")
    
    except Exception as e:
        st.error(f"An error occurred while processing the files: {e}")
else:
    st.write("Please upload files to proceed.")
