from utils import valid_input, valid_marks_input, print_divider
from constants import SUBJECTS, LABEL_WIDTH
from storage import load_data, save_data
from logger import logger

def get_next_student_id(data: list[dict[str, object]]) -> int:
    if data:
        return max(student["id"] for student in data) + 1
    return 1

def display_student_record(student: dict[str, object])->None:
    print()
    print_divider()
    print(f"{'Student ID':<{LABEL_WIDTH}}: {student['id']}")
    print(f"{'Student Name':<{LABEL_WIDTH}}: {student['name']}")
    print()
    print('Marks')
    print_divider(len("Marks"))
    for subject, mark in student.get("marks", {}).items():
        print(f"{subject:<{LABEL_WIDTH}}: {mark}")
    print_divider()
    print()

def add_student()->None:
    
    print('Please enter student details')
    name = valid_input("Enter Name: ", "Name")
    marks = {
        subject: valid_marks_input(f"Enter {subject} marks: ", subject)
        for subject in SUBJECTS
    }
    data = load_data()
    student = {
        "id": get_next_student_id(data),
        "name": name,
        "marks": marks
    }
    data.append(student)
    try:
        save_data(data)
    except OSError:
        logger.exception("Failed to save student data.")
        return
    print("\nStudent added successfully.")
    display_student_record(student)

if __name__ == "__main__":
    add_student()