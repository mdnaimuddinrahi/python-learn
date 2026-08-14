# 🏥 Doctor Appointment Booking Management System

A simple **command-line Doctor Appointment Booking Management System** built with Python to manage doctors, patients, schedules, time slots, and appointments.

## 🎯 Project Goal

The system helps clinic staff manage appointments while preventing common scheduling problems such as double booking and booking outside a doctor's working schedule.

## ✨ Features

### 👨‍⚕️ Doctor Management
- Add, view, list, search, update, and deactivate doctors.

### 🧑‍🤝‍🧑 Patient Management
- Add, view, list, search, and update patients.

### 📅 Schedule Management
- Configure doctor working days.
- Set opening and closing times.
- Set appointment slot duration.
- Generate appointment slots dynamically.

### 🔎 Availability
- Select a doctor and date.
- Display generated slots.
- Show slot status: 🟢 Available, 🔵 Booked, 🔴 Blocked.

### 📋 Appointment Management
- Create, view, list, search, and cancel appointments.
- Search by patient, doctor, or date.

### 🚫 Slot Management
- Block a doctor's specific time slot.
- Unblock a blocked slot.
- Prevent blocked slots from being booked.

### 📊 Daily Schedule
- View a doctor's complete schedule for a selected date.

## 📌 Appointment Rules

Before creating an appointment, the system verifies:

- ✅ Doctor exists.
- ✅ Patient exists.
- ✅ Date is valid and not in the past.
- ✅ Doctor works on the selected date.
- ✅ Time is within working hours.
- ✅ Time belongs to a generated slot.
- ✅ Slot is not blocked.
- ✅ Slot is not occupied by another active appointment.

## 🧠 Business Rules

- 🆔 Doctor, patient, and appointment IDs must be unique.
- 👨‍⚕️ A doctor can have multiple appointments.
- 🧑‍🤝‍🧑 A patient can have multiple appointments.
- 🚫 A doctor cannot have two active appointments at the same date and time.
- 🚫 Blocked slots cannot be booked.
- ❌ Cancelled appointments remain in the records.
- ♻️ Cancelled appointments release their time slots.
- 🕐 Appointment times must come from the doctor's generated schedule.
- ⚙️ Slots are generated dynamically rather than manually stored.
- 🚫 Blocked slots are marked instead of deleted.

## 🛡️ Validation

The application validates:

- Required fields
- Phone number format
- Date and time format
- Existing doctor/patient IDs
- Appointment availability
- Valid appointment slots

## 🖥️ Main Menu

```text
1. Doctor Management
2. Patient Management
3. Manage Doctor Schedule
4. Check Availability
5. Create Appointment
6. View Appointment
7. List Appointments
8. Search Appointments
9. Cancel Appointment
10. Block Time Slot
11. Unblock Time Slot
12. Daily Schedule
13. Exit
```

## 🗂️ Suggested Structure

```text
doctor-appointment-booking/
│
├── app/
│   ├── doctor.py
│   ├── patient.py
│   ├── schedule.py
│   ├── appointment.py
│   └── utils.py
│
├── data/
│   ├── doctors.json
│   ├── patients.json
│   ├── schedules.json
│   └── appointments.json
│
├── main.py
├── README.md
└── requirements.txt
```

## 🧰 Technology

- 🐍 Python
- 📄 JSON
- 💻 Command Line Interface (CLI)

### Python Concepts Practiced

- Variables and data types
- Lists and dictionaries
- Conditions and loops
- Functions
- List comprehensions
- String methods
- Date/time handling
- Input validation
- JSON file handling

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/mdnaimuddinrahi/python-learn
cd doctor-appointment-booking
```

### Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python main.py
```

## 💾 Data Storage

JSON files are used for persistent storage:

```text
data/
├── doctors.json
├── patients.json
├── schedules.json
└── appointments.json
```

## 🔮 Future Improvements

- 🗄️ SQLite/MySQL database
- 🌐 Web interface
- 🔐 Authentication
- 👥 Role-based access
- 📧 Email notifications
- 📱 SMS notifications
- 📈 Appointment reports
- 🏥 Multi-clinic support

## 📚 Project Purpose

This project is designed to apply Python fundamentals to a realistic business problem involving:

**Data Management → Validation → Business Rules → Scheduling → Persistence → Reporting**

## 👨‍💻 Author

**Rahi**

Built as a practical Python project for learning and portfolio development.
