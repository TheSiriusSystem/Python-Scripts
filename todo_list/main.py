import os
import json

SAVE_FILE: str = "save.json"

todo_list: list[str] = []

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
                for element in data:
                    element = element.lower()
                todo_list = data
    print("Welcome to the To-Do List Manager! Type 'help' to see available commands.")
    while True:
        command: str = input("> ").strip().lower()
        if command.startswith("add "):
            item: str = command[4:]
            todo_list.append(item)
            print(f"Added item '{item}'.")
        elif command.startswith("remove "):
            item: str = command[7:]
            if item == "all":
                todo_list.clear()
            elif item in todo_list:
                todo_list.pop(todo_list.index(item))
                print(f"Removed item '{item}'.")
        elif command == "list":
            print(todo_list)
        elif command == "help":
            print("add <item> - Add a new task.")
            print("remove <item> | all - Remove a task..")
            print("list - Show all tasks.")
            print("help - Show all commands.")
            print("exit - Exit the application.")
        elif command == "exit":
            print("Goodbye, User!")
            break
        else:
            print("Invalid command.")
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(todo_list, f, indent=4)