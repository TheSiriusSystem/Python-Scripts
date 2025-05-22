if __name__ == "__main__":
    print("Welcome to the Word Counter!")
    print("Type 'exit' to exit the application.")
    while True:
        command: str = input("> ").strip()
        if command.lower() == "exit":
            print("Goodbye, User!")
            break
        else:
            print(f"Words: {len(command.split())}")