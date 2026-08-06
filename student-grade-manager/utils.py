from constants import MAX_MARKS, MIN_MARKS, INPUT_LIMIT, DEFAULT_DIVIDER
import re

def is_valid_name(name: str) -> bool:
    allowed_extra = {'.', ' ', '-'}

    for char in name:
        if not (char.isalpha() or char in allowed_extra):
            return False
        
    return True

def valid_input(placeholder: str = '', name: str = '') -> str:
    while True:
        value = input(placeholder).strip()

        if not value:
            print(f"{name} can't be empty. Please try again.")
            continue

        if len(value)> INPUT_LIMIT:
            print(f"{name} can't be more than {INPUT_LIMIT} characters.")
            continue

        if not is_valid_name(value):
            print(f"{name} can only contain letters, spaces, periods, and hyphens.")
            continue

        return value

def valid_marks_input(placeholder: str = '', name: str = '') -> int:
    while True:
        value = valid_int_input(placeholder)

        if value > MAX_MARKS:
            print("Marks can't be greater than 100")
            continue
        if value < MIN_MARKS:
            print("Marks can't be less than 0")
            continue

            return value

def print_divider(divided_by:int = DEFAULT_DIVIDER) -> None:
    print("-" * divided_by)


def valid_int_input(placeholder: str) -> int:
    while True:
        value = input(placeholder)
        if re.fullmatch(r'-?\d+', value):
            return int(value)
        print("Invalid input. Please enter only number.")
