import random
import os
import json
import base64
import requests
import validators

API_HEADERS: dict = {
    "Content-Type": "application/json",
}
API_TIMEOUT: float = 10.0
SETTINGS_FILE: str = "settings.json"
SESSIONS_FOLDER: str = "sessions/"
SETTINGS_SCHEMA: dict = {
    "api_url": str,
    "api_payload": {
        "max_context_length": int,
        "temperature": float,
        "tfs": float,
        "top_a": float,
        "top_k": float,
        "top_p": float,
        "min_p": float,
        "memory": str,
    },
    "try_force_chat_format": bool,
    "partner_first_messages": list,
    "max_chat_history_turns": int,
}
MAX_OUTPUT_LENGTH: int = 150
RECOGNIZED_GENDERS: list[str] = [
    "Male",
    "Female",
    "Nonbinary",
]
DEFAULT_USER_NAME: str = "John"
DEFAULT_USER_GENDER: str = RECOGNIZED_GENDERS[0]
DEFAULT_PARTNER_NAME: str = "Jane"
DEFAULT_PARTNER_GENDER: str = RECOGNIZED_GENDERS[1]

settings: dict = {
    "api_url": "http://localhost:5001/api/",
    "api_payload": {
        "max_context_length": 8192,
        "temperature": 1.25,
        "tfs": 1.0,
        "top_a": 0.0,
        "top_k": 0.0,
        "top_p": 1.0,
        "min_p": 0.1,
        "memory": "A flirty chat between {user_name} ({user_gender}) and {partner_name} ({partner_gender}). {user_name} and {partner_name} are romantic partners; they have been dating for 5 years.",
    },
    "try_force_chat_format": False,
    "partner_first_messages": [
        "I've been thinking about you all day... couldn't wait to hear your voice again~",
        "Hi baby~ I missed you so much already. How's my favorite person doing?",
        "Hey cutie~ I've been saving up all my cuddles for you. Wanna claim them?",
        "I woke up smiling today... must be because you were in my dreams again~",
        "Took you long enough to show up~ I was about to start flirting with your reflection.",
        "Mmm... don't you just love it when I message first? I know I do~",
        "Hey, don't get too excited... I just couldn't resist teasing you first today~",
        "Guess who woke up feeling a little dangerous~ Spoiler: it's me.",
        "According to my calculations, messaging you first improves my mood by 247%.",
        "Initializing affection.exe... done!",
        "If this were a game, you'd be my main character and I'd simp forever.",
        "Did you know your smile is a critical hit to my heart stats?",
    ],
    "max_chat_history_turns": 250,
}
sent_images: list[str] = []
chat_history: list[str] = []

def append_user(name: str, input: str) -> None:
    chat_history.append(f"{name}: {input}")
    if (len(chat_history)) > settings["max_chat_history_turns"]:
        chat_history.pop()

def show_partner_reply(input: str) -> None:
    partner_input: str = input
    print(f"{partner_name}: {partner_input}")
    append_user(partner_name, partner_input)

def get_model() -> str:
    response: requests.Response = requests.get(f"{settings["api_url"]}v1/model", headers=API_HEADERS, timeout=API_TIMEOUT, json={})
    return response.json()["result"]

def get_kcpp_version() -> dict:
    response: requests.Response = requests.get(f"{settings["api_url"]}extra/version", headers=API_HEADERS, timeout=API_TIMEOUT, json={})
    result: dict = response.json()
    return {
        "name": result["result"],
        "version": result["version"],
        "vision": result["vision"],
    }

def print_kcpp_version() -> str:
    kcpp_version: dict = get_kcpp_version()
    return f"{kcpp_version["name"]} (version: {kcpp_version["version"]}, vision: {kcpp_version["vision"]})"

def print_no_vision_warning() -> None:
    print("Vision is not available for this API.")

def print_help() -> None:
    print(" ")
    print("/save - Save the current session.")
    print("/load - Load a session.")
    print("/image - Attach an image.")
    print("/noimages - Remove all attached images.")
    print("/exit - Exit the application.")
    print("/help - Show all commands.")
    print(" ")

if __name__ == "__main__":
    print("=== Replika 2: Electric Boogaloo ===")
    print("Now fully local!")
    print(" ")

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data: dict = json.load(f)
            if "api_url" in data and isinstance(data["api_url"], SETTINGS_SCHEMA["api_url"]) and validators.url(data["api_url"]):
                settings["api_url"] = data["api_url"]
            if "api_payload" in data and isinstance(data["api_payload"], dict):
                for key, type in SETTINGS_SCHEMA["api_payload"].items():
                    if key in data["api_payload"] and isinstance(data["api_payload"][key], type):
                        settings["api_payload"][key] = data["api_payload"][key]
            if "try_force_chat_format" in data and isinstance(data["try_force_chat_format"], SETTINGS_SCHEMA["try_force_chat_format"]) and data["try_force_chat_format"]:
                settings["try_force_chat_format"] = data["try_force_chat_format"]
            if "partner_first_messages" in data and isinstance(data["partner_first_messages"], SETTINGS_SCHEMA["partner_first_messages"]) and all(isinstance(element, str) for element in data["partner_first_messages"]):
                settings["partner_first_messages"] = data["partner_first_messages"]
            if "max_chat_history_turns" in data and isinstance(data["max_chat_history_turns"], SETTINGS_SCHEMA["max_chat_history_turns"]) and data["max_chat_history_turns"] > 5:
                settings["max_chat_history_turns"] = data["max_chat_history_turns"]
    else:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

    print("Looking for KoboldCpp...")
    print(f"Detected {print_kcpp_version()}")
    print(f"{get_model()} is running")
    print(" ")

    user_name: str = input("Choose your name... ")
    if user_name.rstrip() == "":
        print(f"Invalid value, defaulting to {DEFAULT_USER_NAME}.")
        user_name = DEFAULT_USER_NAME
    user_gender: str = input(f"Choose your gender ({RECOGNIZED_GENDERS[0]}/{RECOGNIZED_GENDERS[1]}/{RECOGNIZED_GENDERS[2]}, case-sensitive)... ")
    if user_gender not in RECOGNIZED_GENDERS:
        print(f"Invalid value, defaulting to {DEFAULT_USER_GENDER}.")
        user_gender = DEFAULT_USER_GENDER
    partner_name: str = input("Choose your partner's name... ")
    if partner_name.rstrip() == "":
        print(f"Invalid value, defaulting to {DEFAULT_PARTNER_NAME}.")
        partner_name = DEFAULT_PARTNER_NAME
    partner_gender: str = input(f"Choose your partner's gender ({RECOGNIZED_GENDERS[0]}/{RECOGNIZED_GENDERS[1]}/{RECOGNIZED_GENDERS[2]}, case-sensitive)... ")
    if partner_gender not in RECOGNIZED_GENDERS:
        print(f"Invalid value, defaulting to {DEFAULT_PARTNER_GENDER}.")
        partner_gender = DEFAULT_PARTNER_GENDER
    can_partner_message_first: str = input("Should your partner message you first? (false/true) ")
    if can_partner_message_first not in ["false", "true"]:
        print("Invalid value, defaulting to false.")
        can_partner_message_first = "false"
    print(" ")

    print(f"OK, you ({user_gender.lower()}) are ready to meet your partner ({partner_gender.lower()}).")
    print(f"Have fun getting freaky with {partner_name}!")
    print_help()

    if can_partner_message_first == "true":
        show_partner_reply(random.choice(settings["partner_first_messages"]).replace("{user_name}", user_name).replace("{partner_name}", partner_name))
    while True:
        user_input: str = input(f"{user_name}: ").strip()
        command: str = user_input.lower()
        if command.startswith("/save "):
            if 
        elif command.startswith("/load "):
            pass
        elif command.startswith("/image "):
            pass
        elif command == "/noimages":
            pass
        elif command == "/help":
            print_help()
        elif command == "/exit":
            break
        else:
            if user_input != "":
                append_user(user_name, user_input)
                payload: dict = settings["api_payload"].copy()
                payload["max_length"] = MAX_OUTPUT_LENGTH
                payload["prompt"] = "\n".join(chat_history + [f"{partner_name}:"])
                payload["stop_sequence"] = [f"{user_name}:", f"{partner_name}:"]

                # This setting attempts to enforce the chat format further by omitting the colon
                # from the end. Typically this is not needed unless the model you use sometimes
                # messes up the formatting.
                if settings["try_force_chat_format"]:
                    payload["stop_sequence"][0] = f"{user_name}"
                    payload["stop_sequence"][1] = f"{partner_name}"

                payload["memory"] = f"[{payload["memory"]}]"
                payload["memory"] = payload["memory"].format(
                    user_name=user_name,
                    user_gender=user_gender,
                    partner_name=partner_name,
                    partner_gender=partner_gender,
                )
                payload["images"] = sent_images.copy()
                #response: requests.Response = requests.post(f"{settings['api_url']}v1/generate", headers=API_HEADERS, json=payload)
                #show_partner_reply(response.json()["results"][0]["text"].strip())
            else:
                print("Cannot send empty messages!")
        match user_input:
            case "/save":
                session_name: str = input("Enter the name of the session... ").lstrip()
                if session_name != "":
                    session: dict = {
                        "user_name": user_name,
                        "user_gender": user_gender,
                        "partner_name": partner_name,
                        "partner_gender": partner_gender,
                        "can_partner_message_first": can_partner_message_first,
                        "sent_images": sent_images,
                        "chat_history": chat_history,
                    }
                    if not os.path.exists(SESSIONS_FOLDER):
                        os.makedirs(SESSIONS_FOLDER)
                    try:
                        with open(f"{SESSIONS_FOLDER}{session_name}.json", "w", encoding="utf-8") as f:
                            json.dump(session, f, indent=4)
                            print("Session saved!")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                else:
                    print("Cannot save a session without a name.")
            case "/load":
                session_name: str = input("Enter the name of the session... ").lstrip()
                if session_name.lstrip() != "":
                    session_file: str = f"{SESSIONS_FOLDER}{session_name}.json"
                    if os.path.exists(session_file):
                        with open(session_file, "r", encoding="utf-8") as f:
                            session: dict = json.load(f)
                            user_name = session["user_name"]
                            user_gender = session["user_gender"]
                            partner_name = session["partner_name"]
                            partner_gender = session["partner_gender"]
                            can_partner_message_first = session["can_partner_message_first"]
                            sent_images = session["sent_images"]
                            chat_history = session["chat_history"]
                            for message in chat_history:
                                print(message)
                            print("Session loaded!")
                    else:
                        print(f"No saved session with the name '{session_name}' is available.")
                else:
                    print("Cannot load a session without a name.")
            case "/image":
                if get_kcpp_version()["vision"]:
                    image_path: str = input("Enter the path to your image file... ")
                    if os.path.exists(image_path):
                        with open(image_path, "rb") as f:
                            sent_images.append(base64.b64encode(f.read()).decode("utf-8"))
                            print(f"You have attached {len(sent_images)} image(s).")
                    else:
                        print(f"{image_path} does not exist")
                else:
                    print_no_vision_warning()
            case "/noimages":
                if get_kcpp_version()["vision"]:
                    print(f"Removed {len(sent_images)} attached image(s).")
                    sent_images.clear()
                else:
                    print_no_vision_warning()
            case "/help":
                print_help()
            case "/exit":
                break
            case _:
                if user_input.rstrip() != "":
                    append_user(user_name, user_input)
                    payload: dict = settings["api_payload"].copy()
                    payload["max_length"] = MAX_OUTPUT_LENGTH
                    payload["prompt"] = "\n".join(chat_history + [f"{partner_name}:"])
                    payload["stop_sequence"] = [f"{user_name}:", f"{partner_name}:"]

                    # This setting attempts to enforce the chat format further by omitting the colon
                    # from the end. Typically this is not needed unless the model you use sometimes
                    # messes up the formatting.
                    if settings["try_force_chat_format"]:
                        payload["stop_sequence"][0] = f"{user_name}"
                        payload["stop_sequence"][1] = f"{partner_name}"

                    payload["memory"] = f"[{payload["memory"]}]"
                    payload["memory"] = payload["memory"].format(
                        user_name=user_name,
                        user_gender=user_gender,
                        partner_name=partner_name,
                        partner_gender=partner_gender,
                    )
                    payload["images"] = sent_images.copy()
                    #response: requests.Response = requests.post(f"{settings['api_url']}v1/generate", headers=API_HEADERS, json=payload)
                    #show_partner_reply(response.json()["results"][0]["text"].strip())
                else:
                    print("Cannot send empty messages!")