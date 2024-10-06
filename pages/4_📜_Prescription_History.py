import streamlit as st
import os
import pandas as pd

# Prescription History - Page 4
def prescription_history():
    st.title("Prescription History")

    # Check if the prescription file exists
    if os.path.exists("prescriptions.csv"):
        # Load the prescriptions
        prescriptions = pd.read_csv("prescriptions.csv")

        if not prescriptions.empty:
            # Display the stored prescriptions
            st.subheader("Your Prescriptions:")
            st.dataframe(prescriptions)
        else:
            # If the file exists but is empty
            st.subheader("No prescriptions stored yet.")
    else:
        # If the file does not exist
        st.subheader("No prescriptions stored yet.")