import random

STARTING_CAR_FUEL: int = 100

is_car_on: bool = False
car_fuel: int = STARTING_CAR_FUEL
was_car_fuel_warning_shown: bool = False

def command_start() -> None:
    global is_car_on
    if not is_car_on:
        is_car_on = True
        print("Car started... ready to go!")
    else:
        print("Car is already started!")

def command_stop() -> None:
    global is_car_on
    if is_car_on:
        is_car_on = False
        print("Car stopped.")
    else:
        print("Car is already stopped!")

def command_drive() -> None:
    if is_car_on:
        global car_fuel
        if car_fuel > 0:
            requested_fuel_spent: int = random.randint(5, 10)
            actual_fuel_spent: int = min(car_fuel, requested_fuel_spent)
            car_fuel -= actual_fuel_spent
            print(f"You drove the car around. Spent {actual_fuel_spent}% fuel.")

            global was_car_fuel_warning_shown
            if not was_car_fuel_warning_shown and car_fuel <= 20:
                was_car_fuel_warning_shown = True
                print("The car is nearly out of fuel...")

            if car_fuel == 0:
                print("The car ran out of fuel and sputtered to a stop!")
        else:
            print("The car is out of fuel!")
    else:
        print("The car is OFF!")

def command_refuel() -> None:
    global car_fuel
    if car_fuel != STARTING_CAR_FUEL:
        car_fuel = STARTING_CAR_FUEL
        global was_car_fuel_warning_shown
        was_car_fuel_warning_shown = False
        print("You refueled the car.")
    else:
        print("The car already has enough fuel!")

def command_status() -> None:
    print(f"The car is currently {"ON" if is_car_on else "OFF"} and has {car_fuel}% fuel.")

def command_help() -> None:
    print("start - Start the car.")
    print("stop - Stop the car.")
    print("drive - Take the car around for a spin.")
    print("refuel - Refuel the car.")
    print("status - Check the car's status.")
    print("help - Show all commands.")
    print("exit - Exit the application.")

if __name__ == "__main__":
    commands: dict = {
        "start": command_start,
        "stop": command_stop,
        "drive": command_drive,
        "refuel": command_refuel,
        "status": command_status,
        "help": command_help,
    }

    print("Welcome to Console Car Simulator!")
    print("Type 'help' to see available commands.")
    while True:
        command: str = input("> ").strip().lower()
        if command == "exit":
            print("Goodbye, User!")
            break
        elif command in commands:
            commands[command]()
        else:
            print("Invalid command.")