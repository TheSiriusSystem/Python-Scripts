import random

GREETINGS: list[str] = [
    "Alert: {user_name} has entered the chat. Prepare for chaos.",
    "Loading awesomeness... 100% complete. Welcome, {user_name}!",
    "Sup {user_name}, you up?",
    "New challenger approaches: {user_name}!",
    "Hey {user_name}, did you bring snacks this time?",
    "Hey {user_name}, just a reminder—you matter.",
    "Welcome back, beautiful soul.",
    "You’re doing amazing, {user_name}. Let’s keep going~!",
    "Glad to see you, {user_name}. You make today brighter.",
    "Hey hey~ I’m proud of you just for showing up.",
]
STATIC_GREETING: str = "Hello, {user_name}!"

if __name__ == "__main__":
    while True:
        user_name: str = input("Enter your name... ").strip()
        if user_name == "":
            print("Invalid option. Please enter a name.")
            continue

        while True:
            use_random_greeting: str = input("Would you like a random greeting? (Y/N) ").strip().lower()
            if use_random_greeting in ["y", "n"]:
                break
            print("Invalid option. Please enter Y or N.")

        print((random.choice(GREETINGS) if use_random_greeting == "y" else STATIC_GREETING).format(
            user_name=user_name
        ))
        break