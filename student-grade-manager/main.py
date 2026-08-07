import constants
import controller
from utils import valid_int_input

def main() -> None:
    print('Hi, Welcome to Student Grade Manager')

    while True:
        print(constants.MENU_OPTIONS)
        choice = valid_int_input('Choose an option: ')

        if choice == constants.MENU_ADD:
            controller.add_student()
        elif choice == constants.MENU_VIEW_ALL:
            controller.view_all_students()
        elif choice == constants.MENU_SEARCH:
            controller.view_student_details()
        elif choice == constants.MENU_UPDATE:
            controller.update_student_record()
        elif choice == constants.MENU_DELETE:
            controller.delete_student_record()
        elif choice == constants.MENU_REPORT:
            controller.view_report()
        elif choice == constants.MENU_ALL_REPORTS:
            controller.view_all_reports()
        elif choice == constants.MENU_RANKING:
            controller.view_ranking()
        elif choice == constants.MENU_STATISTICS:
            pass
        elif choice == constants.MENU_EXIT:
            print("Good bye, Hope to see you soon!")
            return
        else:
            print("Invalid option, please try again.")
            # match choice:
            #     case c if c == const.MENU_OPTIONS:
            #         add_student()
            #     case c if c == MENU_VIEW_ALL:
            #         view_all_students()
            #     case c if c == MENU_SEARCH:
            #         print("Search - not build yet.")
            #     case c if c == MENU_UPDATE:
            #         print("Search - not build yet.")
            #     case c if c == MENU_DELETE:
            #         print("Search - not build yet.")
            #     case c if c == MENU_REPORT:
            #         print("Search - not build yet.")
            #     case c if c == MENU_ALL_REPORTS:
            #         print("Search - not build yet.")
            #     case c if c == MENU_RANKING:
            #         print("Search - not build yet.")
            #     case c if c == MENU_STATISTICS:
            #         print("Search - not build yet.")
            #     case c if c == MENU_EXIT:
            #         print("Good bye, Hope to see you soon!")
            #         return
            #     case _:
            #         print("Invalid option, please try again.")    

if __name__ == "__main__":
    main()
