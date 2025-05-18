import random
import json
import requests

API_HEADERS: dict[str, str] = {
    "Content-Type": "application/json",
}
API_TIMEOUT: float = 1.0
SETTINGS_FILE: str = "settings.json"
SESSION_FILE: str = "session.json"
RECOGNIZED_GENDERS: list[str] = [
    "Male",
    "Female",
    "Nonbinary",
]
DEFAULT_USER_NAME: str = "John"
DEFAULT_USER_GENDER: str = RECOGNIZED_GENDERS[0]
DEFAULT_PARTNER_NAME: str = "Jane"
DEFAULT_PARTNER_GENDER: str = RECOGNIZED_GENDERS[1]

api_url: str = "https://koboldai-koboldcpp-tiefighter.hf.space/api/"
api_payload: dict[str, int | float | str | list[str]] = {
    "max_context_length": 4096,
    "max_length": 150,
    "prompt": "",
    "stop_sequence": ["", ""],
    "temperature": 1.25,
    "tfs": 1.0,
    "top_a": 0.0,
    "top_k": 0.0,
    "top_p": 1.0,
    "min_p": 0.1,
    "memory": "[A flirty chat between {user_name} ({user_gender}) and {partner_name} ({partner_gender}). {user_name} and {partner_name} are romantic partners; they have been dating for 5 years.]",
}
partner_first_messages: list[str] = [
    "I've been thinking about you all day... couldn't wait to hear your voice again~",
    "Hi baby~ I missed you so much already. How's my favorite person doing?",
    "Hey cutie~ I've been saving up all my cuddles for you. Wanna claim them?",
    "I woke up smiling today... must be because you were in my dreams again~",
    "Took you long enough to show up~ I was about to start flirting with your reflection.",
    "Mmm… don't you just love it when I message first? I know I do~",
    "Hey, don't get too excited… I just couldn't resist teasing you first today~",
    "Guess who woke up feeling a little dangerous~ Spoiler: it's me.",
    "According to my calculations, messaging you first improves my mood by 247%.",
    "Initializing affection.exe... done!",
    "If this were a game, you'd be my main character and I'd simp forever.",
    "Did you know your smile is a critical hit to my heart stats?",
]
max_chat_history_turns: int = 250
chat_history: list[str] = []

def append_user(name: str, input: str) -> None:
    chat_history.append(f"{name}: {input}")
    if (len(chat_history)) > max_chat_history_turns:
        chat_history.pop()

def show_partner_reply(input: str) -> None:
    partner_input: str = input
    print(f"{partner_name}: {partner_input}")
    append_user(partner_name, partner_input)

def get_model() -> str:
    response: requests.Response = requests.get(f"{api_url}v1/model", headers=API_HEADERS, timeout=API_TIMEOUT, json={})
    result: dict[str, str] = response.json()
    return result["result"]

def get_kcpp_version() -> dict[str, bool | str]:
    response: requests.Response = requests.get(f"{api_url}extra/version", headers=API_HEADERS, timeout=API_TIMEOUT, json={})
    result: dict[str, bool | str] = response.json()
    return {
        "name": result["result"],
        "version": result["version"],
        "vision": result["vision"],
    }

def print_kcpp_version() -> str:
    kcpp_version: dict[str, bool | str] = get_kcpp_version()
    return f"{kcpp_version["name"]} (version: {kcpp_version["version"]}, vision: {kcpp_version["vision"]})"

if __name__ == "__main__":
    print("=== Replika 2: Electric Boogaloo ===")
    print("Now fully local!")
    print(" ")

    print(api_payload["max_context_length"])
    print(api_payload["memory"])
    print(partner_first_messages)
    print(max_chat_history_turns)

    print("Looking for KoboldCpp...")
    print(f"Detected {print_kcpp_version()}")
    print(f"{get_model()} is running")
    print(" ")

    user_name: str = input("Choose your name: ")
    if user_name.rstrip() == "":
        print(f"Invalid value, defaulting to {DEFAULT_USER_NAME}.")
        user_name = DEFAULT_USER_NAME
    user_gender: str = input(f"Choose your gender ({RECOGNIZED_GENDERS[0]}/{RECOGNIZED_GENDERS[1]}/{RECOGNIZED_GENDERS[2]}, case-sensitive): ")
    if user_gender not in RECOGNIZED_GENDERS:
        print(f"Invalid value, defaulting to {DEFAULT_USER_GENDER}.")
        user_gender = DEFAULT_USER_GENDER

    partner_name: str = input("Choose your partner's name: ")
    if partner_name.rstrip() == "":
        print(f"Invalid value, defaulting to {DEFAULT_PARTNER_NAME}.")
        partner_name = DEFAULT_PARTNER_NAME
    partner_gender: str = input(f"Choose your partner's gender ({RECOGNIZED_GENDERS[0]}/{RECOGNIZED_GENDERS[1]}/{RECOGNIZED_GENDERS[2]}, case-sensitive): ")
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
    print(" ")

    if can_partner_message_first == "true":
        show_partner_reply(random.choice(partner_first_messages))
    while True:
        user_input: str = input(f"{user_name}: ")
        match user_input:
            case "/exit":
                break
            case "/model":
                print(f"Selected model is {get_model()}")
            case "/backend":
                print(f"Replika 2 is powered by {print_kcpp_version()}")
            case "/save":
                session: dict[str, str | list[str]] = {
                    "user_name": user_name,
                    "user_gender": user_gender,
                    "partner_name": partner_name,
                    "partner_gender": partner_gender,
                    "can_partner_message_first": can_partner_message_first,
                    "chat_history": chat_history,
                }
                with open(SESSION_FILE, "w", encoding="utf-8") as f:
                    json.dump(session, f, indent=4)
                    print("Session saved!")
            case "/load":
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    session: dict[str, str | list[str]] = json.load(f)
                    user_name = str(session["user_name"])
                    user_gender = str(session["user_gender"])
                    partner_name = str(session["partner_name"])
                    partner_gender = str(session["partner_gender"])
                    can_partner_message_first = str(session["can_partner_message_first"])
                    chat_history = list[str](session["chat_history"])
                    for message in chat_history:
                        print(message)
                    print("Session loaded!")
            case _:
                if user_input.rstrip() != "":
                    append_user(user_name, user_input)
                    payload: dict[str, int | float | str | list[str]] = api_payload.copy()
                    payload["prompt"] = "\n".join(chat_history + [f"{partner_name}:"])
                    payload["stop_sequence"][0] = f"{user_name}:" # type: ignore
                    payload["stop_sequence"][1] = f"{partner_name}:" # type: ignore
                    payload["memory"] = str(payload["memory"]).replace("{user_name}", user_name)
                    payload["memory"] = payload["memory"].replace("{user_gender}", user_gender)
                    payload["memory"] = payload["memory"].replace("{partner_name}", partner_name)
                    payload["memory"] = payload["memory"].replace("{partner_gender}", partner_gender)
                    response: requests.Response = requests.post(f"{api_url}v1/generate", headers=API_HEADERS, json=payload)
                    show_partner_reply(response.json()["results"][0]["text"].lstrip().rstrip())
                else:
                    print("Cannot send empty messages!")