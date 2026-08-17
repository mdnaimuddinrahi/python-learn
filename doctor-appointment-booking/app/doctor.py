from . import constant 
from . import helper
from app.storage import load_data, save_data
from app.logger import logger
from datetime import datetime

COLUMN_ID="id"
COLUMN_NAME="name"
COLUMN_SPECIALIZATION="specialization"
COLUMN_PHONE="phone"
COLUMN_STATUS="status"
COLUMN_CREATED_AT="created_at"
COLUMN_UPDATED_AT="updated_at"
STATUS_OPTION = {
    1 : "Active",
    2 : "In-Active",
    3 : "On-Leave",
    4 : "Closed",
}
STATUS_OPTION_PREVIEW = """
1. Active.
2. In-Active.
3. On-Leave.
4. Closed
"""
TOTAL_STATUS = 4

LABEL_WIDTH = max(
    len("Doctor ID"),
    len("Doctor Name"),
    len("Specialize In"),
    len("Phone Number"),
    len("Created At"),
    len("Updated At"),
) + 2

MENU_DOCTOR_MANAGE_OPTIONS = """
1. Add Doctor
2. View Doctor
3. Doctor List
4. Update Doctor
5. Doctor Status
6. Back
"""

MENU_DOCTOR_LIST_OPTIONS = """
1. All List.
2. Search By Name.
3. Search By Specialize.
4. Search By Status.
5. Search By Phone.
6. Back to Doctors Menu.
"""
DOCTOR_LIST_ALL = 1
DOCTOR_LIST_BY_NAME = 2
DOCTOR_LIST_BY_SPECIALIZE = 3
DOCTOR_LIST_BY_STATUS = 4
DOCTOR_LIST_BY_PHONE = 5
DOCTOR_LIST_BACK = 6

DOCTOR_MENU_ADD = 1
DOCTOR_MENU_VIEW = 2
DOCTOR_MENU_LIST = 3
DOCTOR_MENU_UPDATE = 4
DOCTOR_MENU_STATUS = 5
DOCTOR_MENU_BACK = 6

def manage_doctor():
    helper.print_title("Doctor Management")

    while True:
        print(MENU_DOCTOR_MANAGE_OPTIONS)
        choice = helper.valid_option_input("Choose an option: ", name="Option", max_value=6)                

        if choice == DOCTOR_MENU_ADD:
            add_doctor()
        elif choice == DOCTOR_MENU_VIEW:
            view_doctor()
        elif choice == DOCTOR_MENU_LIST:
            doctor_list()
        elif choice == DOCTOR_MENU_UPDATE:
            update_doctor()
        elif choice == DOCTOR_MENU_STATUS:
            doctor_status()
        elif choice == DOCTOR_MENU_BACK:
            return
        else:
            print("Invalid option, please try again.")

def add_doctor():
    print('Please enter doctor details')
    data = load_data(constant.TABLE_DOCTOR)
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    doctor = {
        COLUMN_ID: helper.get_next_id(data),
        COLUMN_NAME: helper.valid_input(placeholder="Enter Name: ",name="Name",limit=30),
        COLUMN_SPECIALIZATION: helper.valid_input(placeholder="Enter Specialized In:", name="Specialized", limit=200),
        COLUMN_CREATED_AT: current_date_time,
        COLUMN_UPDATED_AT:"-",
    }
    phone = helper.valid_input(
                placeholder="Enter Phone:", 
                name="Phone", 
                required=False,
                type="phone")
    doctor[COLUMN_PHONE] = phone or "-"            
    print("Choose an option:")
    print(STATUS_OPTION_PREVIEW)
    status = helper.valid_option_input("Enter Status:", "Status", TOTAL_STATUS)
    doctor[COLUMN_STATUS] = STATUS_OPTION[status]
    data.append(doctor)
    save_doctor_record(constant.ACTION_CREATE, data, doctor)

def view_doctor():
    data = load_data(constant.TABLE_DOCTOR)

    if not ensure_doctor_records_exist(data):
        return
    while True:
        doctor_id = helper.valid_input(
            placeholder="Enter Doctor Id:",
            name="Doctor",
            type="int"
        )
        doctor = find_by_doctor_id(data, doctor_id)
        display_doctor_if_found(doctor, doctor_id)

        search_again = helper.confirm_input(
            helper.confirm_input_message("Do you want search again?")
        )        

        if search_again == constant.CONFIRM_NO:
            return        

def doctor_list() -> None:
    data = load_data(constant.TABLE_DOCTOR)
    if not ensure_doctor_records_exist(data):
        return

    while True:
        print(MENU_DOCTOR_LIST_OPTIONS)
        choice = helper.valid_option_input("Choose an option: ", name="Option", max_value=6)                

        if choice == DOCTOR_LIST_ALL:
            filter_data = data
        elif choice == DOCTOR_LIST_BY_NAME:
            name = helper.valid_input(
                placeholder="Enter Doctor Name: ", 
                name= "Doctor Name",
                limit= 50)
            filter_data = [
                doctor for doctor in data
                if name.lower() in doctor[COLUMN_NAME].lower()
            ]
        elif choice == DOCTOR_LIST_BY_PHONE:
            phone = helper.valid_input(
                placeholder="Enter Doctor Phone: ",
                name="Doctor Phone",
                limit=20,
                type="phone"
            )
            filter_data = [
                doctor for doctor in data
                if phone in doctor[COLUMN_PHONE]
            ]
        elif choice == DOCTOR_LIST_BY_SPECIALIZE:
            specialize = helper.valid_input(
                placeholder="Enter Doctor Specialization", 
                name= "Doctor Specialize",
                limit= 50)
            filter_data = [
                doctor for doctor in data
                if specialize.lower() in doctor[COLUMN_SPECIALIZATION].lower()
            ]
        elif choice == DOCTOR_LIST_BY_STATUS:
            print("Choose an option:")
            print(STATUS_OPTION_PREVIEW)
            status = helper.valid_option_input("Enter Status:", "Status", TOTAL_STATUS)
            filter_data = [
                doctor for doctor in data
                if STATUS_OPTION[status] == doctor[COLUMN_STATUS]
            ]
        elif choice == DOCTOR_LIST_BACK:
            return
        else:
            print("Invalid option, please try again.")

        if not ensure_doctor_records_exist(filter_data):
            continue

        helper.print_divider(divider="*", color=constant.COLOR_YELLOW)
        print(f"\n Total doctors found: {len(filter_data)}")

        for doctor in filter_data:
            display_doctor_if_found(doctor, doctor[COLUMN_ID])


def ensure_doctor_records_exist(data: constant.TYPE_LIST) -> bool:
    if not data:
        print("No doctor records found.")

        return False
    return True

def update_doctor() -> None:
    data = load_data(constant.TABLE_DOCTOR)

    while True:
        doctor_id = helper.valid_input(
            placeholder="Enter Doctor Id:",
            name="Doctor",
            type="int"
        )
        doctor = find_by_doctor_id(data, doctor_id)
        display_doctor_if_found(doctor, doctor_id)

        if doctor is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message("Do you want search again?")
            )        

            if search_again == constant.CONFIRM_YES:
                continue
            return   

        is_updated = False
        should_update_name = helper.confirm_input(
            helper.confirm_input_message("Do you want to update Name?")
        )

        if should_update_name == constant.CONFIRM_YES:
            doctor[COLUMN_NAME] = helper.valid_input(placeholder="Enter Name: ", name="Name", limit=30)
            is_updated = True

        should_update_specialize = helper.confirm_input(
            helper.confirm_input_message("Do you want to update specialization?")
        )

        if should_update_specialize == constant.CONFIRM_YES:
            doctor[COLUMN_SPECIALIZATION] = helper.valid_input(placeholder="Enter Specialization: ", name="Specialization", limit=200)
            is_updated = True
        
        should_update_phone = helper.confirm_input(
            helper.confirm_input_message("Do you want to update phone?")
        )

        if should_update_phone == constant.CONFIRM_YES:
            doctor[COLUMN_PHONE] = helper.valid_input(placeholder="Enter Phone: ", name="Phone", limit=20, type="phone")
            is_updated = True

        should_update_status = helper.confirm_input(
            helper.confirm_input_message("Do you want to update status?")
        )

        if should_update_status == constant.CONFIRM_YES:
            print("Choose an option:")
            print(STATUS_OPTION_PREVIEW)
            status = helper.valid_option_input("Enter Status:", "Status", TOTAL_STATUS)
            doctor[COLUMN_STATUS] = STATUS_OPTION[status]
            is_updated = True

        if is_updated:
            current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            doctor[COLUMN_UPDATED_AT] = current_date_time

        save_doctor_record(constant.ACTION_UPDATE, data, doctor)
        
        search_again = helper.confirm_input(
            helper.confirm_input_message("Do you want update anything else?")
        )

        if search_again == constant.CONFIRM_NO:
            return

def doctor_status() -> None:
    data = load_data(constant.TABLE_DOCTOR)

    while True:
        doctor_id = helper.valid_input(
            placeholder="Enter Doctor Id:",
            name="Doctor",
            type="int"
        )
        doctor = find_by_doctor_id(data, doctor_id)
        display_doctor_if_found(doctor, doctor_id)

        if doctor is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message("Do you want to search again?")
            )

            if search_again == constant.CONFIRM_YES:
                continue
            return
        else:
            should_update_status = helper.confirm_input(
                helper.confirm_input_message("Do you want to update status?")
            )

            if should_update_status == constant.CONFIRM_YES: 
                print("Choose an option:")
                print(STATUS_OPTION_PREVIEW)
                status = helper.valid_option_input("Enter Status:", "Status", TOTAL_STATUS)
                doctor[COLUMN_STATUS] = STATUS_OPTION[status]
                save_doctor_record(constant.ACTION_UPDATE, data, doctor)
        return

def save_doctor_record(action: str, data: constant.TYPE_LIST, doctor: constant.TYPE_DICT) -> None:
    try:
        save_data(constant.TABLE_DOCTOR, data)
    except OSError:
        logger.exception(f"Failed to {action} doctor data.")
        return
    print(f"\nDoctor {action} successfully.")
    display_doctor_if_found(doctor, doctor_id=doctor[COLUMN_ID])

def display_doctor_if_found(doctor: constant.TYPE_DICT | None, doctor_id: int) -> None:
    if doctor is None:
        helper.print_divider(color=constant.COLOR_RED)
        print(f'Doctor Not found with ID {doctor_id}\n')
    else:
        print()
        helper.print_divider(color=constant.COLOR_GREEN)
        print(f"{'Doctor ID':<{LABEL_WIDTH}}: {doctor[COLUMN_ID]}")
        print(f"{'Doctor Name':<{LABEL_WIDTH}}: {doctor[COLUMN_NAME]}")
        print(f"{'Specialize In':<{LABEL_WIDTH}}: {doctor[COLUMN_SPECIALIZATION]}")
        print(f"{'Phone Number':<{LABEL_WIDTH}}: {doctor[COLUMN_PHONE]}")
        print(f"{'Status':<{LABEL_WIDTH}}: {doctor[COLUMN_STATUS]}")
        print(f"{'Created At':<{LABEL_WIDTH}}: {doctor[COLUMN_CREATED_AT]}")
        print(f"{'Updated At':<{LABEL_WIDTH}}: {doctor[COLUMN_UPDATED_AT]}")
    
        print()
                
def find_by_doctor_id(data: constant.TYPE_LIST, doctor_id: int) -> constant.TYPE_DICT | None:
    return next(
            (doctor for doctor in data if doctor[COLUMN_ID] == doctor_id), None
        )

