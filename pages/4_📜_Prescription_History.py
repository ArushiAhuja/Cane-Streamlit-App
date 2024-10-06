import streamlit as st
import hashlib

st.title("Prescription History")

# List previous prescriptions (for demo purposes, these are static)
prescriptions = [
    {"name": "prescription1.png", "text": "Medicine A: 50mg"},
    {"name": "prescription2.jpeg", "text": "Medicine B: 100mg"}
]

for prescription in prescriptions:
    st.image(prescription["name"], caption=prescription["name"])
    st.write("Encrypted Text:")
    
    # Hashing text for encryption (simple encryption demo)
    encrypted_text = hashlib.sha256(prescription["text"].encode()).hexdigest()
    st.code(encrypted_text)
