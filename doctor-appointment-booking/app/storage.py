from . import constant 
import json
from app.logger import logger

def load_data(table: str) -> constant.TYPE_LIST:
    table_file_path = constant.BASE_DIR_DATABASE / table

    try: 
        with open (table_file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"{table_file_path} contains invalid JSON. Starting with empty list.")
        return []

def save_data(table: str,data: constant.TYPE_LIST) -> None:
    table_file_path = constant.BASE_DIR_DATABASE / table
    with open(table_file_path, "w") as file:
        json.dump(data, file, indent=4)
