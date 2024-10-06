import streamlit as st

st.title("Profile Setup")

st.write("Please provide your details to complete your profile setup.")

gender = st.selectbox("Gender", ["Female", "Male", "Other"])
dob = st.date_input("Date of Birth")
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
