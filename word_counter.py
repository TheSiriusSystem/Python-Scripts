import re

if __name__ == "__main__":
    print("Welcome to the Word Counter!")
    while True:
        try:
            # https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/#using-regular-expressions
            command: str = input("> ").strip()
            print(f"Words: {len(re.findall(r'\b\w+\b', command))}")
        except KeyboardInterrupt:
            print("") # Creates a newline.
            print("Goodbye, User!")
            break