import random

VALID_DIFFICULTIES: list[str] = [
    "easy",
    "normal",
    "hard",
]

def print_lives() -> None:
    print(f"Lives: {lives}")

if __name__ == "__main__":
    guess_range_min: int = 1
    guess_range_max: int = 100
    lives: int = -1

    while True:
        difficulty: str = input(f"Choose a difficulty... ({"/".join(VALID_DIFFICULTIES)}) ").strip().lower()
        if difficulty not in VALID_DIFFICULTIES:
            print(f"Invalid option. Please choose ({"/".join(VALID_DIFFICULTIES)}).")
            continue
        if difficulty == VALID_DIFFICULTIES[0]: # Easy
            guess_range_max = 50
        elif difficulty == VALID_DIFFICULTIES[2]: # Hard
            guess_range_min = 0
            lives = 7
        break

    secret_number: str = str(random.randint(guess_range_min, guess_range_max))
    attempts: int = 0

    print(f"Guess the secret number! ({guess_range_min}-{guess_range_max})")
    print("Type 'help' to see available commands.")
    print("")
    if lives != -1:
        print_lives()
    while True:
        command: str = input("> ").strip().lower()
        if command == secret_number:
            print(f"Congratulations! You guessed the secret number ({secret_number}) in {attempts} attempt{"s" if attempts > 1 else ""}.")
            break
        elif not command.isdigit():
            if command == "attempts":
                print(f"Attempts: {attempts}")
            elif command == "help":
                print("attempts - See how many guesses you made.")
                print("help - Show all commands.")
                print("exit - Exit the application.")
            elif command == "exit":
                print("Goodbye, User!")
                break
            else:
                print("Invalid input. Please enter a number.")
        else:
            attempts += 1
            if lives != -1:
                lives -= 1
                print_lives()
                if lives <= 0:
                    print("Game Over! You ran out of lives.")
                    break