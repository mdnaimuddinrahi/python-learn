# 🎓 Student Grade Manager

A small command-line **Student Grade Manager** built with Python. This project manages student records, marks, grades, GPA, reports, class rankings, and statistics using JSON for data persistence.

The project was built as part of my Python learning journey to practice **functions, data structures, file handling, validation, CRUD operations, calculations, sorting, error handling, logging, and testing**.

---

## ✨ Features

### 👨‍🎓 Student Management

- ➕ Add a new student
- 📋 View all students
- 🔎 Search student by ID
- ✏️ Update student information
- 🗑️ Delete student
- 🆔 Automatically generate student IDs

### 📚 Marks & Grades

- 📝 Store marks for multiple subjects
- ✅ Validate marks between `0–100`
- 📊 Calculate total marks
- 📈 Calculate average marks
- 🏆 Calculate letter grade
- 🎯 Calculate GPA
- ✅ Determine PASS / FAIL status

### 📊 Reports

- 👤 View individual student report
- 📋 View all student reports
- 🏅 View class ranking
- 📈 View class statistics
- 🎓 Display highest and lowest scorers
- 📊 Display class average
- ✅ Display pass/fail statistics and rates

### 💾 Data Persistence

- 📁 Store student records in JSON
- 📥 Load records from `database.json`
- 💾 Save changes automatically
- ⚠️ Handle missing or invalid JSON data
- 📝 Log storage errors using Python logging

### 🛡️ Input Validation

- 🚫 Prevent empty names
- 🔤 Validate student names
- 🔢 Validate numeric input
- 📏 Limit student name length
- 📚 Validate marks within the allowed range
- ❓ Validate confirmation input

---

## 🛠️ Technologies

- 🐍 Python 3
- 📦 JSON
- 🧪 pytest
- 📝 Python `logging`
- 📚 Standard Library

---

## 📁 Project Structure

```text
student-grade-manager/
│
├── 📄 constants.py              # Application constants and type definitions
├── 🎮 controller.py             # Student operations, reports, ranking and statistics
├── 💾 database.json             # JSON student data
├── 📝 logger.py                 # Application logging configuration
├── 🚀 main.py                   # Application entry point and menu
├── 📋 project-requirements.txt  # Project requirements and specifications
├── 📖 README.md                 # Project documentation
├── 💾 storage.py                # JSON load/save operations
├── 🧪 test_storage.py           # Storage tests
├── 🛠️ utils.py                  # Input validation and utility functions
└── 🚫 .gitignore                # Ignored files and directories
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone <https://github.com/mdnaimuddinrahi/python-learn>
```

### 2. Navigate to the project

```bash
cd student-grade-manager
```

### 3. Run the application

```bash
python main.py
```

---

## 🧭 Application Menu

```text
1. Add Student
2. View All Students
3. Search Student by ID
4. Update Student
5. Delete Student
6. View Student Report
7. View All Reports
8. Class Ranking
9. Class Statistics
0. Exit
```

---

## 📊 Grade System

| Average Marks | Grade | GPA |
|---:|:---:|---:|
| 80–100 | A+ | 4.00 |
| 70–79 | A | 3.75 |
| 60–69 | A- | 3.50 |
| 50–59 | B | 3.00 |
| 40–49 | C | 2.00 |
| 33–39 | D | 1.00 |
| 0–32 | F | 0.00 |

A student is considered **PASS** only when every subject mark meets the minimum passing mark.

---

## 🧪 Testing

The project includes tests for the JSON storage functionality.

Run the tests with:

```bash
pytest
```

---

## 💡 What I Practiced

This project helped me practice:

- 🐍 Python functions
- 📦 Lists and dictionaries
- 🔄 Loops and comprehensions
- 🧩 Modular programming
- 📝 Type hints
- 🔐 Input validation
- 📂 File handling
- 💾 JSON serialization/deserialization
- ⚠️ Exception handling
- 📝 Logging
- 🔍 Searching
- ✏️ CRUD operations
- 📊 Data aggregation
- 🏆 Sorting and ranking
- 🧪 Unit testing
- 🧹 Code organization

---

## 🚀 Future Improvements

Possible improvements for a future version:

- 🗄️ Replace JSON storage with SQLite
- 🧪 Expand test coverage
- 🖥️ Build a graphical or web interface
- 📤 Add CSV export
- 📊 Add more detailed subject-wise statistics
- 🧑‍🏫 Add teacher/class management
- 🔐 Add authentication and user roles

---

## 👨‍💻 Project Status

**Status: ✅ Completed**

This project is intentionally kept small and focused on practicing core Python development concepts through a real-world style application.

---

## 📜 License

This project is for learning and portfolio purposes.