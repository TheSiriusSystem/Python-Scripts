if __name__ == "__main__":
    print("Welcome to the Palindrome Checker!")
    print("Type 'exit' to exit the application.")
    while True:
        command: str = input("> ").strip().lower()
        if command == "exit":
            print("Goodbye, User!")
            break
        else:
            text: str = "".join(character for character in command if character.isalnum())

            if len(text) <= 1:
                print("Invalid input. Please enter a text with more than 1 character.")
                continue

            reversed_text: str = text[::-1]
            print(f"{reversed_text} - {"MATCH!" if text == reversed_text else "NO MATCH!"}")