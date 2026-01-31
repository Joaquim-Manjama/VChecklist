from scripts.utils import run_checkList, color, clear

def run_menu():
    aircraft_type = main_menu()

    if aircraft_type:
        checklist_menu(aircraft_type)
        return

def main_menu():
    option = 0
    aircraft_type = "C172"

    while option != 3:
        # MENU
        clear()
        print("\n  ****  Main Menu  ****")
        print(f"\n                                           Aircraft Type: {aircraft_type}")
        print("1. Go to Checklist")
        print("2. Change Aircraft Type")
        print("3. Exit")
        option = int(input(": "))

        match option:
            case 1: return aircraft_type
            case 2: 
                next_aircraft_type = select_aircraft()
                if next_aircraft_type:
                    aircraft_type = next_aircraft_type
            case 3: 
                print("Thanks for using VChecklist!")
                return False
            case _: 
                print("Invalid Option!")

def select_aircraft():
    option = 0
    supported_aircrafts = ["A320", "A330", "A340", "A350", "A380", "B737", "B757", "B767", "B777", "B787", "E140", "E190"]
    length = len(supported_aircrafts)

    while option != length + 1:
        #MENU
        clear()
        print("\n  ****  Choose Aircraft Type  ****")
        for i in range(length):
            print(f"{i + 1}. {supported_aircrafts[i]}")
        print(f"{length + 1}. Back")
        option = int(input(": "))

        if option < 1 or option > length + 1:
            print("Invalid Option!")
            continue

        if option == length + 1:
            return False
        
        return supported_aircrafts[option - 1]
        
def checklist_menu(aircraft_type):
    option = 0
    
    flight_phases = [   "Preflight", "Before Start", "After Start", "Before Taxi", 
                        "Before Takeoff", "After Takeoff", "Climb", "Cruise", 
                        "Descent", "Approach", "Landing", "Shutdown"]
    
    completed_checks = []

    length = len(flight_phases)
    
    while option != 14:

        clear()
        print("\n  ****  Checklist  ****")
        print(f"\n                                           Aircraft Type: {aircraft_type}")
        
        for i in range(length):

            if flight_phases[i] in completed_checks:
                print(color(f"{i + 1}. {flight_phases[i]}", "GREEN"))
            else:
                print(f"{i + 1}. {flight_phases[i]}")

        print(f"{length + 1}. Back")

        option = int(input(": "))

        if option < 1 or option > length + 1:
            print("Invalid Option!")
            continue

        if option == length + 1:
            run_menu()
            return
        
        run_checkList(aircraft_type, flight_phases[option - 1])
        
        if not flight_phases[option - 1] in completed_checks:
            completed_checks.append(flight_phases[option - 1])