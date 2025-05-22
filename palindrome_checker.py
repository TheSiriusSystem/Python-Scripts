MINIMUM_TEXT_LENGTH: int = 1

if __name__ == "__main__":
    print("Welcome to the Palindrome Checker!")
    while True:
        try:
            command: str = input("> ").lower()
            text: str = ""
            for character in command:
                if character.isalnum():
                    text += character

            if len(text) <= MINIMUM_TEXT_LENGTH:
                print(f"Invalid input. Please enter a text with more than {MINIMUM_TEXT_LENGTH} character{"s" if MINIMUM_TEXT_LENGTH >= 2 else ""}.")
                continue

            reversed_text: str = text[::-1]
            print(f"{reversed_text} - {"Palindrome!" if text == reversed_text else "Not a palindrome!"}")
        except KeyboardInterrupt:
            print("") # Creates a newline.
            print("Goodbye, User!")
            break