import os
import json

SAVE_FILE: str = "save.json"
TODO_LIST_LIMIT: int = 25

todo_list: list[str] = []

def save() -> None:
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(todo_list, f, indent=4)

def is_save_valid(data) -> bool:
    if type(data) != list:
        return False
    for element in data:
        if type(element) != str:
            return False
    return True

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
                if name not in todo_list:
                    todo_list.append(name)
                    print(f"Added item '{name}'.")
                else:
                    print(f"'{name}' is already in your to-do list.")
            else:
                print(f"You cannot add more than {TODO_LIST_LIMIT} names to the to-do list!")
        elif command_lowercase.startswith("remove "):
            name: str = command[7:]
            if name == "all":
                count: int = len(todo_list)
                todo_list.clear()
                print(f"Removed {count} item(s).")
            elif name in todo_list:
                todo_list.pop(todo_list.index(name))
                print(f"Removed item '{name}'.")
            elif name.isdigit():
                index: int = int(name)
                try:
                    name = todo_list[index]
                    todo_list.pop(index)
                    print(f"Removed item '{name}'.")
                except (IndexError, ValueError):
                    print(f"Index {index} is not in your to-do list.")
            else:
                print(f"'{name}' is not in your to-do list.")
        elif command_lowercase == "list":
            if len(todo_list) > 0:
                for index, name in enumerate(todo_list):
                    print(f"Item: (index: {index}, name: {name})")
            else:
                print("Your to-do list is empty.")
        elif command_lowercase == "help":
            print("add <name> - Add a new task.")
            print("remove <name> | <index> | all - Remove a task..")
            print("list - Show all tasks.")
            print("help - Show all commands.")
            print("exit - Exit the application.")
        elif command_lowercase == "exit":
            print("Goodbye, User!")
            break
        else:
            print("Invalid command.")
    save()