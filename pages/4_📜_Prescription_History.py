import streamlit as st
import os
import pandas as pd

# Prescription details - Page 4
def prescription_details():
    st.title("Prescription Details")

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
        
    # Option to add a new prescription
    st.subheader("Add New Prescription")
    with st.form("add_prescription_form"):
        medicine_name = st.text_input("Medicine Name")
        dosage = st.text_input("Dosage")
        frequency = st.text_input("Frequency")
        submit_button = st.form_submit_button("Add Prescription")

    if submit_button:
        if medicine_name and dosage and frequency:
            new_prescription = pd.DataFrame({
                'Medicine Name': [medicine_name],
                'Dosage': [dosage],
                'Frequency': [frequency]
            })

            if os.path.exists("prescriptions.csv"):
                prescriptions = pd.read_csv("prescriptions.csv")
                updated_prescriptions = pd.concat([prescriptions, new_prescription], ignore_index=True)
            else:
                updated_prescriptions = new_prescription

            updated_prescriptions.to_csv("prescriptions.csv", index=False)
            st.success("Prescription added successfully!")
        else:
            st.error("Please fill out all fields before submitting.")