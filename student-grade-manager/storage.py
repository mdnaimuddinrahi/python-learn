import json
from constants import DATA_FILE, StudentList
from logger import logger

def load_data() -> StudentList:
    try:
        with open (DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"{DATA_FILE} not found. Starting with empty student list.")
        save_data([])
        return []
    except json.JSONDecodeError:
        logger.error(f"{DATA_FILE} contains invalid JSON. Starting with empty student list.")
        return []
    
def save_data(data: StudentList) -> None:
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)