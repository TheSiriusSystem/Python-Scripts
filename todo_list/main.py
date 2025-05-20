import os
import json

type ToDoListItem = dict[str, str]

SAVE_FILE: str = "save.json"
TODO_LIST_LIMIT: int = 25
VALID_TODO_LIST_ITEM_STATUSES: list[str] = [
    "pending",
    "in progress",
    "done",
]

def save() -> None:
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(todo_list, f, indent=4)

def is_save_valid(data) -> bool:
    if type(data) != list:
        return False
    for item in data:
        if type(item) != dict:
            return False
        if "name" not in item or "status" not in item:
            return False
        if not isinstance(item["name"], str) or not isinstance(item["status"], str):
            return False
        if item["name"] == "all":
            return False
    return True

def get_todo_list_item(name: str) -> ToDoListItem | None:
    for item in todo_list:
        if item["name"] == name:
            return item
    return None

def is_argument_not_specified(argument) -> bool:
    return not isinstance(argument, str) or argument == ""

def is_argument_specified(argument) -> bool:
    return isinstance(argument, str) and argument != ""

def print_no_command_arg_warning(command: str) -> None:
    print(f"Command '{command}' does not take a parameter.")

def command_add(argument) -> None:
    if is_argument_not_specified(argument):
        print("Usage: <name>")
        return

    if len(todo_list) < TODO_LIST_LIMIT:
        if argument != "all" and not get_todo_list_item(argument):
            todo_list.append({
                "name": argument,
                "status": VALID_TODO_LIST_ITEM_STATUSES[0],
            })
            print(f"Added item '{argument}'.")
        else:
            if argument == "all":
                print(f"Cannot add an item with the name '{argument}'.")
            else:
                print(f"'{argument}' is already in your to-do list.")
    else:
        print(f"You cannot add more than {TODO_LIST_LIMIT} names to the to-do list!")

def command_remove(argument) -> None:
    if is_argument_not_specified(argument):
        print("Usage: <name>")
        return

    item = get_todo_list_item(argument) if argument != "all" else None # type: ignore
    if argument == "all":
        count: int = len(todo_list)
        if count > 0:
            todo_list.clear()
            print(f"Removed {count} item{"s" if count > 1 else ""}.")
        else:
            print("Your to-do list is already empty.")
    elif item:
        todo_list.pop(todo_list.index(item))
        print(f"Removed item '{argument}'.")
    else:
        print(f"'{argument}' is not in your to-do list.")

def command_mark(argument) -> None:
    if is_argument_not_specified(argument):
        print("Usage: <name>")
        return

    item: ToDoListItem = get_todo_list_item(argument) # type: ignore
    if item:
        new_item_status: str = input(f"Enter a status... ").strip().lower()
        if new_item_status not in VALID_TODO_LIST_ITEM_STATUSES:
            print("Invalid option.")
        else:
            if item["status"] != new_item_status:
                item["status"] = new_item_status
                print(f"Marked task '{item["name"]}' as '{new_item_status}'.")
            else:
                print(f"Task '{item["name"]}' is already marked as '{new_item_status}'.")
    else:
        print(f"'{argument}' is not in your to-do list.")

def command_list(argument) -> None:
    if is_argument_specified(argument):
        print_no_command_arg_warning("list")
        return

    if len(todo_list) > 0:
        for index, item in enumerate(todo_list):
            print(f"[{index + 1}]: {item["name"]} - {item["status"].capitalize()}")
    else:
        print("Your to-do list is empty.")

def command_help(argument) -> None:
    if is_argument_specified(argument):
        print_no_command_arg_warning("help")
        return

    print("add <name> - Add a new task.")
    print("remove <name> | all - Remove a task.")
    print(f"mark <name> - Mark a task as ({", ".join(VALID_TODO_LIST_ITEM_STATUSES)}). When a task is provided, it will prompt you to set a new status.")
    print("list - Show all tasks.")
    print("help - Show all commands.")
    print("exit - Exit the application.")

if __name__ == "__main__":
    commands: dict = {
        "add": command_add,
        "remove": command_remove,
        "mark": command_mark,
        "list": command_list,
        "help": command_help,
    }
    todo_list: list[ToDoListItem] = []

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if is_save_valid(data):
                todo_list = data
    print("Welcome to the To-Do List Manager!")
    print("Type 'help' to see available commands.")
    while True:
        save()
        command_parts: list[str] = input("> ").strip().split(maxsplit=1)
        command: str = command_parts[0].lower()
        if command == "exit":
            print("Goodbye, User!")
            break
        elif command in commands:
            commands[command](command_parts[1] if len(command_parts) == 2 else None)
        else:
            print("Invalid command.")
    save()