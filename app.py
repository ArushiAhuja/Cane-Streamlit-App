import streamlit as st

st.set_page_config(page_title="Cane", page_icon="💊", layout="centered")

st.title("Cane: A Medical Prescription Tracker")
st.markdown("Welcome to Cane, an intuitive app designed to help elders and disabled individuals easily track their prescriptions.")

st.image("Cane.png", width=250)  # Make sure to add your logo image in the directory
st.sidebar.success("Use the sidebar to navigate between the pages.")
st.write("Cane allows you to log in, upload prescriptions, extract text, and convert text to audio for ease of access.")
