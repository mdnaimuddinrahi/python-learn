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
COLUMN_SCHEDULE="schedule"
COLUMN_CREATED_AT="created_at"
COLUMN_UPDATED_AT="updated_at"
STATUS_OPTION = {
    1 : "Active",
    2 : "In-Active",
    3 : "On-Leave",
    4 : "Closed",
}

LABEL_WIDTH = max(
    len("Doctor ID"),
    len("Doctor Name"),
    len("Specialize In"),
    len("Phone Number"),
    len("Created At"),
    len("Updated At"),
) + 2

DOCTOR_MENU_ADD = 1
DOCTOR_MENU_VIEW = 2
DOCTOR_MENU_LIST = 3 
DOCTOR_MENU_UPDATE = 4
DOCTOR_MENU_STATUS = 5
DOCTOR_MENU_BACK = 6

MENU_DOCTOR_MANAGE_OPTIONS = {
    DOCTOR_MENU_ADD: "Add Doctor",
    DOCTOR_MENU_VIEW: "View Doctor",
    DOCTOR_MENU_LIST: "Doctor List",
    DOCTOR_MENU_UPDATE: "Update Doctor",
    DOCTOR_MENU_STATUS: "Doctor Status",
    DOCTOR_MENU_BACK: "Back",
}

DOCTOR_LIST_ALL = 1
DOCTOR_LIST_BY_NAME = 2
DOCTOR_LIST_BY_SPECIALIZE = 3
DOCTOR_LIST_BY_STATUS = 4
DOCTOR_LIST_BY_PHONE = 5
DOCTOR_LIST_BACK = 6

MENU_DOCTOR_LIST_OPTIONS = {
    DOCTOR_LIST_ALL : "All List.",
    DOCTOR_LIST_BY_NAME : "Search By Name.",
    DOCTOR_LIST_BY_SPECIALIZE : "Search By Specialize.",
    DOCTOR_LIST_BY_STATUS : "Search By Status.",
    DOCTOR_LIST_BY_PHONE : "Search By Phone.",
    DOCTOR_LIST_BACK : "Back to Doctors Menu.",
}

def manage_doctor():
    helper.print_title("Doctor Management")

    while True:
        helper.display_menu(MENU_DOCTOR_MANAGE_OPTIONS)
        choice = helper.valid_option_input("Choose an option: ", name="Option", max_value=len(MENU_DOCTOR_MANAGE_OPTIONS))

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

def add_doctor() -> None:
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
    helper.display_menu(STATUS_OPTION)
    status = helper.valid_option_input("Enter Status:", "Status", len(STATUS_OPTION))
    doctor[COLUMN_STATUS] = STATUS_OPTION[status]
    doctor[COLUMN_SCHEDULE] = list()
    data.append(doctor)
    save_doctor_record(constant.ACTION_CREATE, data, doctor)

def view_doctor() -> None:
    data = load_data(constant.TABLE_DOCTOR)

    if not helper.ensure_records_exist(data, 'doctor'):
        return
    while True:
        doctor_id = helper.valid_input(
            placeholder="Enter Doctor Id:",
            name="Doctor",
            type="int"
        )
        doctor = helper.find_by_id(data, doctor_id)
        display_doctor_if_found(doctor, doctor_id)

        search_again = helper.confirm_input(
            helper.confirm_input_message("Do you want search again?")
        )        

        if search_again == constant.CONFIRM_NO:
            return        

def doctor_list() -> None:
    data = load_data(constant.TABLE_DOCTOR)
    if not helper.ensure_records_exist(data, 'doctor'):
        return

    while True:
        helper.display_menu(MENU_DOCTOR_LIST_OPTIONS)
        choice = helper.valid_option_input("Choose an option: ", name="Option", max_value=len(MENU_DOCTOR_LIST_OPTIONS))                

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
            helper.display_menu(STATUS_OPTION)
            status = helper.valid_option_input("Enter Status:", "Status", len(STATUS_OPTION))
            filter_data = [
                doctor for doctor in data
                if STATUS_OPTION[status] == doctor[COLUMN_STATUS]
            ]
        elif choice == DOCTOR_LIST_BACK:
            return
        else:
            print("Invalid option, please try again.")

        if not helper.ensure_records_exist(filter_data, 'doctor'):
            continue

        helper.print_divider(divider="*", color=constant.COLOR_YELLOW)
        print(f"\n Total doctors found: {len(filter_data)}")

        for doctor in filter_data:
            display_doctor_if_found(doctor, doctor[COLUMN_ID])


def update_doctor() -> None:
    data = load_data(constant.TABLE_DOCTOR)
    
    if not helper.ensure_records_exist(data, 'doctor'):
        return

    while True:
        doctor_id = helper.valid_input(
            placeholder="Enter Doctor Id:",
            name="Doctor",
            type="int"
        )
        doctor = helper.find_by_id(data, doctor_id)
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
            # print(STATUS_OPTION_PREVIEW)
            helper.display_menu(STATUS_OPTION)
            status = helper.valid_option_input("Enter Status:", "Status", len(STATUS_OPTION))
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
        doctor = helper.find_by_id(data, doctor_id)
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
                # print(STATUS_OPTION_PREVIEW)
                helper.display_menu(STATUS_OPTION)
                status = helper.valid_option_input("Enter Status:", "Status", len(STATUS_OPTION))
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

def display_doctor_if_found(doctor: constant.TYPE_DICT | None, doctor_id: int, visible_schedule: bool = False) -> None:
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
         
        if visible_schedule:
            helper.print_divider(color=constant.COLOR_GREEN)
            print("Schedule")

            schedules = doctor.get("schedule", [])

            if not schedules:
                print("No schedule found.")
            else:
                for schedule in schedules:
                    print(f"{'Day':<{LABEL_WIDTH}}: {schedule['day']}")
                    print(f"{'Start Time':<{LABEL_WIDTH}}: {schedule['start_time']}")
                    print(f"{'End Time':<{LABEL_WIDTH}}: {schedule['end_time']}")
                    print(f"{'Slot Duration':<{LABEL_WIDTH}}: {schedule['slot_duration']} minutes")
                    print()
             
























