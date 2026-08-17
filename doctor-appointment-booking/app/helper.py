import app.constant as constant
import re
from typing import Literal

def is_valid_name(name: str) -> bool:
    allowed_extra = {".", " ", "-", ","}

    for char in name:
        if not (char.isalpha() or char in allowed_extra):
            return False
        
    return True


def is_valid_phone(value: str) -> bool:
    return bool(re.fullmatch(r"01[3-9]\d{8}", value))

def valid_input(
    placeholder: str = "",
    name: str = "",
    limit: int = constant.DEFAULT_LIMIT,
    required: bool = True,
    type: Literal["text", "phone", "int"] = "text",
) -> str | int:
    while True:
        value = input(placeholder).strip()

        if required and not value:
            print(f"{name} can't be empty. Please try again.")
            continue

        if type == "int":
            if re.fullmatch(r"-?\d+", value):
                return int(value)

            print(f"{name} must be a valid number.")
            continue

        if len(value) > limit:
            print(f"{name} can't be more than {limit} characters.")
            continue

        if required and type == "phone":
            if not is_valid_phone(value):
                print(f"{name} must be a valid phone number.")
                continue

        elif type == "text":
            if not is_valid_name(value):
                print(
                    f"{name} can only contain letters, spaces, periods, "
                    "comma, and hyphens."
                )
                continue

        return value

def valid_option_input(
    placeholder: str = "",
    name: str = "Option",
    max_value: int = 1,
) -> int:
    while True:
        value = input(placeholder).strip()

        if not value:
            print(f"{name} can't be empty. Please try again.")
            continue

        try:
            value = int(value)
        except ValueError:
            print(f"{name} must be a valid number.")
            continue

        if value < 1 or value > max_value:
            print(f"{name} must be between 1 and {max_value}.")
            continue

        return value

def print_divider(
    divided_by: int = constant.DEFAULT_DIVIDER,
    divider: str = "-",
    color: str = constant.COLOR_BLUE,
) -> None:
    print(f"{color}{divider * divided_by}{constant.COLOR_RESET}")

# def print_title(title: str) -> None:
#     print_divider(divider="=")
#     print(f"{constant.CYAN}  {title}{constant.RESET}")
#     print_divider(divider="=")
#     print()
def print_title(title: str) -> None:
    width = constant.DEFAULT_DIVIDER

    print_divider(divider="=")
    print(f"{constant.COLOR_CYAN}{title.center(width)}{constant.COLOR_RESET}")
    print_divider(divider="=")
    print()


def confirm_input(placeholder: str = "", name: str = "Confirmation") -> str:
    while True:
        value = input(placeholder).strip().lower()

        if value in (constant.CONFIRM_YES, constant.CONFIRM_NO):
            return value
        elif not value:
            print(f"{name} can't be empty. Please try again.")
        else:
            print("Wrong Input, please try again.")

def confirm_input_message(message: str) -> str:
    return f"{message} [{constant.CONFIRM_YES}/{constant.CONFIRM_NO}]: " 

def get_next_id(data: constant.TYPE_LIST) -> int:
    if data:
        return max(item["id"] for item in data) + 1

    return 1