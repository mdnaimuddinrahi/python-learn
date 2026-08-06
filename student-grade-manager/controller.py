from utils import valid_input, valid_marks_input, print_divider, valid_int_input
import constants
from storage import load_data, save_data
from logger import logger


def get_next_student_id(data: list[dict[str, object]]) -> int:

    if data:
        return max(student["id"] for student in data) + 1
    
    return 1

def display_student_record(student: dict[str, object]) -> None:
    print()
    print_divider()
    print(f"{'Student ID':<{constants.LABEL_WIDTH}}: {student['id']}")
    print(f"{'Student Name':<{constants.LABEL_WIDTH}}: {student['name']}")
    print()
    print('Marks')
    print_divider(len("Marks"))

    for subject, mark in student.get("marks", {}).items():
        print(f"{subject:<{constants.LABEL_WIDTH}}: {mark}")
    print_divider()
    print()

def add_student() -> None:
    print('Please enter student details')
    name = valid_input("Enter Name: ", "Name")
    marks = {
        subject: valid_marks_input(f"Enter {subject} marks: ", subject)
        for subject in constants.SUBJECTS
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

def ensure_student_records_exist(data: list[dict[str, object]]) -> bool:

    if not data:
        print("No student records found.")

        return False

    return True

def view_all_students() -> None:
    data = load_data()

    if not ensure_student_records_exist(data): 
        return None

    for student in data:
        display_student_record(student)


def find_by_student_id() -> dict[str, object] | None:
    data = load_data()
    
    if not ensure_student_records_exist(data): 
        return
    
    student_id = valid_int_input("Enter student id: ")
    student = next(
        (student for student in data if student['id'] == student_id),
        None
    )

    if student is None:
        print('Student Not found.')

    return student


def view_student_details() -> None:
    while True:
        student = find_by_student_id()

        if student is None:
            search_again = confirm_input(f"Do you want search again? [{constants.CONFIRM_YES}/{constants.CONFIRM_NO}]: ", "Confirmation")

            if search_again == constants.CONFIRM_YES:
                continue
            else:
                return
        else:
            display_student_record(student)
            return
    
def confirm_input(placeholder: str = '', name: str = '')->str:
    while True:
        value = input(placeholder).strip().lower()

        if value in (constants.CONFIRM_YES, constants.CONFIRM_NO):
            return value
        elif not value:
            print(f"{name} can't be empty. Please try again.")
        else:
            print('Wrong Input, please try again.')
  
    