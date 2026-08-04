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
MENU_ADD, MENU_VIEW, MENU_LIST, MENU_EXIT = 1, 2, 3, 9

def print_divider(divided_by:int = 30)->None:
    print("-" * divided_by)

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

def display_task(task)->None:
    print(f"ID          : {task['id']}")
    print(f"Title       : {task['title']}")
    print(f"Description : {task['description']}")
    print(f"priority    : {PRIORITIES[task['priority']]}")
    print(f"Status      : {STATUSES[task['status']]}")
    print(f"Due Date    : {task['due_date']}")
    print(f"Created At  : {task['created_at']}")

def find_task_by_id(tasks:list[dict])->int|None:
    if not tasks:
        print("No Tasks available yet.")
        return
    try:
        task_id = int(input("Enter the task id: "))
        index = next((i for i, item in enumerate(tasks) if item.get("id") == task_id), None)
    except ValueError:
        print("Wrong input, please try again.")
        return None

    return index

def view_task(tasks:list[dict])->None:
    task_index = find_task_by_id(tasks)

    if task_index is None:
        print('Task Not found.')

        return
    print_divider()
    display_task(tasks[task_index])

def task_list(tasks:list[dict])->None:
    if not tasks:
        print("No Tasks available yet.")
        return
    print("To-do task list:")
    while True:
        try:
            print("1. All list.")
            print("2. search by title.")
            print("3. Filter by priority.")
            print("4. Filter by status.")
            print("5. End list action.")
            filter_by = int(input("Please choose from (1-5): "))
            filtered_tasks = []

            if filter_by == 1:
                filtered_tasks = tasks
            elif filter_by == 2:
                search_title = input("Search Title: ").strip()
                filtered_tasks = [
                    task for task in tasks
                    if search_title.lower() in task['title'].lower()
                ]
            elif filter_by == 3:
                search_priority = choose_option(PRIORITIES, 'Priority')
                filtered_tasks = [
                    task for task in tasks
                    if search_priority == task['priority']
                ]
            elif filter_by == 4:
                search_status = choose_option(STATUSES, 'Status')
                filtered_tasks = [
                    task for task in tasks
                    if search_status == task['status']
                ]
            elif filter_by == 5:
                break
            else:
                print("Input invalided option, please try again.")

            display_tasks_table(filtered_tasks)
        except ValueError:
            print("Wrong Input, Please try again.")

def display_tasks_table(tasks: list[dict]) -> None:
    if not tasks:
        print("No records found.")
        return
    print('\n')
    # Header
    header = f"{'ID':<4} {'Title':<20} {'Priority':<10} {'Status':<12} {'Due Date':<12}"
    print_divider(len(header))
    print(header)
    print_divider(len(header))

    # Rows
    for task in tasks:
        title = task['title'][:18] + '..' if len(task['title']) > 18 else task['title']
        row = (
            f"{task['id']:<4} "
            f"{title:<20} "
            f"{PRIORITIES[task['priority']]:<10} "
            f"{STATUSES[task['status']]:<12} "
            f"{task['due_date']:<12}"
        )
        print(row)

    print_divider(len(header))
    print('\n')

def main()->None:
    tasks = []
    task_next_id = 1
    print('Hi, Welcome to To-do list')
    print_divider()
    while True:
        try:
            print('\n')
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
            elif choice == MENU_VIEW:
                view_task(tasks)
            elif choice == MENU_LIST:
                task_list(tasks)
            elif choice == MENU_EXIT:
                print("Good Bye, Hope to see you soon!")
                break
            else:
                print("Input invalided option, please try again.")
        except ValueError:
            print("Invalid input, Please enter a number.")

if __name__ == "__main__":
    main()
