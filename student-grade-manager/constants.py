from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "database.json"
MIN_MARKS = 0
PASS_MARKS = 33
MAX_MARKS = 100
INPUT_LIMIT = 50
DEFAULT_DIVIDER = 30
CONFIRM_YES = 'y'
CONFIRM_NO = 'n'

SUBJECTS = (
    "Mathematics",
    "English",
    "Science",
    "Social Studies",
    "Computer Science",
)
LABEL_WIDTH = max(
    len("Student ID"),
    len("Student Name"),
    *(len(subject) for subject in SUBJECTS)
) + 2

GRADE_BOUNDARIES = [
    (80, 100, "A+", 4.00),
    (70, 79, "A", 3.75),
    (60, 69, "A-", 3.50),
    (50, 59, "B", 3.00),
    (40, 49, "C", 2.00),
    (33, 39, "D", 1.00),
    (0, 32, "F", 0.00),
]
MENU_ADD = 1
MENU_VIEW_ALL = 2
MENU_SEARCH = 3
MENU_UPDATE = 4
MENU_DELETE = 5
MENU_REPORT = 6
MENU_ALL_REPORTS = 7
MENU_RANKING = 8
MENU_STATISTICS = 9
MENU_EXIT = 0
MENU_OPTIONS = """
1. Add Student
2. View All Students
3. Search Student by ID
4. Update Student
5. Delete Student
6. View Student Report
7. View All Reports
8. Class Ranking
9. Class Statistics
0. Exit
"""