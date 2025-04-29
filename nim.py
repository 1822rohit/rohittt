import streamlit as st
import pandas as pd
import os
import datetime

# File paths
PATIENTS_FILE = "patients.csv"
APPOINTMENTS_FILE = "appointments.csv"

# Helper functions
def load_data(file, columns):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=columns)

def save_data(file, new_data, columns):
    df = load_data(file, columns)
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(file, index=False)

# App Title
st.title("🏥 Hospital Management System")

# Tabs for different operations
tab1, tab2, tab3 = st.tabs(["Register Patient", "Book Appointment", "View Records"])

with tab1:
    st.header("➕ Register New Patient")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    contact = st.text_input("Contact Number")
    address = st.text_area("Address")

    if st.button("Register Patient"):
        if name and contact:
            patient = {
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Contact": contact,
                "Address": address,
                "Registered On": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_data(PATIENTS_FILE, patient, ["Name", "Age", "Gender", "Contact", "Address", "Registered On"])
            st.success(f"Patient {name} registered successfully.")
        else:
            st.error("Name and Contact are required.")

with tab2:
    st.header("📅 Book Appointment")
    patients = load_data(PATIENTS_FILE, ["Name", "Age", "Gender", "Contact", "Address", "Registered On"])
    if not patients.empty:
        patient_name = st.selectbox("Select Patient", patients["Name"].unique())
        doctor = st.selectbox("Select Doctor", ["Dr. Sharma", "Dr. Khan", "Dr. Patel"])
        date = st.date_input("Appointment Date", min_value=datetime.date.today())
        time = st.time_input("Appointment Time")
        reason = st.text_area("Reason for Visit")

        if st.button("Book Appointment"):
            appointment = {
                "Patient Name": patient_name,
                "Doctor": doctor,
                "Date": date.strftime("%Y-%m-%d"),
                "Time": time.strftime("%H:%M"),
                "Reason": reason,
                "Booked On": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_data(APPOINTMENTS_FILE, appointment, ["Patient Name", "Doctor", "Date", "Time", "Reason", "Booked On"])
            st.success(f"Appointment booked for {patient_name} with {doctor} on {date}.")
    else:
        st.warning("Please register a patient first.")

with tab3:
    st.header("📋 View Records")

    view_option = st.selectbox("Select Record Type", ["Patients", "Appointments"])

    if view_option == "Patients":
        data = load_data(PATIENTS_FILE, ["Name", "Age", "Gender", "Contact", "Address", "Registered On"])
    else:
        data = load_data(APPOINTMENTS_FILE, ["Patient Name", "Doctor", "Date", "Time", "Reason", "Booked On"])

    if not data.empty:
        st.dataframe(data)
    else:
        st.info(f"No {view_option.lower()} records found.")
