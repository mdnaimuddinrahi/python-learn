import app.constant as constant
from app.helper import valid_option_input, print_title
from app.doctor import manage_doctor
from app.patient import manage_patient
from app.schedule import manage_schedule
from app.appointment import manage_appointment

def main() -> None:
    print_title("DOCTOR APPOINTMENT MANAGEMENT")   
    while True:
        print(constant.MENU_OPTIONS)
        choice = valid_option_input("Choose an option: ", name="Option", max_value=13)

        if choice == constant.MENU_MANAGE_DOCTOR:
            manage_doctor()
        elif choice == constant.MENU_MANAGE_PATIENT:
            manage_patient()
        elif choice == constant.MENU_MANAGE_DOCTOR_SCHEDULE:
            manage_schedule()
        elif choice == constant.MENU_MANAGE_APPOINTMENT:
            manage_appointment()
        elif choice == constant.MENU_EXIT:
            print("Good bye, Hope to see you soon!")
            return
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
