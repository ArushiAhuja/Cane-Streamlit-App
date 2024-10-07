import streamlit as st
import pytesseract
import zipfile
import os
from PIL import Image
import io
import time

# Step 1: Path to the Tesseract zip file in your repo
tesseract_zip_path = 'tesseract/tesseract.zip'  # Update this to reflect your directory structure

# Step 2: Define the extraction directory
tesseract_extracted_dir = '/tmp/tesseract'

# Step 3: Extract the zip file if not already extracted
if not os.path.exists(tesseract_extracted_dir):
    st.write("Extracting Tesseract...")
    with zipfile.ZipFile(tesseract_zip_path, 'r') as zip_ref:
        zip_ref.extractall(tesseract_extracted_dir)
    st.success("Tesseract extracted successfully!")

# Step 4: Set the path to the Tesseract executable within the extracted files
tesseract_cmd_path = os.path.join(tesseract_extracted_dir, 'tesseract.exe')  # Update this based on your zip content
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
