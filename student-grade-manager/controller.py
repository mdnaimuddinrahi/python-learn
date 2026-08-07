import utils
import constants
from storage import load_data, save_data
from logger import logger

def get_next_student_id(data: constants.StudentList) -> int:

    if data:
        return max(student["id"] for student in data) + 1
    return 1

def display_student_record(student: constants.Student) -> None:
    print()
    utils.print_divider()
    print(f"{'Student ID':<{constants.LABEL_WIDTH}}: {student['id']}")
    print(f"{'Student Name':<{constants.LABEL_WIDTH}}: {student['name']}")
    print()
    print("Marks")
    utils.print_divider(len("Marks"))

    for subject, mark in student["marks"].items():
        print(f"{subject:<{constants.LABEL_WIDTH}}: {mark}")
    utils.print_divider()
    print()

def save_student_record(action: str, data: constants.StudentList, student: constants.Student) -> None:
    try:
        save_data(data)
    except OSError:
        logger.exception(f"Failed to {action} student data.")
        return
    print(f"\nStudent {action} successfully.")
    display_student_record(student)

def add_student() -> None:
    print('Please enter student details')
    
    data = load_data()

    student = {
        'id': get_next_student_id(data),
        'name': utils.valid_input("Enter Name: ", "Name")
    }
    
    student['marks'] = {
        subject: utils.valid_marks_input(f"Enter {subject} marks: ", subject)
        for subject in constants.SUBJECTS
    }
    data.append(student)
    save_student_record(constants.ACTION_CREATE, data, student)
    

def ensure_student_records_exist(data: constants.StudentList) -> bool:

    if not data:
        print("No student records found.")

        return False

    return True

def view_all_students() -> None:
    data = load_data()

    if not ensure_student_records_exist(data): 
        return

    for student in data:
        display_student_record(student)

def find_by_student_id(data: constants.StudentList, student_id: int) -> constants.Student | None:
    return next(
        (student for student in data if student['id'] == student_id),
        None
    )
  
def display_student_if_found(student: constants.Student | None, student_id: int) -> None:
    if student is None:
        utils.print_divider()
        print(f'Student Not found with ID {student_id}')
        print()
    else: 
        display_student_record(student)

def view_student_details() -> None:
    data = load_data()

    if not ensure_student_records_exist(data): 
        return
    
    while True:    
        student_id = utils.valid_int_input("Enter student id: ")
        student = find_by_student_id(data, student_id)
        display_student_if_found(student, student_id)
        
        search_again = utils.confirm_input(f"Do you want search again? [{constants.CONFIRM_YES}/{constants.CONFIRM_NO}]: ", "Confirmation")

        if search_again == constants.CONFIRM_NO:
            return

def update_student_record() -> None:
    data = load_data()
    while True:
        student_id = utils.valid_int_input("Enter student id: ")
        student = find_by_student_id(data, student_id)
        display_student_if_found(student, student_id)

        if student is None:
            search_again = utils.confirm_input(f"Do you want search again? [{constants.CONFIRM_YES}/{constants.CONFIRM_NO}]: ", "Confirmation")

            if search_again == constants.CONFIRM_YES:
                continue
            return
        should_update_name = utils.confirm_input(f'Do you want to update Name? [{constants.CONFIRM_YES}/{constants.CONFIRM_NO}]: ', 'Confirmation')
        
        if should_update_name == constants.CONFIRM_YES:
            student['name'] = utils.valid_input("Enter Name: ", "Name")

        # marks = student['marks']

        for subject in constants.SUBJECTS:
            should_update_mark = utils.confirm_input(
                f'Do you want to update {subject} marks? [{constants.CONFIRM_YES}/{constants.CONFIRM_NO}]: ',
                'Confirmation'
            )

            if should_update_mark == constants.CONFIRM_YES:
                student['marks'][subject] = utils.valid_marks_input(f"Enter {subject} marks: ", subject)
        save_student_record(constants.ACTION_UPDATE, data, student)

        search_again = utils.confirm_input(
            utils.confirm_input_message("Do you want update anything else?")
        )
        
        if search_again == constants.CONFIRM_NO:
            return
        
def delete_student_record():
    data = load_data()

    while True:
        student_id = utils.valid_int_input("Enter student id: ")
        student = find_by_student_id(data, student_id)
        display_student_if_found(student, student_id)
        if student is None:
            search_again = utils.confirm_input(
                utils.confirm_input_message("Do you want to search again?")
            )

            if search_again == constants.CONFIRM_YES:
                continue
            return
        delete_confirmation = utils.confirm_input(
            utils.confirm_input_message("Are you sure you want to delete?")
        )

        if delete_confirmation == constants.CONFIRM_YES:
            data.remove(student)
            save_student_record(constants.ACTION_DELETE, data, student)
        return

