import random

VALID_DIFFICULTIES: list[str] = [
    "baby",
    "easy",
    "normal",
    "hard",
    "impossible",
]
LIFE_SYSTEM_DISABLER: int = -1

def print_lives() -> None:
    print(f"Lives: {lives}")

if __name__ == "__main__":
    while True:
        guess_range_min: int = 1
        guess_range_max: int = 100
        lives: int = LIFE_SYSTEM_DISABLER
        disable_hints: bool = False

        while True:
            difficulty: str = input(f"Choose a difficulty... ({"/".join(VALID_DIFFICULTIES)}) ").strip().lower()
            if difficulty not in VALID_DIFFICULTIES:
                print(f"Invalid option. Please choose ({"/".join(VALID_DIFFICULTIES)}).")
                continue
            if difficulty == VALID_DIFFICULTIES[0]: # Baby
                guess_range_max = 10
            elif difficulty == VALID_DIFFICULTIES[1]: # Easy
                guess_range_max = 50
            elif difficulty == VALID_DIFFICULTIES[3]: # Hard
                guess_range_min = 0
                lives = 7
            elif difficulty == VALID_DIFFICULTIES[4]: # Impossible
                guess_range_min = 0
                guess_range_max = 125
                lives = 5
                disable_hints = True
            break

        secret_number: int = random.randint(guess_range_min, guess_range_max)
        attempts: int = 0

        print(f"Guess the number between {guess_range_min} and {guess_range_max}!")
        print("Type 'help' to see available commands.")
        print("")
        if lives != LIFE_SYSTEM_DISABLER:
            print_lives()
        while True:
            command: str = input("> ").strip().lower()
            if command.isdigit():
                guess: int = int(command)
                if guess >= guess_range_min and guess <= guess_range_max:
                    attempts += 1
                    if guess == secret_number:
                        print(f"Correct! The number is {secret_number}. You guessed it in {attempts} attempt{"s" if attempts > 1 else ""}.")
                        break
                    else:
                        if not disable_hints:
                            if guess < secret_number:
                                print("Too low!")
                            elif guess > secret_number:
                                print("Too high!")
                        else:
                            print("Wrong guess!")

                        if lives != LIFE_SYSTEM_DISABLER:
                            lives -= 1
                            if lives > 0:
                                print_lives()
                            else:
                                print(f"Game Over! The number was {secret_number}. Better luck next time.")
                                break
                else:
                    print("Invalid input.")
            else:
                match command:
                    case "attempts":
                        print(f"Attempts: {attempts}")
                    case "help":
                        print("attempts - See how many guesses you made.")
                        print("help - Show all commands.")
                        print("exit - Exit the application.")
                    case "exit":
                        print("Goodbye, User!")
                        break
                    case _:
                        print("Invalid input. Please enter a number.")

        while True:
            play_again: str = input("Would you like to play again? (Y/N) ").strip().lower()
            if play_again not in ["y", "n"]:
                print("Invalid option. Please choose Y or N.")
                continue
            break
        if play_again == "n":
            break