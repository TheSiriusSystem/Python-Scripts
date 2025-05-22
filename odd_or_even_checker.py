if __name__ == "__main__":
    print("Welcome to the Odd or Even Checker!")
    print("Type 'exit' to exit the application.")
    while True:
        command: str = input("> ").strip().lower()
        if command.isdigit():
            number: int = int(command)
            if number % 2 != 0:
                print(f"{number} is odd.")
            else:
                print(f"{number} is even.")
        else:
            if command == "exit":
                print("Goodbye, User!")
                break
            else:
                print("Invalid input. Please enter a number.")