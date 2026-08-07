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

def ensure_student_records_exist(data: constants.StudentList) -> bool:

    if not data:
        print("No student records found.")

        return False

    return True

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

def calculate_total_marks(marks: dict[str, int]) -> int:
    return sum(marks.values())

def calculate_average_marks(marks: dict[str, int]) -> float:
    return calculate_total_marks(marks)/ len(constants.SUBJECTS)

def calculate_gpa(marks: dict[str, int]) -> float:
    average_mark = calculate_average_marks(marks)

    for minimum_mark, maximum_mark, letter, gpa in constants.GRADE_BOUNDARIES:
        if minimum_mark <= average_mark <= maximum_mark:
            return gpa
    raise ValueError(f"No matching gpa boundary for average: {average_mark}")

def find_grade(marks: dict[str, int]) -> str:
    average_mark = calculate_average_marks(marks)

    for minimum_mark, maximum_mark, letter, gpa in constants.GRADE_BOUNDARIES:
        if minimum_mark <= average_mark <= maximum_mark:
            return letter
    raise ValueError(f"No matching grade boundary for average: {average_mark}")

def get_pass_or_fail_status(marks: dict[str, int]) -> str:
    
    for subject, mark in marks.items():
        if mark < constants.PASS_MARKS:
            return "FAIL"
    return "PASS"

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

def view_all_students() -> None:
    data = load_data()

    if not ensure_student_records_exist(data): 
        return

    for student in data:
        display_student_record(student)

def view_student_details() -> None:
    data = load_data()

    if not ensure_student_records_exist(data): 
        return
    
    while True:    
        student_id = utils.valid_int_input("Enter student id: ")
        student = find_by_student_id(data, student_id)
        display_student_if_found(student, student_id)
        
        search_again = utils.confirm_input(
            utils.confirm_input_message("Do you want search again?")
        )

        if search_again == constants.CONFIRM_NO:
            return

def update_student_record() -> None:
    data = load_data()
    while True:
        student_id = utils.valid_int_input("Enter student id: ")
        student = find_by_student_id(data, student_id)
        display_student_if_found(student, student_id)

        if student is None:
            search_again = utils.confirm_input(
                utils.confirm_input_message("Do you want search again?")
            )
            if search_again == constants.CONFIRM_YES:
                continue
            return
        should_update_name = utils.confirm_input(
            utils.confirm_input_message("Do you want to update Name?")
        )
        
        if should_update_name == constants.CONFIRM_YES:
            student['name'] = utils.valid_input("Enter Name: ", "Name")

        for subject in constants.SUBJECTS:
            should_update_mark = utils.confirm_input(
                            utils.confirm_input_message(f"Do you want to update {subject} marks?")
                        )

            if should_update_mark == constants.CONFIRM_YES:
                student['marks'][subject] = utils.valid_marks_input(f"Enter {subject} marks: ", subject)
        save_student_record(constants.ACTION_UPDATE, data, student)

        search_again = utils.confirm_input(
            utils.confirm_input_message("Do you want update anything else?")
        )
        
        if search_again == constants.CONFIRM_NO:
            return

def delete_student_record() -> None:
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

def view_report() -> None:
    data = load_data()
    
    if not ensure_student_records_exist(data): 
        return
    
    while True:
        print()
        student_id = utils.valid_int_input("Enter student id: ")
        student = find_by_student_id(data, student_id)
        display_student_if_found(student, student_id)

        if student is not None:
            marks = student['marks']
            total_marks = calculate_total_marks(marks)
            average_marks = calculate_average_marks(marks)
            grade = find_grade(marks)
            gpa = calculate_gpa(marks)
            status = get_pass_or_fail_status(marks)
            maximum_marks = len(constants.SUBJECTS) * constants.MAX_MARKS
            label_width = 15

            print(f"{'Total Marks':<{label_width}}: {total_marks} / {maximum_marks}")
            print(f"{'Average Marks':<{label_width}}: {average_marks}")
            print(f"{'Grade':<{label_width}}: {grade}")
            print(f"{'GPA':<{label_width}}: {gpa:.2f}")
            print(f"{'Status':<{label_width}}: {status}")
            utils.print_divider()
            print()
            
        search_again = utils.confirm_input(
            utils.confirm_input_message("Do you want to search again?")
        )

        if search_again == constants.CONFIRM_NO:
            return

def view_all_reports() -> None:
    data = load_data()

    if not ensure_student_records_exist(data): 
        return    

    utils.print_divider(70)
    print(f"{'ID':<5}{'Name':<19}{'Total':<9}{'Average':<11}{'Grade':<9}{'GPA':<8}{'Status'}")
    utils.print_divider(70)

    for student in data:
        marks = student['marks']
        total = calculate_total_marks(marks)
        average = calculate_average_marks(marks)
        grade = find_grade(marks)
        gpa = calculate_gpa(marks)
        status = get_pass_or_fail_status(marks)
        print(f"{student['id']:<5}{student['name']:<19}{total:<9}{average:<11.2f}{grade:<9}{gpa:<8.2f}{status}")
    utils.print_divider(70)
    print()

def view_ranking() -> None:
    pass

def view_statistics() -> None:
    pass