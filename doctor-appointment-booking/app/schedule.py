from . import constant 
from . import helper
from app.storage import load_data, save_data
from app.logger import logger
from datetime import datetime
from app.doctor import display_doctor_if_found, COLUMN_SCHEDULE, save_doctor_record

SCHEDULE_MENU_ADD = 1
SCHEDULE_MENU_VIEW = 2
SCHEDULE_MENU_UPDATE = 3
SCHEDULE_MENU_STATUS = 4
SCHEDULE_DELETE = 5
SCHEDULE_MENU_BACK = 6

MENU_SCHEDULE_MANAGE_OPTIONS = {
    SCHEDULE_MENU_ADD: "Add Schedule",
    SCHEDULE_MENU_VIEW: "View Schedule",
    SCHEDULE_MENU_UPDATE: "Update Schedule",
    SCHEDULE_MENU_STATUS: "Schedule Status",
    SCHEDULE_DELETE: "Schedule Delete",
    SCHEDULE_MENU_BACK: "Back",
}

COLUMN_ID = "id"
COLUMN_DAY = "day"
COLUMN_START_TIME = "start_time"
COLUMN_END_TIME = "end_time"
COLUMN_SLOT_DURATION = "slot_duration"
COLUMN_STATUS = "status"
COLUMN_CREATED_AT = "created_at"
COLUMN_UPDATED_AT = "updated_at"

SCHEDULE_STATUSES = {
    1: "Available",
    2: "Blocked",
}

DAYS_OF_WEEK = {
    1: "Saturday",
    2: "Sunday",
    3: "Monday",
    4: "Tuesday",
    5: "Wednesday",
    6: "Thursday",
    7: "Friday",
}

SCHEDULE_LABEL_WIDTH = max(
    len("Schedule ID"),
    len("Day"),
    len("Start Time"),
    len("End Time"),
    len("Slot Duration"),
    len("Status"),
    len("Created At"),
    len("Updated At"),
) + 2

def manage_schedule():
    helper.print_title("Schedule Management")
    while True:
        helper.display_menu(MENU_SCHEDULE_MANAGE_OPTIONS)

        choice = helper.valid_option_input("Choose an option: ", name="Option", max_value=len(MENU_SCHEDULE_MANAGE_OPTIONS))

        if choice == SCHEDULE_MENU_ADD:
            add_schedule()
        elif choice == SCHEDULE_MENU_VIEW:
            view_schedule()
        elif choice == SCHEDULE_MENU_UPDATE:
            update_schedule()
        elif choice == SCHEDULE_MENU_STATUS:
            schedule_status()
        elif choice == SCHEDULE_DELETE:
            schedule_delete()
        elif choice == SCHEDULE_MENU_BACK:
            return
        else:
            print("Invalid option, please try again.")

def add_schedule() -> None:
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

        print("\nChoose Day:")
        helper.display_menu(DAYS_OF_WEEK)

        day = helper.valid_option_input(
            "Enter Day:",
            "Day",
            len(DAYS_OF_WEEK)
        )

        print("\nEnter Schedule Details:")

        start_time = helper.valid_time_input(
            placeholder="Enter Start Time (HH:MM): ",
            name="Start Time"
        )

        end_time = helper.valid_time_input(
            placeholder="Enter End Time (HH:MM): ",
            name="End Time"
        )

        slot_duration = helper.valid_input(
            placeholder="Enter Slot Duration (minutes): ",
            name="Slot Duration",
            type="int"
        )

        print("\nChoose Schedule Status:")
        helper.display_menu(SCHEDULE_STATUSES)

        status = helper.valid_option_input(
            "Enter Status:",
            "Status",
            len(SCHEDULE_STATUSES)
        )

        current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        schedules = doctor.get(COLUMN_SCHEDULE, [])

        schedule = {
            "id": helper.get_next_id(schedules),
            "day": DAYS_OF_WEEK[day],
            "start_time": start_time,
            "end_time": end_time,
            "slot_duration": slot_duration,
            "status": SCHEDULE_STATUSES[status],
            "created_at": current_date_time,
            "updated_at": "-"
        }

        if COLUMN_SCHEDULE not in doctor:
            doctor[COLUMN_SCHEDULE] = []

        doctor[COLUMN_SCHEDULE].append(schedule)

        save_doctor_record(
            constant.ACTION_UPDATE,
            data,
            doctor
        )

        print("Schedule added successfully.")
        return

def view_schedule() -> None:
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

        if doctor is None:
            display_doctor_if_found(doctor, doctor_id)

            search_again = helper.confirm_input(
                helper.confirm_input_message("Do you want search again?")
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        display_doctor_if_found(doctor, doctor_id)

        schedules = doctor.get(COLUMN_SCHEDULE, [])

        if not schedules:
            print("No schedule found for this doctor.")
        else:
            print("\nDoctor Schedule")
            helper.print_divider(color=constant.COLOR_GREEN)
            for index, schedule in enumerate(schedules, start=1):
                display_schedule(schedule)

        search_again = helper.confirm_input(
            helper.confirm_input_message("Do you want search again?")
        )

        if search_again == constant.CONFIRM_NO:
            return

def update_schedule() -> None:
    data = load_data(constant.TABLE_DOCTOR)

    if not helper.ensure_records_exist(data, 'doctor'):
        return

    while True:
        # Doctor
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

        # Schedule
        schedules = doctor.get(COLUMN_SCHEDULE, [])

        if not schedules:
            print("No schedule found for this doctor.")
            return

        schedule_id = helper.valid_input(
            placeholder="Enter Schedule Id:",
            name="Schedule",
            type="int"
        )

        schedule = helper.find_by_id(schedules, schedule_id)

        if schedule is None:
            print(f"Schedule not found with ID {schedule_id}.")

            search_again = helper.confirm_input(
                helper.confirm_input_message(
                    "Do you want search again?"
                )
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        is_updated = False

        # Day
        should_update_day = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Day?"
            )
        )

        if should_update_day == constant.CONFIRM_YES:
            print("\nChoose Day:")
            helper.display_menu(DAYS_OF_WEEK)

            day = helper.valid_option_input(
                "Enter Day:",
                "Day",
                len(DAYS_OF_WEEK)
            )

            schedule["day"] = DAYS_OF_WEEK[day]
            is_updated = True

        # Start Time
        should_update_start_time = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Start Time?"
            )
        )

        if should_update_start_time == constant.CONFIRM_YES:
            schedule["start_time"] = helper.valid_time_input(
                placeholder="Enter Start Time (HH:MM): ",
                name="Start Time"
            )
            is_updated = True

        # End Time
        should_update_end_time = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update End Time?"
            )
        )

        if should_update_end_time == constant.CONFIRM_YES:
            schedule["end_time"] = helper.valid_time_input(
                placeholder="Enter End Time (HH:MM): ",
                name="End Time"
            )
            is_updated = True

        # Slot Duration
        should_update_slot_duration = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Slot Duration?"
            )
        )

        if should_update_slot_duration == constant.CONFIRM_YES:
            schedule["slot_duration"] = helper.valid_input(
                placeholder="Enter Slot Duration (minutes): ",
                name="Slot Duration",
                type="int"
            )
            is_updated = True

        # Status
        should_update_status = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Status?"
            )
        )

        if should_update_status == constant.CONFIRM_YES:
            print("\nChoose Schedule Status:")
            helper.display_menu(SCHEDULE_STATUSES)

            status = helper.valid_option_input(
                "Enter Status:",
                "Status",
                len(SCHEDULE_STATUSES)
            )

            schedule["status"] = SCHEDULE_STATUSES[status]
            is_updated = True

        # Updated At
        if is_updated:
            current_date_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            schedule["updated_at"] = current_date_time

            save_doctor_record(
                constant.ACTION_UPDATE,
                data,
                doctor
            )

            print("Schedule updated successfully.")

        search_again = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want update anything else?"
            )
        )

        if search_again == constant.CONFIRM_NO:
            return

def schedule_status() -> None:
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

        if doctor is None:
            display_doctor_if_found(doctor, doctor_id)

            search_again = helper.confirm_input(
                helper.confirm_input_message("Do you want search again?")
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        display_doctor_if_found(doctor, doctor_id)

        schedules = doctor.get(COLUMN_SCHEDULE, [])

        if not schedules:
            print("No schedule found for this doctor.")
            return

        schedule_id = helper.valid_input(
            placeholder="Enter Schedule Id:",
            name="Schedule",
            type="int"
        )

        schedule = helper.find_by_id(schedules, schedule_id)

        if schedule is None:
            print(f"Schedule not found with ID {schedule_id}.")

            search_again = helper.confirm_input(
                helper.confirm_input_message(
                    "Do you want search again?"
                )
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        display_schedule(schedule)

        print("\nChoose Schedule Status:")
        helper.display_menu(SCHEDULE_STATUSES)

        status = helper.valid_option_input(
            "Enter Status:",
            "Status",
            len(SCHEDULE_STATUSES)
        )

        schedule["status"] = SCHEDULE_STATUSES[status]

        current_date_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        schedule["updated_at"] = current_date_time

        save_doctor_record(
            constant.ACTION_UPDATE,
            data,
            doctor
        )

        print("Schedule status updated successfully.")

        search_again = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want update another schedule status?"
            )
        )

        if search_again == constant.CONFIRM_NO:
            return

def display_schedule(schedule: constant.TYPE_DICT) -> None:
    helper.print_divider(color=constant.COLOR_GREEN)

    print(f"{'Schedule ID':<{SCHEDULE_LABEL_WIDTH}}: {schedule['id']}")
    print(f"{'Day':<{SCHEDULE_LABEL_WIDTH}}: {schedule['day']}")
    print(f"{'Start Time':<{SCHEDULE_LABEL_WIDTH}}: {schedule['start_time']}")
    print(f"{'End Time':<{SCHEDULE_LABEL_WIDTH}}: {schedule['end_time']}")
    print(
        f"{'Slot Duration':<{SCHEDULE_LABEL_WIDTH}}: "
        f"{schedule['slot_duration']} minutes"
    )
    print(f"{'Status':<{SCHEDULE_LABEL_WIDTH}}: {schedule['status']}")
    print(f"{'Created At':<{SCHEDULE_LABEL_WIDTH}}: {schedule['created_at']}")
    print(f"{'Updated At':<{SCHEDULE_LABEL_WIDTH}}: {schedule['updated_at']}")

    helper.print_divider(color=constant.COLOR_GREEN)

def schedule_delete() -> None:
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

        if doctor is None:
            display_doctor_if_found(doctor, doctor_id)

            search_again = helper.confirm_input(
                helper.confirm_input_message("Do you want search again?")
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        display_doctor_if_found(doctor, doctor_id)

        schedules = doctor.get(COLUMN_SCHEDULE, [])

        if not schedules:
            print("No schedule found for this doctor.")
            return

        schedule_id = helper.valid_input(
            placeholder="Enter Schedule Id:",
            name="Schedule",
            type="int"
        )

        schedule = helper.find_by_id(schedules, schedule_id)

        if schedule is None:
            print(f"Schedule not found with ID {schedule_id}.")

            search_again = helper.confirm_input(
                helper.confirm_input_message(
                    "Do you want search again?"
                )
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        display_schedule(schedule)

        should_delete = helper.confirm_input(
            helper.confirm_input_message(
                "Are you sure you want to delete this schedule?"
            )
        )

        if should_delete == constant.CONFIRM_NO:
            print("Schedule deletion cancelled.")
            return

        schedules.remove(schedule)

        save_doctor_record(
            constant.ACTION_UPDATE,
            data,
            doctor
        )

        print("Schedule deleted successfully.")

        delete_another = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to delete another schedule?"
            )
        )

        if delete_another == constant.CONFIRM_NO:
            return

