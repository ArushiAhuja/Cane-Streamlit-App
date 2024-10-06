import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
from gtts import gTTS
import io
import time

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
    matched_meds = meds[meds['Name'].isin(extracted_text.split())]
    st.write("Matched Medications:", matched_meds)
else:
    st.write("Please upload a file to proceed.")
