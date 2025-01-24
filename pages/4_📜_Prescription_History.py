import streamlit as st
import hashlib

st.title("Prescription History")


prescriptions = st.session_state.get('prescriptions', [])

if not prescriptions:
    st.write("No prescriptions stored yet.")
else:
    for prescription in prescriptions:
        st.write(f"Prescription Name: {prescription['name']}")
        st.write("Extracted Text:")
        st.text_area("Text", prescription["text"], height=200)
        st.write("Encrypted Text:")
        encrypted_text = hashlib.sha256(prescription["text"].encode()).hexdigest()
        st.code(encrypted_text)
