from . import constant 
from . import helper
from app.storage import load_data, save_data
from app.logger import logger
from datetime import datetime
from app.patient import display_patient_if_found, COLUMN_NAME as COLUMN_PATIENT_NAME
from app.doctor import display_doctor_if_found, COLUMN_SCHEDULE, COLUMN_NAME as COLUMN_DOCTOR_NAME
import app.schedule
from datetime import datetime, timedelta

APPOINTMENT_MENU_ADD = 1
APPOINTMENT_MENU_VIEW = 2
APPOINTMENT_MENU_LIST = 3
APPOINTMENT_MENU_UPDATE = 4
APPOINTMENT_MENU_STATUS = 5
APPOINTMENT_MENU_CANCEL = 6
APPOINTMENT_MENU_BACK = 7

MENU_APPOINTMENT_MANAGE_OPTIONS = {
    APPOINTMENT_MENU_ADD: "Create Appointment",
    APPOINTMENT_MENU_VIEW: "View Appointment",
    APPOINTMENT_MENU_LIST: "Appointment List",
    APPOINTMENT_MENU_UPDATE: "Update Appointment",
    APPOINTMENT_MENU_STATUS: "Appointment Status",
    APPOINTMENT_MENU_CANCEL: "Cancel Appointment",
    APPOINTMENT_MENU_BACK: "Back",
}

STATUS_SCHEDULED = 1
STATUS_CONFIRMED = 2
STATUS_COMPLETED = 3
STATUS_CANCELLED = 4
STATUS_NO_SHOW = 5

APPOINTMENT_STATUSES = {
    STATUS_SCHEDULED: "Scheduled",
    STATUS_CONFIRMED: "Confirmed",
    STATUS_COMPLETED: "Completed",
    STATUS_CANCELLED: "Cancelled",
    STATUS_NO_SHOW: "No Show",
}

COLUMN_ID = "id"
COLUMN_PATIENT_ID = "patient_id"
COLUMN_DOCTOR_ID = "doctor_id"
COLUMN_APPOINTMENT_DATE = "appointment_date"
COLUMN_APPOINTMENT_TIME = "appointment_time"
COLUMN_STATUS = "status"
COLUMN_REASON = "reason"
COLUMN_NOTES = "notes"
COLUMN_CREATED_AT = "created_at"
COLUMN_UPDATED_AT = "updated_at"

def manage_appointment():
    helper.print_title("Appointment Management")

    while True:
        helper.display_menu(MENU_APPOINTMENT_MANAGE_OPTIONS)

        choice = helper.valid_option_input(
            "Choose an option: ",
            name="Option",
            max_value=len(MENU_APPOINTMENT_MANAGE_OPTIONS)
        )

        if choice == APPOINTMENT_MENU_ADD:
            add_appointment()

        elif choice == APPOINTMENT_MENU_VIEW:
            view_appointment()

        elif choice == APPOINTMENT_MENU_LIST:
            appointment_list()

        elif choice == APPOINTMENT_MENU_UPDATE:
            update_appointment()

        elif choice == APPOINTMENT_MENU_STATUS:
            appointment_status()

        elif choice == APPOINTMENT_MENU_CANCEL:
            cancel_appointment()

        elif choice == APPOINTMENT_MENU_BACK:
            return

        else:
            print("Invalid option, please try again.")

def add_appointment() -> None:
    patient_data = load_data(constant.TABLE_PATIENT)

    if not helper.ensure_records_exist(patient_data, 'patient'):
        return

    doctor_data = load_data(constant.TABLE_DOCTOR)

    if not helper.ensure_records_exist(doctor_data, 'doctor'):
        return

    appointment_data = load_data(constant.TABLE_APPOINTMENT)

    while True:
        # Patient
        patient_id = helper.valid_input(
            placeholder="Enter Patient Id:",
            name="Patient",
            type="int"
        )

        patient = helper.find_by_id(
            patient_data,
            patient_id
        )

        display_patient_if_found(
            patient,
            patient_id
        )

        if patient is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message(
                    "Do you want search again?"
                )
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

#         # Doctor
        doctor_id = helper.valid_input(
            placeholder="Enter Doctor Id:",
            name="Doctor",
            type="int"
        )

        doctor = helper.find_by_id(
            doctor_data,
            doctor_id
        )

        display_doctor_if_found(
            doctor,
            doctor_id
        )

        if doctor is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message(
                    "Do you want search again?"
                )
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        schedules = doctor.get(
            COLUMN_SCHEDULE,
            []
        )

        if not schedules:
            print("No schedule found for this doctor.")
            return

        # Appointment date
        appointment_date = helper.valid_date_input(
            placeholder="Enter Appointment Date (YYYY-MM-DD): ",
            name="Appointment Date"
        )

        selected_date = datetime.strptime(
            appointment_date,
            "%Y-%m-%d"
        ).date()

        today = datetime.now().date()

        if selected_date < today:
            print(
                "Appointment date cannot be in the past."
            )
            continue

        # check Same patient + same doctor + same day

        if has_patient_doctor_same_day(
            appointment_data,
            patient_id,
            doctor_id,
            appointment_date
        ):
            print(
                "This patient already has an appointment "
                "with this doctor on this date."
            )
            return
        appointment_day = selected_date.strftime(
            "%A"
        )


        # Find doctor's schedule for selected day
        doctor_schedule = None

        for schedule in schedules:
            if (
                schedule[app.schedule.COLUMN_DAY] == appointment_day
                and schedule[app.schedule.COLUMN_STATUS] == app.schedule.SCHEDULE_STATUSES[app.schedule.STATUS_AVAILABLE]
            ):
                doctor_schedule = schedule
                break

        if doctor_schedule is None:
            print(
                f"Doctor has no available schedule on "
                f"{appointment_day}."
            )
            return

        # Generate slots
        slots = generate_time_slots(
            doctor_schedule[app.schedule.COLUMN_START_TIME],
            doctor_schedule[app.schedule.COLUMN_END_TIME],
            doctor_schedule[app.schedule.COLUMN_SLOT_DURATION]
        )

        if not slots:
            print(
                "No appointment slots available "
                "for this schedule."
            )
            return

        # Remove already booked slots
        booked_doctor_slots = []

        for appointment in appointment_data:
            if is_appointment_cancelled(
                appointment
            ):
                continue

            if (
                appointment[
                    COLUMN_DOCTOR_ID
                ] == doctor_id
                and appointment[
                    COLUMN_APPOINTMENT_DATE
                ] == appointment_date
            ):
                booked_doctor_slots.append(
                    appointment[
                        COLUMN_APPOINTMENT_TIME
                    ]
                )


        available_slots = []

        for slot in slots:
            if slot in booked_doctor_slots:
                continue

            if has_patient_time_conflict(
                appointment_data,
                patient_id,
                appointment_date,
                slot
            ):
                continue

            available_slots.append(slot)

        if not available_slots:
            print(
                "No available appointment slots "
                "for this date."
            )
            return

        # Display slots
        slot_options = {
            index + 1: slot
            for index, slot in enumerate(available_slots)
        }

        print("\nAvailable Appointment Slots:")
        helper.display_menu(slot_options)

        slot_choice = helper.valid_option_input(
            "Choose Time Slot: ",
            "Time Slot",
            len(slot_options)
        )

        appointment_time = slot_options[slot_choice]

        if has_doctor_appointment(
            appointment_data,
            doctor_id,
            appointment_date,
            appointment_time
        ):
            print(
                "This time slot has already been "
                "booked for this doctor."
            )
            continue

        if has_patient_time_conflict(
            appointment_data,
            patient_id,
            appointment_date,
            appointment_time
        ):
            print(
                "This patient already has an appointment "
                "at this time on this date."
            )
            continue

        if has_patient_doctor_same_day(
            appointment_data,
            patient_id,
            doctor_id,
            appointment_date
        ):
            print(
                "This patient already has an appointment "
                "with this doctor on this date."
            )
            continue

        # Reason
        reason = helper.valid_input(
            placeholder="Enter Appointment Reason: ",
            name="Reason",
            limit=100
        )

        # Notes
        notes = helper.valid_input(
            placeholder="Enter Notes: ",
            name="Notes",
            required=False,
            limit=200
        )

        current_date_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        appointment = {
            COLUMN_ID: helper.get_next_id(appointment_data),
            COLUMN_PATIENT_ID: patient_id,
            COLUMN_DOCTOR_ID: doctor_id,
            COLUMN_APPOINTMENT_DATE: appointment_date,
            COLUMN_APPOINTMENT_TIME: appointment_time,
            COLUMN_STATUS: APPOINTMENT_STATUSES[1],
            COLUMN_REASON: reason,
            COLUMN_NOTES: notes or "-",
            COLUMN_CREATED_AT: current_date_time,
            COLUMN_UPDATED_AT: "-"
        }

        appointment_data.append(appointment)

        save_appointment_record(
            constant.ACTION_CREATE,
            appointment_data,
            appointment
        )

        print("Appointment created successfully.")

        return

def save_appointment_record(action: str, data: constant.TYPE_LIST, appointment: constant.TYPE_DICT) -> None:
    try:
        save_data(constant.TABLE_APPOINTMENT, data)
    except OSError:
        logger.exception(f"Failed to {action} appointment data.")
        return
    print(f"\nAppointment {action} successfully.")
    display_appointment_if_found(appointment, appointment_id=appointment[COLUMN_ID])

LABEL_WIDTH = max(
    len("Appointment ID"),
    len("Patient ID"),
    len("Patient Name"),
    len("Doctor ID"),
    len("Doctor Name"),
    len("Appointment Date"),
    len("Appointment Time"),
    len("Status"),
    len("Reason"),
    len("Notes"),
    len("Created At"),
    len("Updated At"),
) + 2

def display_appointment_if_found(
    appointment: constant.TYPE_DICT | None,
    appointment_id: int
) -> None:
    if appointment is None:
        helper.print_divider(color=constant.COLOR_RED)
        print(f"Appointment Not found with ID {appointment_id}\n")
        return

    patient_data = load_data(constant.TABLE_PATIENT)
    doctor_data = load_data(constant.TABLE_DOCTOR)

    patient = helper.find_by_id(
        patient_data,
        appointment[COLUMN_PATIENT_ID]
    )

    doctor = helper.find_by_id(
        doctor_data,
        appointment[COLUMN_DOCTOR_ID]
    )

    print()
    helper.print_divider(color=constant.COLOR_GREEN)

    print(
        f"{'Appointment ID':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_ID]}"
    )
    print(
        f"{'Patient ID':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_PATIENT_ID]}"
    )
    print(
        f"{'Patient Name':<{LABEL_WIDTH}}: "
        f"{patient[COLUMN_PATIENT_NAME] if patient else '-'}"
    )
    print(
        f"{'Doctor ID':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_DOCTOR_ID]}"
    )
    print(
        f"{'Doctor Name':<{LABEL_WIDTH}}: "
        f"{doctor[COLUMN_DOCTOR_NAME] if doctor else '-'}"
    )
    print(
        f"{'Appointment Date':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_APPOINTMENT_DATE]}"
    )
    print(
        f"{'Appointment Time':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_APPOINTMENT_TIME]}"
    )
    print(
        f"{'Status':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_STATUS]}"
    )
    print(
        f"{'Reason':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_REASON]}"
    )
    print(
        f"{'Notes':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_NOTES]}"
    )
    print(
        f"{'Created At':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_CREATED_AT]}"
    )
    print(
        f"{'Updated At':<{LABEL_WIDTH}}: "
        f"{appointment[COLUMN_UPDATED_AT]}"
    )

    print()
    helper.print_divider(color=constant.COLOR_GREEN)


def generate_time_slots(
    start_time: str,
    end_time: str,
    slot_duration: int
) -> list[str]:
    slots = []

    current_time = datetime.strptime(
        start_time,
        "%H:%M"
    )

    final_time = datetime.strptime(
        end_time,
        "%H:%M"
    )

    while current_time < final_time:
        next_time = current_time + timedelta(
            minutes=slot_duration
        )

        # Do not create a slot that extends beyond the schedule.
        if next_time > final_time:
            break

        slots.append(
            current_time.strftime("%H:%M")
        )

        current_time = next_time

    return slots

def is_appointment_cancelled(appointment: constant.TYPE_DICT) -> bool:
    return (appointment[COLUMN_STATUS] == APPOINTMENT_STATUSES[STATUS_CANCELLED])

def has_doctor_appointment(
    appointments: constant.TYPE_LIST,
    doctor_id: int,
    appointment_date: str,
    appointment_time: str
) -> bool:
    for appointment in appointments:
        if is_appointment_cancelled(appointment):
            continue

        if (
            appointment[COLUMN_DOCTOR_ID] == doctor_id and 
            appointment[COLUMN_APPOINTMENT_DATE] == appointment_date and 
            appointment[COLUMN_APPOINTMENT_TIME] == appointment_time
        ):
            return True

    return False

def has_patient_time_conflict(
    appointments: constant.TYPE_LIST,
    patient_id: int,
    appointment_date: str,
    appointment_time: str
) -> bool:
    for appointment in appointments:
        if is_appointment_cancelled(appointment):
            continue

        if (
            appointment[COLUMN_PATIENT_ID] == patient_id and 
            appointment[COLUMN_APPOINTMENT_DATE] == appointment_date and 
            appointment[COLUMN_APPOINTMENT_TIME] == appointment_time
        ):
            return True

    return False

def has_patient_doctor_same_day(
    appointments: constant.TYPE_LIST,
    patient_id: int,
    doctor_id: int,
    appointment_date: str
) -> bool:
    for appointment in appointments:
        if is_appointment_cancelled(appointment):
            continue

        if (
            appointment[COLUMN_PATIENT_ID] == patient_id and 
            appointment[COLUMN_DOCTOR_ID] == doctor_id and 
            appointment[COLUMN_APPOINTMENT_DATE] == appointment_date
        ):
            return True

    return False

def update_appointment() -> None:
    appointment_data = load_data(constant.TABLE_APPOINTMENT)

    if not helper.ensure_records_exist(appointment_data, 'appointment'):
        return

    patient_data = load_data(constant.TABLE_PATIENT)

    if not helper.ensure_records_exist(patient_data, 'patient'):
        return

    doctor_data = load_data(constant.TABLE_DOCTOR)

    if not helper.ensure_records_exist(doctor_data, 'doctor'):
        return

    while True:
        appointment_id = helper.valid_input(
            placeholder="Enter Appointment Id:",
            name="Appointment",
            type="int"
        )

        appointment = helper.find_by_id(
            appointment_data,
            appointment_id
        )

        display_appointment_if_found(
            appointment,
            appointment_id
        )

        if appointment is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message(
                    "Do you want search again?"
                )
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        is_updated = False

        # ---------------------------------------------------------
        # Patient
        # ---------------------------------------------------------
        should_update_patient = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Patient?"
            )
        )

        if should_update_patient == constant.CONFIRM_YES:
            patient_id = helper.valid_input(
                placeholder="Enter Patient Id:",
                name="Patient",
                type="int"
            )

            patient = helper.find_by_id(
                patient_data,
                patient_id
            )

            display_patient_if_found(
                patient,
                patient_id
            )

            if patient is None:
                print(
                    "Patient was not changed."
                )
            else:
                appointment[
                    COLUMN_PATIENT_ID
                ] = patient_id

                is_updated = True

        should_update_doctor = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Doctor?"
            )
        )

        if should_update_doctor == constant.CONFIRM_YES:
            doctor_id = helper.valid_input(
                placeholder="Enter Doctor Id:",
                name="Doctor",
                type="int"
            )

            doctor = helper.find_by_id(
                doctor_data,
                doctor_id
            )

            display_doctor_if_found(
                doctor,
                doctor_id
            )

            if doctor is None:
                print("Doctor was not changed.")
            else:
                appointment[COLUMN_DOCTOR_ID] = doctor_id
                is_updated = True

        should_update_date = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Appointment Date?"
            )
        )

        if should_update_date == constant.CONFIRM_YES:
            appointment_date = helper.valid_date_input(
                placeholder=(
                    "Enter Appointment Date "
                    "(YYYY-MM-DD): "
                ),
                name="Appointment Date"
            )

            selected_date = datetime.strptime(
                appointment_date,
                "%Y-%m-%d"
            ).date()

            today = datetime.now().date()

            if selected_date < today:
                print(
                    "Appointment date cannot be "
                    "in the past."
                )
            else:
                appointment[COLUMN_APPOINTMENT_DATE] = appointment_date
                is_updated = True

        should_update_time = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Appointment Time?"
            )
        )

        if should_update_time == constant.CONFIRM_YES:
            current_doctor_id = appointment[COLUMN_DOCTOR_ID]

            current_appointment_date = appointment[COLUMN_APPOINTMENT_DATE]

            doctor = helper.find_by_id(
                doctor_data,
                current_doctor_id
            )

            if doctor is None:
                print(
                    "Doctor not found. "
                    "Appointment time was not changed."
                )
            else:
                schedules = doctor.get(
                    COLUMN_SCHEDULE,
                    []
                )

                selected_date = datetime.strptime(
                    current_appointment_date,
                    "%Y-%m-%d"
                ).date()
                appointment_day = selected_date.strftime("%A")
                doctor_schedule = None

                for schedule in schedules:
                    if (
                        schedule[app.schedule.COLUMN_DAY] == appointment_day and 
                        schedule[app.schedule.COLUMN_STATUS] == app.schedule.SCHEDULE_STATUSES[app.schedule.STATUS_AVAILABLE]
                    ):
                        doctor_schedule = schedule
                        break

                if doctor_schedule is None:
                    print(
                        f"Doctor has no available "
                        f"schedule on {appointment_day}."
                    )
                else:
                    slots = generate_time_slots(
                        doctor_schedule[app.schedule.COLUMN_START_TIME],
                        doctor_schedule[app.schedule.COLUMN_END_TIME],
                        doctor_schedule[app.schedule.COLUMN_SLOT_DURATION]
                    )

                    # Remove doctor's occupied slots,
                    # excluding the current appointment.
                    available_slots = []

                    for slot in slots:
                        if slot == appointment[
                            COLUMN_APPOINTMENT_TIME
                        ]:
                            available_slots.append(slot)
                            continue

                        if has_doctor_appointment(
                            appointment_data,
                            current_doctor_id,
                            current_appointment_date,
                            slot
                        ):
                            continue

                        if has_patient_time_conflict(
                            appointment_data,
                            appointment[
                                COLUMN_PATIENT_ID
                            ],
                            current_appointment_date,
                            slot
                        ):
                            continue

                        available_slots.append(slot)

                    if not available_slots:
                        print(
                            "No available appointment "
                            "slots for this date."
                        )
                    else:
                        slot_options = {
                            index + 1: slot
                            for index, slot
                            in enumerate(
                                available_slots
                            )
                        }

                        print(
                            "\nAvailable Appointment Slots:"
                        )

                        helper.display_menu(
                            slot_options
                        )

                        slot_choice = (
                            helper.valid_option_input(
                                "Choose Time Slot: ",
                                "Time Slot",
                                len(slot_options)
                            )
                        )

                        new_time = slot_options[
                            slot_choice
                        ]

                        appointment[
                            COLUMN_APPOINTMENT_TIME
                        ] = new_time

                        is_updated = True

        should_update_reason = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Reason?"
            )
        )

        if should_update_reason == constant.CONFIRM_YES:
            appointment[
                COLUMN_REASON
            ] = helper.valid_input(
                placeholder="Enter Appointment Reason: ",
                name="Reason",
                limit=100
            )

            is_updated = True

        should_update_notes = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update Notes?"
            )
        )

        if should_update_notes == constant.CONFIRM_YES:
            notes = helper.valid_input(
                placeholder="Enter Notes: ",
                name="Notes",
                required=False,
                limit=200
            )
            appointment[COLUMN_NOTES] = notes or "-"
            is_updated = True

        if is_updated:
            current_patient_id = appointment[COLUMN_PATIENT_ID]
            current_doctor_id = appointment[COLUMN_DOCTOR_ID]
            current_date = appointment[COLUMN_APPOINTMENT_DATE]
            current_time = appointment[COLUMN_APPOINTMENT_TIME]
            conflict_found = False

            for existing_appointment in appointment_data:
                if (existing_appointment[COLUMN_ID] == appointment_id):
                    continue

                if is_appointment_cancelled(existing_appointment):
                    continue

                existing_patient_id = (existing_appointment[COLUMN_PATIENT_ID])
                existing_doctor_id = (existing_appointment[COLUMN_DOCTOR_ID])
                existing_date = (existing_appointment[COLUMN_APPOINTMENT_DATE])
                existing_time = (existing_appointment[COLUMN_APPOINTMENT_TIME])

                if (
                    existing_doctor_id == current_doctor_id and 
                    existing_date == current_date and 
                    existing_time == current_time
                ):
                    print(
                        "Doctor already has another "
                        "appointment at this date and time."
                    )
                    conflict_found = True
                    break

                # Same patient + same date + same time
                if (
                    existing_patient_id == current_patient_id and 
                    existing_date == current_date and 
                    existing_time == current_time
                ):
                    print(
                        "Patient already has another "
                        "appointment at this date and time."
                    )
                    conflict_found = True
                    break

                # Same patient + same doctor + same day
                if (
                    existing_patient_id == current_patient_id and 
                    existing_doctor_id == current_doctor_id and 
                    existing_date == current_date
                ):
                    print(
                        "Patient already has another "
                        "appointment with this doctor "
                        "on this date."
                    )
                    conflict_found = True
                    break

            if conflict_found:
                print("Appointment was not updated.")

                appointment_data = load_data(
                    constant.TABLE_APPOINTMENT
                )
            else:
                current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                appointment[COLUMN_UPDATED_AT] = current_date_time

                save_appointment_record(
                    constant.ACTION_UPDATE,
                    appointment_data,
                    appointment
                )

                print(
                    "Appointment updated successfully."
                )

        search_again = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want update anything else?"
            )
        )

        if search_again == constant.CONFIRM_NO:
            return

APPOINTMENT_LIST_DATE = 1
APPOINTMENT_LIST_CREATED_AT = 2
APPOINTMENT_LIST_DOCTOR = 3
APPOINTMENT_LIST_STATUS = 4
APPOINTMENT_LIST_BACK = 5


APPOINTMENT_LIST_OPTIONS = {
    APPOINTMENT_LIST_DATE: "Appointment Date",
    APPOINTMENT_LIST_CREATED_AT: "Created At",
    APPOINTMENT_LIST_DOCTOR: "Doctor",
    APPOINTMENT_LIST_STATUS: "Status",
    APPOINTMENT_LIST_BACK: "Back",
}

def appointment_list() -> None:
    data = load_data(constant.TABLE_APPOINTMENT)

    if not helper.ensure_records_exist(data, 'appointment'):
        return

    patient_data = load_data(constant.TABLE_PATIENT)
    doctor_data = load_data(constant.TABLE_DOCTOR)

    while True:
        print("\nAppointment List Filter:")
        helper.display_menu(APPOINTMENT_LIST_OPTIONS)

        choice = helper.valid_option_input(
            "Choose Filter: ",
            "Filter",
            len(APPOINTMENT_LIST_OPTIONS)
        )

        if choice == APPOINTMENT_LIST_BACK:
            return

        filtered_appointments = []

        if choice == APPOINTMENT_LIST_DATE:
            appointment_date = helper.valid_date_input(
                placeholder="Enter Appointment Date (YYYY-MM-DD): ",
                name="Appointment Date"
            )

            filtered_appointments = [
                appointment
                for appointment in data
                if appointment[COLUMN_APPOINTMENT_DATE]
                == appointment_date
            ]

        elif choice == APPOINTMENT_LIST_CREATED_AT:
            created_date = helper.valid_date_input(
                placeholder="Enter Created Date (YYYY-MM-DD): ",
                name="Created Date"
            )

            filtered_appointments = [
                appointment
                for appointment in data
                if appointment[COLUMN_CREATED_AT].startswith(
                    created_date
                )
            ]

        elif choice == APPOINTMENT_LIST_DOCTOR:
            doctor_id = helper.valid_input(
                placeholder="Enter Doctor Id: ",
                name="Doctor",
                type="int"
            )

            doctor = helper.find_by_id(
                doctor_data,
                doctor_id
            )

            if doctor is None:
                display_doctor_if_found(
                    doctor,
                    doctor_id
                )
                continue

            filtered_appointments = [
                appointment
                for appointment in data
                if appointment[COLUMN_DOCTOR_ID]
                == doctor_id
            ]

        elif choice == APPOINTMENT_LIST_STATUS:
            print("\nChoose Status:")
            helper.display_menu(APPOINTMENT_STATUSES)

            status = helper.valid_option_input(
                "Enter Status: ",
                "Status",
                len(APPOINTMENT_STATUSES)
            )

            selected_status = APPOINTMENT_STATUSES[status]

            filtered_appointments = [
                appointment
                for appointment in data
                if appointment[COLUMN_STATUS]
                == selected_status
            ]

        if not filtered_appointments:
            print("No appointments found.")
            continue

        print()

        appointment_id_width = 5
        patient_width = 20
        doctor_width = 20
        date_width = 12
        time_width = 8
        status_width = 12
        created_at_width = 19

        print(
            f"{'ID':<{appointment_id_width}}"
            f"{'Patient Name':<{patient_width}}"
            f"{'Doctor Name':<{doctor_width}}"
            f"{'Date':<{date_width}}"
            f"{'Time':<{time_width}}"
            f"{'Status':<{status_width}}"
            f"{'Created At':<{created_at_width}}"
        )

        helper.print_divider(
            color=constant.COLOR_GREEN
        )

        for appointment in filtered_appointments:
            patient = helper.find_by_id(
                patient_data,
                appointment[COLUMN_PATIENT_ID]
            )

            doctor = helper.find_by_id(
                doctor_data,
                appointment[COLUMN_DOCTOR_ID]
            )

            patient_name = (
                patient[COLUMN_PATIENT_NAME][:19]
                if patient
                else "-"
            )

            doctor_name = (
                doctor[COLUMN_DOCTOR_NAME][:19]
                if doctor
                else "-"
            )

            print(
                f"{appointment[COLUMN_ID]:<{appointment_id_width}}"
                f"{patient_name:<{patient_width}}"
                f"{doctor_name:<{doctor_width}}"
                f"{appointment[COLUMN_APPOINTMENT_DATE]:<{date_width}}"
                f"{appointment[COLUMN_APPOINTMENT_TIME]:<{time_width}}"
                f"{appointment[COLUMN_STATUS]:<{status_width}}"
                f"{appointment[COLUMN_CREATED_AT]:<{created_at_width}}"
            )

        helper.print_divider(
            color=constant.COLOR_GREEN
        )

        search_again = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to filter again?"
            )
        )

        if search_again == constant.CONFIRM_NO:
            return

def view_appointment() -> None:
    data = load_data(constant.TABLE_APPOINTMENT)

    if not helper.ensure_records_exist(data, 'appointment'):
        return

    while True:
        appointment_id = helper.valid_input(
            placeholder="Enter Appointment Id:",
            name="Appointment",
            type="int"
        )

        appointment = helper.find_by_id(
            data,
            appointment_id
        )

        display_appointment_if_found(
            appointment,
            appointment_id
        )

        search_again = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want search again?"
            )
        )

        if search_again == constant.CONFIRM_NO:
            return

def appointment_status() -> None:
    data = load_data(constant.TABLE_APPOINTMENT)

    if not helper.ensure_records_exist(data, 'appointment'):
        return

    while True:
        appointment_id = helper.valid_input(
            placeholder="Enter Appointment Id:",
            name="Appointment",
            type="int"
        )

        appointment = helper.find_by_id(
            data,
            appointment_id
        )

        display_appointment_if_found(
            appointment,
            appointment_id
        )

        if appointment is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message(
                    "Do you want to search again?"
                )
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        should_update_status = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to update status?"
            )
        )

        if should_update_status == constant.CONFIRM_YES:
            print("Choose an option:")
            helper.display_menu(APPOINTMENT_STATUSES)

            status = helper.valid_option_input(
                "Enter Status:",
                "Status",
                len(APPOINTMENT_STATUSES)
            )

            appointment[COLUMN_STATUS] = APPOINTMENT_STATUSES[status]

            current_date_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            appointment[COLUMN_UPDATED_AT] = current_date_time

            save_appointment_record(
                constant.ACTION_UPDATE,
                data,
                appointment
            )

            print("Appointment status updated successfully.")

        return

def cancel_appointment():
    pass

def cancel_appointment() -> None:
    data = load_data(constant.TABLE_APPOINTMENT)

    if not helper.ensure_records_exist(data, 'appointment'):
        return

    while True:
        appointment_id = helper.valid_input(
            placeholder="Enter Appointment Id:",
            name="Appointment",
            type="int"
        )

        appointment = helper.find_by_id(
            data,
            appointment_id
        )

        display_appointment_if_found(
            appointment,
            appointment_id
        )

        if appointment is None:
            search_again = helper.confirm_input(
                helper.confirm_input_message(
                    "Do you want to search again?"
                )
            )

            if search_again == constant.CONFIRM_YES:
                continue

            return

        # Already cancelled
        if appointment[COLUMN_STATUS] == APPOINTMENT_STATUSES[STATUS_CANCELLED]:
            print("This appointment is already cancelled.")
            return

        # Cannot cancel completed appointment
        if appointment[COLUMN_STATUS] == APPOINTMENT_STATUSES[STATUS_COMPLETED]:
            print("Completed appointment cannot be cancelled.")
            return

        should_cancel = helper.confirm_input(
            helper.confirm_input_message(
                "Are you sure you want to cancel this appointment?"
            )
        )

        if should_cancel == constant.CONFIRM_NO:
            print("Appointment cancellation cancelled.")
            return

        appointment[COLUMN_STATUS] = APPOINTMENT_STATUSES[
            STATUS_CANCELLED
        ]

        current_date_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        appointment[COLUMN_UPDATED_AT] = current_date_time

        save_appointment_record(
            constant.ACTION_UPDATE,
            data,
            appointment
        )

        print("Appointment cancelled successfully.")

        cancel_another = helper.confirm_input(
            helper.confirm_input_message(
                "Do you want to cancel another appointment?"
            )
        )

        if cancel_another == constant.CONFIRM_NO:
            return
