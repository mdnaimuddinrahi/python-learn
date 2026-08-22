from . import constant 
from . import helper
from app.storage import load_data, save_data
from app.logger import logger
from datetime import datetime

PATIENT_MENU_ADD = 1
PATIENT_MENU_VIEW = 2
PATIENT_MENU_LIST = 3
PATIENT_MENU_UPDATE = 4
PATIENT_MENU_STATUS = 5
PATIENT_MENU_DELETE = 6
PATIENT_MENU_BACK = 7

MENU_PATIENT_MANAGE_OPTIONS = """
1. Add Patient
2. View Patient
3. Patient List
4. Update Patient
5. Patient Status
6. Patient Delete
7. Back
"""

COLUMN_ID = "id"
COLUMN_PATIENT_NUMBER = "patient_number"
COLUMN_NAME = "name"
COLUMN_DATE_OF_BIRTH = "date_of_birth"
COLUMN_GENDER = "gender"
COLUMN_PHONE = "phone"
COLUMN_EMAIL = "email"
COLUMN_ADDRESS = "address"
COLUMN_BLOOD_GROUP = "blood_group"
COLUMN_EMERGENCY_CONTACT_NAME = "emergency_contact_name"
COLUMN_EMERGENCY_CONTACT_PHONE = "emergency_contact_phone"
COLUMN_STATUS = "status"
COLUMN_CREATED_AT = "created_at"
COLUMN_UPDATED_AT = "updated_at"

GENDER_LIST_OPTIONS = """
1. Male.
2. Female.
3. Other.
"""
GENDER_OPTIONS = {
    1: "Male",
    2: "Female",
    3: "Other",
}
BLOOD_GROUP_LIST_OPTIONS = """
1. A+
2. A-
3. B+
4. B-
5. AB+
6. AB-
7. O+
8. O-
"""
BLOOD_GROUP_OPTIONS = {
    1: "A+",
    2: "A-",
    3: "B+",
    4: "B-",
    5: "AB+",
    6: "AB-",
    7: "O+",
    8: "O-",
}
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
LABEL_WIDTH = max(
    len("Patient ID"),
    len("Name"),
    len("Date of Birth"),
    len("Gender"),
    len("Phone"),
    len("Email"),
    len("Address"),
    len("Blood Group"),
    len("Emergency Contact Name"),
    len("Emergency Contact Phone"),
    len("Status"),
    len("Created At"),
    len("Updated At"),
) + 2

def manage_patient():
    helper.print_title("Patient Management")
    while True:
        print(MENU_PATIENT_MANAGE_OPTIONS)
        choice = helper.valid_option_input("Choose an option: ", name="Option", max_value=7)

        if choice == PATIENT_MENU_ADD:
            add_patient()          
        elif choice == PATIENT_MENU_VIEW:
            view_patient()  
        elif choice == PATIENT_MENU_LIST:
            patient_list()
        elif choice == PATIENT_MENU_UPDATE:
            update_patient()
        elif choice == PATIENT_MENU_STATUS:
            patient_status()
        elif choice == PATIENT_MENU_DELETE:
            patient_delete()
        elif choice == PATIENT_MENU_BACK:
            return
        else:
            print("Invalid option, please try again.")
MENU_PATIENT_LIST_OPTIONS = """
1. All List.
2. Search By Name.
3. Search By Email.
4. Search By Status.
5. Search By Phone.
6. Search By Address.
7. Back to Doctors Menu.
"""
PATIENT_LIST_ALL = 1
PATIENT_LIST_BY_NAME = 2
PATIENT_LIST_BY_EMAIL = 3
PATIENT_LIST_BY_STATUS = 4
PATIENT_LIST_BY_PHONE = 5
PATIENT_LIST_BY_ADDRESS = 6
PATIENT_LIST_BACK = 7

def patient_delete() -> None:
    data = load_data(constant.TABLE_PATIENT)

    if not helper.ensure_records_exist(data, 'patient'):
        return

    while True:
        patient_id = helper.valid_input(
            placeholder="Enter Patient Id:",
            name="Patient",
            type="int"
        )

        patient = helper.find_by_id(data, patient_id)

        display_patient_if_found(patient, patient_id)

        if patient is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message("Do you want to search again?")
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        should_delete = helper.confirm_input(
            helper.confirm_input_message("Do you want to delete this patient?")
        )

        if should_delete == constant.CONFIRM_YES:
            data.remove(patient)

            save_patient_record(
                constant.ACTION_DELETE,
                data,
                patient
            )

        return

def patient_status() -> None:
    data = load_data(constant.TABLE_PATIENT)

    if not helper.ensure_records_exist(data, 'patient'):
        return

    while True:
        patient_id = helper.valid_input(
            placeholder="Enter Patient Id:",
            name="Patient",
            type="int"
        )

        patient = helper.find_by_id(data, patient_id)

        display_patient_if_found(patient, patient_id)

        if patient is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message("Do you want to search again?")
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        should_update_status = helper.confirm_input(
            helper.confirm_input_message("Do you want to update status?")
        )

        if should_update_status == constant.CONFIRM_YES:
            print("Choose an option:")
            print(STATUS_OPTION_PREVIEW)

            status = helper.valid_option_input(
                "Enter Status:",
                "Status",
                len(STATUS_OPTION)
            )

            patient[COLUMN_STATUS] = STATUS_OPTION[status]

            current_date_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            patient[COLUMN_UPDATED_AT] = current_date_time

            save_patient_record(
                constant.ACTION_UPDATE,
                data,
                patient
            )

        return

def patient_list():
    data = load_data(constant.TABLE_PATIENT)

    if not helper.ensure_records_exist(data, 'patient'):
        return
        
    while True:
        print(MENU_PATIENT_LIST_OPTIONS)
        choice = helper.valid_option_input("Choose an option: ", name="Option", max_value=7)

        if choice == PATIENT_LIST_ALL:
            filter_data = data        
        elif choice ==PATIENT_LIST_BY_NAME:
            name = helper.valid_input(
                placeholder="Enter Patient Name: ", 
                name= "Patient Name",
                limit= 50)
            filter_data = [
                patient for patient in data
                if name.lower() in patient[COLUMN_NAME].lower()
            ]
        elif choice ==PATIENT_LIST_BY_EMAIL:
            email = helper.valid_input(
                placeholder="Enter Email:", 
                name="Email", 
                required=False,
                type="email")
            filter_data = [
                doctor for doctor in data
                if email.lower() in doctor[COLUMN_EMAIL].lower()
            ]
        elif choice ==PATIENT_LIST_BY_STATUS:
            print("Choose an option:")
            print(STATUS_OPTION_PREVIEW)
            status = helper.valid_option_input("Enter Status:", "Status", len(STATUS_OPTION))
            filter_data = [
                doctor for doctor in data
                if STATUS_OPTION[status] == doctor[COLUMN_STATUS]
            ]
        elif choice ==PATIENT_LIST_BY_PHONE:
            phone = helper.valid_input(
                placeholder="Enter Patient Phone: ",
                name="Patient Phone",
                limit=20,
                type="phone"
            )
            filter_data = [
                patient for patient in data
                if phone in patient[COLUMN_PHONE]
            ]
        elif choice == PATIENT_LIST_BY_ADDRESS:
            address = helper.valid_input(
                placeholder="Enter Address: ",
                name="Address",
                limit=100)
            search_words = address.lower().split()

            filter_data = [
                patient for patient in data
                if all(
                    word in patient[COLUMN_ADDRESS].lower()
                    for word in search_words
                )
            ]
        elif choice ==PATIENT_LIST_BACK:
            return
        else:
            print("Invalid option, please try again.")

        if not helper.ensure_records_exist(filter_data, 'patient'):
            continue
        helper.print_divider(divider="*", color=constant.COLOR_YELLOW)
        print(f"\n Total patients found: {len(filter_data)}")

        for patient in filter_data:
            display_patient_if_found(patient, patient[COLUMN_ID])

def add_patient():
    print('Please enter patient details')
    data = load_data(constant.TABLE_PATIENT)
    patient = {
        COLUMN_ID: helper.get_next_id(data),
        COLUMN_NAME: helper.valid_input(placeholder="Enter Name: ",name="Name",limit=30),
        COLUMN_DATE_OF_BIRTH: helper.valid_date_input(placeholder="Enter Date of Birth (YYYY-MM-DD): ",name="Date of Birth"),
        COLUMN_ADDRESS: helper.valid_input(placeholder="Enter Address: ",name="Address",limit=100),
    }
    phone = helper.valid_input(
        placeholder="Enter Phone:", 
        name="Phone", 
        required=False,
        type="phone")
    patient[COLUMN_PHONE] = phone or "-" 
    email = helper.valid_input(
        placeholder="Enter Email:", 
        name="Email", 
        required=False,
        type="email")
    patient[COLUMN_EMAIL] = email or "-"
                   
    print("Choose Gender option:")
    print(GENDER_LIST_OPTIONS)
    gender = helper.valid_option_input("Enter Gender:", "Gender", len(GENDER_OPTIONS))
    patient[COLUMN_GENDER] = GENDER_OPTIONS[gender]
    print("Choose Blood Group option:")
    print(BLOOD_GROUP_LIST_OPTIONS)
    blood_group = helper.valid_option_input("Enter Blood Group:", "Blood Group", len(BLOOD_GROUP_OPTIONS))
    patient[COLUMN_BLOOD_GROUP] = BLOOD_GROUP_OPTIONS[blood_group]
    patient[COLUMN_EMERGENCY_CONTACT_NAME] = helper.valid_input(
                                                    placeholder="Enter Emergency Contact Name: ",
                                                    name="Emergency Contact Name",
                                                    limit=30)
    emergency_contact_phone = helper.valid_input(
                                    placeholder="Enter Phone:", 
                                    name="Phone", 
                                    required=False,
                                    type="phone")
    patient[COLUMN_EMERGENCY_CONTACT_PHONE] = emergency_contact_phone or "-"
    print(STATUS_OPTION_PREVIEW)
    status = helper.valid_option_input("Enter Status:", "Status", len(STATUS_OPTION))
    patient[COLUMN_STATUS] = STATUS_OPTION[status]
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    patient[COLUMN_CREATED_AT] = current_date_time
    patient[COLUMN_UPDATED_AT] = "-"
    data.append(patient)
    save_patient_record(constant.ACTION_CREATE, data, patient)

def update_patient() -> None:
    data = load_data(constant.TABLE_PATIENT)

    while True:
        patient_id = helper.valid_input(
            placeholder="Enter Patient Id:",
            name="Patient",
            type="int"
        )

        patient = helper.find_by_id(data, patient_id)

        display_patient_if_found(patient, patient_id)

        if patient is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message("Do you want search again?")
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        is_updated = False

        # Name
        should_update_name = helper.confirm_input(
            helper.confirm_input_message("Do you want to update Name?")
        )

        if should_update_name == constant.CONFIRM_YES:
            patient[COLUMN_NAME] = helper.valid_input(
                placeholder="Enter Name: ",
                name="Name",
                limit=30
            )
            is_updated = True

        # Date of Birth
        should_update_date_of_birth = helper.confirm_input(
            helper.confirm_input_message("Do you want to update Date of Birth?")
        )

        if should_update_date_of_birth == constant.CONFIRM_YES:
            patient[COLUMN_DATE_OF_BIRTH] = helper.valid_date_input(
                placeholder="Enter Date of Birth (YYYY-MM-DD): ",
                name="Date of Birth"
            )
            is_updated = True

        # Address
        should_update_address = helper.confirm_input(
            helper.confirm_input_message("Do you want to update Address?")
        )

        if should_update_address == constant.CONFIRM_YES:
            patient[COLUMN_ADDRESS] = helper.valid_input(
                placeholder="Enter Address: ",
                name="Address",
                limit=100
            )
            is_updated = True

        # Phone
        should_update_phone = helper.confirm_input(
            helper.confirm_input_message("Do you want to update Phone?")
        )

        if should_update_phone == constant.CONFIRM_YES:
            phone = helper.valid_input(
                placeholder="Enter Phone: ",
                name="Phone",
                required=False,
                type="phone"
            )

            patient[COLUMN_PHONE] = phone or "-"
            is_updated = True

        # Email
        should_update_email = helper.confirm_input(
            helper.confirm_input_message("Do you want to update Email?")
        )

        if should_update_email == constant.CONFIRM_YES:
            email = helper.valid_input(
                placeholder="Enter Email: ",
                name="Email",
                required=False,
                type="email"
            )

            patient[COLUMN_EMAIL] = email or "-"
            is_updated = True

        # Gender
        should_update_gender = helper.confirm_input(
            helper.confirm_input_message("Do you want to update Gender?")
        )

        if should_update_gender == constant.CONFIRM_YES:
            print("Choose Gender option:")
            print(GENDER_LIST_OPTIONS)

            gender = helper.valid_option_input(
                "Enter Gender:",
                "Gender",
                len(GENDER_OPTIONS)
            )

            patient[COLUMN_GENDER] = GENDER_OPTIONS[gender]
            is_updated = True

        # Blood Group
        should_update_blood_group = helper.confirm_input(
            helper.confirm_input_message("Do you want to update Blood Group?")
        )

        if should_update_blood_group == constant.CONFIRM_YES:
            print("Choose Blood Group option:")
            print(BLOOD_GROUP_LIST_OPTIONS)

            blood_group = helper.valid_option_input(
                "Enter Blood Group:",
                "Blood Group",
                len(BLOOD_GROUP_OPTIONS)
            )

            patient[COLUMN_BLOOD_GROUP] = BLOOD_GROUP_OPTIONS[blood_group]
            is_updated = True

        # Emergency Contact Name
        should_update_emergency_contact_name = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Emergency Contact Name?"
            )
        )

        if should_update_emergency_contact_name == constant.CONFIRM_YES:
            patient[COLUMN_EMERGENCY_CONTACT_NAME] = helper.valid_input(
                placeholder="Enter Emergency Contact Name: ",
                name="Emergency Contact Name",
                limit=30
            )
            is_updated = True

        # Emergency Contact Phone
        should_update_emergency_contact_phone = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Emergency Contact Phone?"
            )
        )

        if should_update_emergency_contact_phone == constant.CONFIRM_YES:
            emergency_contact_phone = helper.valid_input(
                placeholder="Enter Phone: ",
                name="Phone",
                required=False,
                type="phone"
            )

            patient[COLUMN_EMERGENCY_CONTACT_PHONE] = (
                emergency_contact_phone or "-"
            )
            is_updated = True

        # Status
        should_update_status = helper.confirm_input(
            helper.confirm_input_message("Do you want to update Status?")
        )

        if should_update_status == constant.CONFIRM_YES:
            print(STATUS_OPTION_PREVIEW)

            status = helper.valid_option_input(
                "Enter Status:",
                "Status",
                len(STATUS_OPTION)
            )

            patient[COLUMN_STATUS] = STATUS_OPTION[status]
            is_updated = True

        # Updated At
        if is_updated:
            current_date_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            patient[COLUMN_UPDATED_AT] = current_date_time

            save_patient_record(
                constant.ACTION_UPDATE,
                data,
                patient
            )

        search_again = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want update anything else?"
            )
        )

        if search_again == constant.CONFIRM_NO:
            return

def view_patient():
    data = load_data(constant.TABLE_PATIENT)

    if not helper.ensure_records_exist(data, 'patient'):
        return
    while True:
        patient_id = helper.valid_input(
            placeholder="Enter Patient Id:",
            name="Patient",
            type="int"
        )
        doctor = helper.find_by_id(data, patient_id)
        display_patient_if_found(doctor, patient_id)

        search_again = helper.confirm_input(
            helper.confirm_input_message("Do you want search again?")
        )        

        if search_again == constant.CONFIRM_NO:
            return        

def save_patient_record(action: str, data: constant.TYPE_LIST, patient: constant.TYPE_DICT) -> None:
    try:
        save_data(constant.TABLE_PATIENT, data)
    except OSError:
        logger.exception(f"Failed to {action} patient data.")
        return
    print(f"\nPatient {action} successfully.")
    display_patient_if_found(patient, patient_id=patient[COLUMN_ID])

def display_patient_if_found(
    patient: constant.TYPE_DICT | None,
    patient_id: int
) -> None:
    if patient is None:
        helper.print_divider(color=constant.COLOR_RED)
        print(f"Patient Not found with ID {patient_id}\n")
    else:
        print()
        helper.print_divider(color=constant.COLOR_GREEN)

        print(f"{'Patient ID':<{LABEL_WIDTH}}: {patient[COLUMN_ID]}")
        print(f"{'Name':<{LABEL_WIDTH}}: {patient[COLUMN_NAME]}")
        print(f"{'Date of Birth':<{LABEL_WIDTH}}: {patient[COLUMN_DATE_OF_BIRTH]}")
        print(f"{'Gender':<{LABEL_WIDTH}}: {patient[COLUMN_GENDER]}")
        print(f"{'Phone':<{LABEL_WIDTH}}: {patient[COLUMN_PHONE]}")
        print(f"{'Email':<{LABEL_WIDTH}}: {patient[COLUMN_EMAIL]}")
        print(f"{'Address':<{LABEL_WIDTH}}: {patient[COLUMN_ADDRESS]}")
        print(f"{'Blood Group':<{LABEL_WIDTH}}: {patient[COLUMN_BLOOD_GROUP]}")
        print(
            f"{'Emergency Contact Name':<{LABEL_WIDTH}}: "
            f"{patient[COLUMN_EMERGENCY_CONTACT_NAME]}"
        )
        print(
            f"{'Emergency Contact Phone':<{LABEL_WIDTH}}: "
            f"{patient[COLUMN_EMERGENCY_CONTACT_PHONE]}"
        )
        print(f"{'Status':<{LABEL_WIDTH}}: {patient[COLUMN_STATUS]}")
        print(f"{'Created At':<{LABEL_WIDTH}}: {patient[COLUMN_CREATED_AT]}")
        print(f"{'Updated At':<{LABEL_WIDTH}}: {patient[COLUMN_UPDATED_AT]}")

        print()
        helper.print_divider(color=constant.COLOR_GREEN)

