from pathlib import Path
MENU_OPTIONS = """
1. Doctor Management
2. Patient Management
3. Manage Doctor Schedule
4. Manage Appointment
5. Exit
"""

MENU_MANAGE_DOCTOR = 1
MENU_MANAGE_PATIENT = 2
MENU_MANAGE_DOCTOR_SCHEDULE = 3
MENU_MANAGE_APPOINTMENT = 4
MENU_EXIT = 5


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


