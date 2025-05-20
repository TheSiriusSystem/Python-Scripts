import random

GREETINGS: list[str] = [
    "Hello, {user_name}!",
]

if __name__ == "__main__":
    user_name: str = input("Enter your name... ")
    print(random.choice(GREETINGS).format(
        user_name=user_name,
    ))