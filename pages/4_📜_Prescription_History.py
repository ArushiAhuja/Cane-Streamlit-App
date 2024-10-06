import streamlit as st
import hashlib

st.title("Prescription History")

# Simulate a stored prescription history (replace this with actual saved data)
prescriptions = st.session_state.get('prescriptions', [])

if not prescriptions:
    st.write("No prescriptions stored yet.")
else:
    for prescription in prescriptions:
        st.image(prescription["name"], caption=prescription["name"])
        st.write("Encrypted Text:")
        encrypted_text = hashlib.sha256(prescription["text"].encode()).hexdigest()
        st.code(encrypted_text)
