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

todo_list: list[ToDoListItem] = []

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

def mark_todo_list_item(item: ToDoListItem, new_status: str) -> None:
    item["status"] = new_status
    print(f"Marked task '{item["name"]}' as '{new_status}'.")

if __name__ == "__main__":
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if is_save_valid(data):
                todo_list = data
    print("Welcome to the To-Do List Manager! Type 'help' to see available commands.")
    while True:
        save()
        command: str = input("> ").strip()
        command_lowercase: str = command.lower()
        if command_lowercase.startswith("add "):
            if len(todo_list) < TODO_LIST_LIMIT:
                name: str = command[4:]
                if name != "all" and not get_todo_list_item(name):
                    todo_list.append({
                        "name": name,
                        "status": VALID_TODO_LIST_ITEM_STATUSES[0],
                    })
                    print(f"Added item '{name}'.")
                else:
                    if name == "all":
                        print(f"Cannot add an item with the name '{name}'.")
                    else:
                        print(f"'{name}' is already in your to-do list.")
            else:
                print(f"You cannot add more than {TODO_LIST_LIMIT} names to the to-do list!")
        elif command_lowercase.startswith("remove "):
            name: str = command[7:]
            item = get_todo_list_item(name) if name != "all" else None # type: ignore
            if name == "all":
                count: int = len(todo_list)
                todo_list.clear()
                print(f"Removed {count} item(s).")
            elif item:
                todo_list.pop(todo_list.index(item))
                print(f"Removed item '{name}'.")
            else:
                print(f"'{name}' is not in your to-do list.")
        elif command_lowercase.startswith("mark "):
            name: str = command[5:]
            item: ToDoListItem = get_todo_list_item(name) # type: ignore
            if item:
                new_item_status: str = input(f"Enter a status... ").strip().lower()
                if new_item_status not in VALID_TODO_LIST_ITEM_STATUSES:
                    print("Invalid option.")
                else:
                    mark_todo_list_item(item, new_item_status)
            else:
                print(f"'{name}' is not in your to-do list.")
        elif command_lowercase == "list":
            if len(todo_list) > 0:
                for index, item in enumerate(todo_list):
                    print(f"[{index + 1}]: {item["name"]} - {item["status"].capitalize()}")
            else:
                print("Your to-do list is empty.")
        elif command_lowercase == "help":
            print("add <name> - Add a new task.")
            print("remove <name> | all - Remove a task.")
            print(f"mark <name> - Mark a task as ({", ".join(VALID_TODO_LIST_ITEM_STATUSES)}). When a task is provided, it will prompt you to set a new status.")
            print("list - Show all tasks.")
            print("help - Show all commands.")
            print("exit - Exit the application.")
        elif command_lowercase == "exit":
            print("Goodbye, User!")
            break
        else:
            print("Invalid command.")
    save()