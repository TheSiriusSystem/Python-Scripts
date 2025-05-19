is_car_on: bool = False

if __name__ == "__main__":
    print("Welcome to Console Car Simulator! Type 'help' to see available commands.")
    while True:
        command: str = input("> ").strip().lower()
        match command:
            case "start":
                if not is_car_on:
                    is_car_on = True
                    print("Car started... ready to go!")
                else:
                    print("Car is already started!")
            case "stop":
                if is_car_on:
                    is_car_on = False
                    print("Car stopped.")
                else:
                    print("Car is already stopped!")
            case "exit":
                print("Goodbye, User!")
                break
            case "help":
                print("start - Start the car.")
                print("stop - Stop the car.")
                print("exit - Exit the application.")
                print("help - Show all commands.")
            case _:
                print("Sorry, I don't understand that...")