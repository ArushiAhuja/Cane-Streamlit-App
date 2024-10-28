import streamlit as st
from PIL import Image
import pytesseract
import pdf2image
import os

# Ensure pytesseract can find the tesseract executable
pytesseract.pytesseract.tesseract_cmd = os.path.join(os.path.dirname(__file__), 'tesseract.exe')

def process_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text

def process_pdf(pdf_file):
    images = pdf2image.convert_from_path(pdf_file)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def main():
    st.title("File Upload and OCR")
    st.write("Upload an image or PDF file to extract text.")

    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf"])

    if uploaded_file is not None:
        file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
        st.write(file_details)

        if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
            text = process_image(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            text = process_pdf(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return

        st.write("Extracted Text:")
        st.write(text)

if __name__ == "__main__":
    main()
