import streamlit as st
from datetime import datetime

st.title("Profile Setup")

st.write("Please provide your details to complete your profile setup.")

gender = st.selectbox("Gender", ["Female", "Male", "Other"])


min_date = datetime(1920, 1, 1)
max_date = datetime.now()


default_date = datetime(2000, 1, 1)


dob = st.date_input("Date of Birth", value=default_date, min_value=min_date, max_value=max_date)

conditions = st.multiselect("Do you have any of the following conditions?", 
                            ["Diabetes", "Hypertension", "Arthritis", "Asthma", "Other (Specify)"])
disabilities = st.multiselect("Do you have any disabilities?", 
                              ["Visual Impairment", "Hearing Impairment", "Mobility Issues", "Other (Please specify)"])
medications = st.text_area("Are you currently taking any medications? (Enter medicine name)")

if st.button("Submit"):
    st.success("Profile setup completed.")
    st.write(f"Gender: {gender}")
    st.write(f"Date of Birth: {dob}")
    st.write(f"Conditions: {', '.join(conditions)}")
    st.write(f"Disabilities: {', '.join(disabilities)}")
    st.write(f"Medications: {medications}")
