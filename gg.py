import streamlit as st
import pandas as pd
import datetime
import os

# File paths
PATIENTS_FILE = "patients.csv"
APPOINTMENTS_FILE = "appointments.csv"
PATIENT_HISTORY_FILE = "patient_history.csv"

# Load/save utilities
def load_data(file, columns):
    return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)

def save_data(file, new_data, columns):
    df = load_data(file, columns)
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(file, index=False)

# App UI
st.title("🏥 Hospital Management Dashboard")

# --- Register Patient ---
with st.expander("➕ Register New Patient"):
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
            st.success(f"Patient '{name}' registered.")
        else:
            st.error("Name and Contact are required.")

# --- Book Appointment ---
with st.expander("📅 Book Appointment"):
    patients = load_data(PATIENTS_FILE, ["Name", "Age", "Gender", "Contact", "Address", "Registered On"])
    if not patients.empty:
        patient_name = st.selectbox("Select Patient", patients["Name"].unique(), key="appt")
        doctor = st.selectbox("Doctor", ["Dr. Sharma", "Dr. Khan", "Dr. Patel"], key="doc")
        date = st.date_input("Date", min_value=datetime.date.today())
        time = st.time_input("Time")
        reason = st.text_area("Reason for Visit")

        if st.button("Book Appointment"):
            appt = {
                "Patient Name": patient_name,
                "Doctor": doctor,
                "Date": date.strftime("%Y-%m-%d"),
                "Time": time.strftime("%H:%M"),
                "Reason": reason,
                "Booked On": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_data(APPOINTMENTS_FILE, appt, ["Patient Name", "Doctor", "Date", "Time", "Reason", "Booked On"])
            st.success(f"Appointment booked for {patient_name} with {doctor}.")
    else:
        st.warning("Please register patients first.")

# --- Add/View Patient History ---
with st.expander("📝 Patient Medical History"):
    patients = load_data(PATIENTS_FILE, ["Name", "Age", "Gender", "Contact", "Address", "Registered On"])
    if not patients.empty:
        selected_patient = st.selectbox("Patient", patients["Name"].unique(), key="history")
        visit_date = st.date_input("Date of Visit", datetime.date.today(), key="visit_date")
        diagnosis = st.text_area("Diagnosis")
        treatment = st.text_area("Treatment")
        prescription = st.text_area("Prescription")
        doctor = st.selectbox("Doctor", ["Dr. Sharma", "Dr. Khan", "Dr. Patel"], key="hist_doc")

        if st.button("Save History"):
            entry = {
                "Patient Name": selected_patient,
                "Date": visit_date.strftime("%Y-%m-%d"),
                "Diagnosis": diagnosis,
                "Treatment": treatment,
                "Prescription": prescription,
                "Doctor": doctor,
                "Recorded On": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_data(PATIENT_HISTORY_FILE, entry, ["Patient Name", "Date", "Diagnosis", "Treatment", "Prescription", "Doctor", "Recorded On"])
            st.success(f"History saved for {selected_patient}.")

        st.subheader("📂 History Records for Patient")
        history_df = load_data(PATIENT_HISTORY_FILE, ["Patient Name", "Date", "Diagnosis", "Treatment", "Prescription", "Doctor", "Recorded On"])
        patient_history = history_df[history_df["Patient Name"] == selected_patient]
        if not patient_history.empty:
            st.dataframe(patient_history)
        else:
            st.info("No history found.")
    else:
        st.warning("No patients registered.")

# --- View All Records ---
with st.expander("📋 All Records"):
    view = st.radio("View Type", ["Patients", "Appointments", "History"], horizontal=True)
    
    if view == "Patients":
        df = load_data(PATIENTS_FILE, ["Name", "Age", "Gender", "Contact", "Address", "Registered On"])
    elif view == "Appointments":
        df = load_data(APPOINTMENTS_FILE, ["Patient Name", "Doctor", "Date", "Time", "Reason", "Booked On"])
    else:
        df = load_data(PATIENT_HISTORY_FILE, ["Patient Name", "Date", "Diagnosis", "Treatment", "Prescription", "Doctor", "Recorded On"])

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No records found.")
