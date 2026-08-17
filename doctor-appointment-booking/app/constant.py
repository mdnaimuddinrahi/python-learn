from pathlib import Path
MENU_OPTIONS = """
1. Doctor Management
2. Patient Management
3. Manage Doctor Schedule
4. Check Availability
5. Create Appointment
6. View Appointment
7. List Appointments
8. Search Appointments
9. Cancel Appointment
10. Block Time Slot
11. Unblock Time Slot
12. Daily Schedule
13. Exit
"""

MENU_MANAGE_DOCTOR = 1
MENU_MANAGE_PATIENT = 2
MENU_MANAGE_DOCTOR_SCHEDULE = 3
MENU_CHECK_AVAILABILITY = 4
MENU_CREATE_APPOINTMENT = 5
MENU_VIEW_APPOINTMENT = 6
MENU_LIST_APPOINTMENTS = 7
MENU_SEARCH_APPOINTMENTS = 8
MENU_CANCEL_APPOINTMENT = 9
MENU_BLOCK_TIME_SLOT = 10
MENU_UNBLOCK_TIME_SLOT = 11
MENU_DAILY_SCHEDULE = 12
MENU_EXIT = 13


DEFAULT_LIMIT = 50
DEFAULT_DIVIDER = 32
CONFIRM_YES = 'y'
CONFIRM_NO = 'n'
ACTION_CREATE = 'create'
ACTION_UPDATE = 'update'
ACTION_DELETE = 'delete'

COLOR_RESET = "\033[0m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_CYAN = "\033[96m"
COLOR_WHITE = "\033[97m"

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR_DATABASE = BASE_DIR / "database"

TYPE_DICT = dict[str, object]
TYPE_LIST = list[TYPE_DICT]

TABLE_DOCTOR = "doctors.json"
TABLE_PATIENT = "patients.json"
TABLE_APPOINTMENT = "appointments.json"


