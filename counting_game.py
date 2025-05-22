import sys
import time

GOAL: int = 10
VALID_DIFFICULTIES: list[str] = [
    "easy",
    "normal",
    "hard",
    "expert",
]
FORMATTED_VALID_DIFFICULTIES: str = "/".join(VALID_DIFFICULTIES)

def print_invalid_number_warning() -> None:
    print("Invalid input. Please enter the next number.")

if __name__ == "__main__":
    while True:
        goal_time: float = 5.5

        while True:
            difficulty: str = input(f"Choose a difficulty... ({FORMATTED_VALID_DIFFICULTIES}) ").strip().lower()
            if difficulty not in VALID_DIFFICULTIES:
                print(f"Invalid option. Please choose ({FORMATTED_VALID_DIFFICULTIES}).")
                continue
            if difficulty == VALID_DIFFICULTIES[0]: # Easy
                goal_time = 8.0
            elif difficulty == VALID_DIFFICULTIES[2]: # Hard
                goal_time = 4.0
            elif difficulty == VALID_DIFFICULTIES[3]: # Expert
                goal_time = 3.25
            break

        count: int = 0
        initial_time: float = time.time()

        print(f"Count from {count + 1} to {GOAL} within {goal_time} seconds!")
        print("Type 'exit' to exit the game.")
        while True:
            command: str = input("> ").strip().lower()
            if command.isdigit():
                if int(command) == count + 1:
                    count += 1

                    elapsed_time: float = time.time() - initial_time
                    formatted_elapsed_time: str = "{:.2f}".format(elapsed_time)

                    if elapsed_time > goal_time:
                        print(f"Game Over! You tried to count for {formatted_elapsed_time} seconds.")
                        break
                    if count == GOAL:
                        print(f"Congratulations! You counted to {GOAL} in {formatted_elapsed_time} seconds.")
                        break
                else:
                    print_invalid_number_warning()
            else:
                if command == "exit":
                    print("Goodbye, User!")
                    sys.exit()
                else:
                    print_invalid_number_warning()

        while True:
            play_again: str = input("Would you like to play again? (Y/N) ").strip().lower()
            if play_again not in ["y", "n"]:
                print("Invalid option. Please choose Y or N.")
                continue
            break
        if play_again == "n":
            break