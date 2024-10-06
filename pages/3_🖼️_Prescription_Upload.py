import streamlit as st
import pytesseract
from PIL import Image
import io
import time

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
