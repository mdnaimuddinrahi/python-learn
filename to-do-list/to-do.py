from datetime import date, datetime

PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW = 1, 2, 3  
PRIORITIES = {
    PRIORITY_HIGH: "High",
    PRIORITY_MEDIUM: "Medium",
    PRIORITY_LOW: "Low",
}
STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETE, STATUS_CANCEL = 1, 2, 3, 4
STATUSES = {
    STATUS_PENDING: "Pending",
    STATUS_IN_PROGRESS: "In Progress",
    STATUS_COMPLETE: "Completed",
    STATUS_CANCEL: "Cancelled",
}
MENU_ADD, MENU_EXIT = 1, 9

def print_divider()-> None:
    print("-" * 30)

def choose_option(options: dict, label: str)->int:
    print(f"Choose {label}")
    print_divider()
    for key, value in options.items():
        print(f"{key}. {value}")
    while True:
        try:
            choice = int(input(f"Enter number (1-{len(options)}): "))
            if choice in options:
                return choice
            print("Invalid choice, try again.")
        except ValueError:
            print("Please enter a number.")

def valid_input(placeholder: str = '', name: str = '')->str:
    while True:
        value = input(placeholder).strip()
        if value:
            return value
        print(f"{name} can't be empty. Please try again.")

def valid_date(placeholder: str = '', name: str = '')->str:
    while True:
        value = input(placeholder).strip()
        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
            if parsed_date<date.today():
                print(f"{name} can't be in the past, Please try again")
                continue
            return value
        except ValueError:
            print(f"Invalid date format. Please use YYYY-MM-DD (e.g. {date.today().isoformat()}).")

def add_task(tasks: list, next_task_id: int)->int: 
    print('Please enter task details.')
    title = valid_input('Input title: ', "Title")
    description = valid_input('Input description: ', "Description")
    due_date = valid_date('Enter Due Date(YYYY-MM-DD): ', 'Due Date')
    priority = choose_option(PRIORITIES, "Priority")
    task = {
        "id": next_task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "status": STATUS_PENDING,
        "created_at": date.today().isoformat()
    }
    tasks.append(task)
    print("New Task is created.")
    print_divider()
    display_task(task)

    return next_task_id + 1

def display_task(task):
    print(f"ID          : {task['id']}")
    print(f"Title       : {task['title']}")
    print(f"Description : {task['description']}")
    print(f"priority    : {PRIORITIES[task['priority']]}")
    print(f"Status      : {STATUSES[task['status']]}")
    print(f"Due Date    : {task['due_date']}")
    print(f"Created At  : {task['created_at']}")

def main()->None:
    tasks = []
    task_next_id = 1
    print('Hi, Welcome to To-do list')
    print_divider()
    while True:
        try:
            print('''============ To do list ============
1. Add task.
2. View task.
3. Task List.
4. Update task.
5. Delete task.
6. Complete task.
9. Exit.
            ''')
            choice = int(input('Choose an option: '))

            if choice == MENU_ADD:
                task_next_id = add_task(tasks, task_next_id)
            elif choice == MENU_EXIT:
                print("Good Bye, Hope to see you soon!")
                break
        except ValueError:
            print("Invalid input, Please enter a number.")

if __name__ == "__main__":
    main()
