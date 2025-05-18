import random

lives: int = 3
secret_number: str = str(random.randint(0, 10))

def print_lives() -> None:
    print(f"Lives: {lives}")

if __name__ == "__main__":
    print("Guess the secret number!")
    print(" ")
    print_lives()
    while True:
        guess: str = input("> ")
        if guess == secret_number:
            print("CONGRATULATIONS!")
            break
        elif not guess.isdigit():
            print("Invalid guess.")
        else:
            lives -= 1
            print_lives()
            if lives <= 0:
                print("You lost the game!")
                break