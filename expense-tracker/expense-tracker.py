"""
Expense Tracker

Author: MD. Naim Uddin Rahi
Description:
A simple command-line CRUD application built with Python to practice
functions, lists, dictionaries, loops, exception handling, and
basic software design.
"""
def add_expense(expenses, next_id):
    new_category = input("Enter new category: ")
    new_amount = input("Enter new amount: ")

    expenses.append({
        'id': next_id,
        'amount': int(new_amount),
        'category': new_category
    })
    return next_id + 1

def expense_list(expenses):
    if not expenses:
        print("Expense Not found.")
        return
    print("Expense List:")
    print("-" * 30)
    for expense in expenses:
        print(f"ID: {expense['id']}")
        print(f"Category: {expense['category']}")
        print(f"Amount: {expense['amount']}")
        print("-" * 30)

def show_total_expense(expenses):
    total = sum(expense['amount'] for expense in expenses)
    print(f"total amount is: {total}")

def find_expense_by_id(expenses, expense_id):
    index = next((i for i, item in enumerate(expenses) if item.get("id") == expense_id), None)
    return index

def delete_expense(expenses, expense_id):
    expense_index = find_expense_by_id(expenses, expense_id)

    if expense_index is None:
        print('Expense Not found.')
        return

    removed = expenses.pop(expense_index)
    print('Expense deleted successfully.')
    print(f'Deleted: {removed}')

def update_expense(expenses, expense_id):
    expense_index = find_expense_by_id(expenses, expense_id)
    
    if expense_index is None:
        print('Expense Not found.')
        return
    expense = expenses[expense_index]
    is_name = input('Do you want to update name?[y/n]:')

    if is_name == 'y':
        name = input('Upate category name: ')
        expense['category'] = name
    is_amount = input('Do you want to update amount?[y/n]:')

    if is_amount == 'y':
        amount = int(input('Update amount: '))
        expense['amount'] = amount
    print('Expense Updated Successfully.')

def show_expense(expenses, expense_id): 
    expense_index = find_expense_by_id(expenses, expense_id)

    if expense_index is None:
        print('Expense Not found.')
        return

    expense = expenses[expense_index]
    print("-" * 30)
    print(f"ID: {expense['id']}")
    print(f"Category: {expense['category']}")
    print(f"Amount: {expense['amount']}")
    print("-" * 30)
    return expense

def main():
    expenses = [] 
    next_id = 1  
    while True:
        try:
            print('''============ Expense Tracker ============
1. Add Expense
2. Expense List
3. Show Total Expenses
4. Update Expense
5. Delete Expense
6. Show Expense Details
9. Exit''')
            question = int(input('Choose an option: '))
            if question == 1:
                next_id = add_expense(expenses, next_id)
            elif question == 2:
                expense_list(expenses)            
            elif question == 3:
                show_total_expense(expenses)
            elif question == 4:
                expense_id = int(input('Enter the Expense Id: '))
                update_expense(expenses, expense_id)
            elif question == 5:
                expense_id = int(input("Enter the Expense Id: "))
                delete_expense(expenses, expense_id)
            elif question == 6:
                expense_id = int(input("Enter the Expense Id: "))
                show_expense(expenses, expense_id)
            elif question == 9:
                break
            else:
                print("Invalid Option")
        except ValueError:
            print('Invalid input. Please enter a number.')

main()
