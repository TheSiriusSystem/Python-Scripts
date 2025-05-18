import random

RANGE_MIN: int = 0
RANGE_MAX: int = 10

lives: int = 5
secret_number: str = str(random.randint(RANGE_MIN, RANGE_MAX))

def print_lives() -> None:
    print(f"Lives: {lives}")

if __name__ == "__main__":
    print(f"Guess the secret number! ({RANGE_MIN}–{RANGE_MAX})")
    print("Type 'exit' to exit the application.")
    print("")
    print_lives()
    while True:
        command: str = input("> ").strip().lower()
        if command == secret_number:
            print("CONGRATULATIONS!")
            break
        elif not command.isdigit():
            if command != "exit":
                print("Invalid guess.")
            else:
                print("Goodbye, User!")
                break
        else:
            lives -= 1
            print_lives()
            if lives <= 0:
                print("You lost the game!")
                break