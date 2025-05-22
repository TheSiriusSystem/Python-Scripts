if __name__ == "__main__":
    print("Welcome to the Odd or Even Checker!")
    while True:
        try:
            command: str = input("> ").strip().lower()
            if command.isdigit():
                number: int = int(command)
                print(f"{number} is {"odd" if number % 2 != 0 else "even"}.")
            else:
                print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("") # Creates a newline.
            print("Goodbye, User!")
            break