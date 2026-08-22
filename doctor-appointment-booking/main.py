import app.constant as constant
from app.helper import valid_option_input, print_title
from app.doctor import manage_doctor
from app.patient import manage_patient

def main() -> None:
    print_title("DOCTOR APPOINTMENT MANAGEMENT")   
    while True:
        print(constant.MENU_OPTIONS)
        choice = valid_option_input("Choose an option: ", name="Option", max_value=13)

        if choice == constant.MENU_MANAGE_DOCTOR:
            manage_doctor()
        elif choice == constant.MENU_MANAGE_PATIENT:
            # patient.add_patient()
            manage_patient()
            pass
        elif choice == constant.MENU_MANAGE_DOCTOR_SCHEDULE:
            # schedule.generate_slots()
            pass
        elif choice == constant.MENU_CHECK_AVAILABILITY:
            # schedule.check_availability()
            pass
        elif choice == constant.MENU_CREATE_APPOINTMENT:
            # appointment.create_appointment()
            pass
        elif choice == constant.MENU_VIEW_APPOINTMENT:
            # appointment.view_appointment()
            pass
        elif choice == constant.MENU_LIST_APPOINTMENTS:
            # appointment.appointment_list()
            pass
        elif choice == constant.MENU_SEARCH_APPOINTMENTS:
            # appointment.search_appointments()
            pass
        elif choice == constant.MENU_CANCEL_APPOINTMENT:
            # appointment.cancel_appointment()
            pass
        elif choice == constant.MENU_BLOCK_TIME_SLOT:
            # schedule.block_slot()
            pass
        elif choice == constant.MENU_UNBLOCK_TIME_SLOT:
            # schedule.unblock_slot()
            pass
        elif choice == constant.MENU_DAILY_SCHEDULE:
            # schedule.daily_schedule()
            pass
        elif choice == constant.MENU_EXIT:
            print("Good bye, Hope to see you soon!")
            return
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
