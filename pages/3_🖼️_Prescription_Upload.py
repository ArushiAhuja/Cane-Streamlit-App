import streamlit as st
import pytesseract
import zipfile
import os
import shutil
from PIL import Image
import io
import time

# Step 1: Path to the Tesseract zip file in your repo
tesseract_zip_path = 'tesseract.zip'  # Update this to the correct path in your repo

# Step 2: Extract the zip file to a temporary directory if not already extracted
tesseract_extracted_dir = '/tmp/tesseract'
if not os.path.exists(tesseract_extracted_dir):
    with zipfile.ZipFile(tesseract_zip_path, 'r') as zip_ref:
        zip_ref.extractall(tesseract_extracted_dir)

# Step 3: Set the Tesseract executable path
tesseract_cmd_path = os.path.join(tesseract_extracted_dir, 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

# Initialize prescription history if not already initialized
if 'prescriptions' not in st.session_state:
    st.session_state['prescriptions'] = []

st.title("Upload and Extract Prescription")

# File uploader for image or PDF
uploaded_file = st.file_uploader("Upload Prescription (PDF, JPEG, PNG)", type=["pdf", "jpeg", "png"])

if uploaded_file is not None:
    # Show uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Prescription", use_column_width=True)

    # Extract text from prescription
    st.write("Extracting text...")
    with st.spinner("Processing..."):
        time.sleep(2)  # Simulate processing time
        extracted_text = pytesseract.image_to_string(image)
        st.success("Text extraction complete!")
        st.text_area("Extracted Text", extracted_text)

    # Add a Save button to store the prescription to history
    if st.button("Save Prescription"):
        st.session_state['prescriptions'].append({
            "name": uploaded_file.name,
            "text": extracted_text
        })
        st.success("Prescription saved successfully!")
else:
    st.write("Please upload a file to proceed.")
