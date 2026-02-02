from scripts.utils import run_checkList, color, clear, get_available_checklists, get_checklist_phases, get_integer

current_checklist = 0
completed = []

# Function to run the submenus
def run_menu():
    
    checklists = get_available_checklists()

    if not checklists:
        print("Error: No Checklists Found! Add .json files to the checklist folder, see README.txt for more details")
        return

    aircraft_type = main_menu()

    if aircraft_type:
        checklist_menu(aircraft_type)
        return

# Initial Menu of the application
def main_menu():
    
    option = 0
    aircraft_type = get_available_checklists()[0]

    while option != 3:
        # MENU
        clear()
        print("\n  ****  Main Menu  ****")
        print(f"\n                                           Aircraft Type: {aircraft_type}")
        print("1. Go to Checklist")
        print("2. Change Aircraft Type")
        print("3. Exit")
        option = get_integer()

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

# Menu to allow user to select and aircraft
def select_aircraft():
    
    option = 0
    supported_aircrafts = get_available_checklists()
    global current_checklist, completed
    current_checklist = 0
    completed = []
    length = len(supported_aircrafts)

    while option != length + 1:
        
        #MENU
        clear()
        print("\n  ****  Choose Aircraft Type  ****")
        
        for i in range(length):
            print(f"{i + 1}. {supported_aircrafts[i]}")
        
        print(f"{length + 1}. Back")
        option = get_integer()

        if option < 1 or option > length + 1:
            print("Invalid Option!")
            continue

        if option == length + 1:
            return False
        
        return supported_aircrafts[option - 1]
        
# Menu to let user chose the menu item
def checklist_menu(aircraft_type):
    
    option = 0
    flight_phases = get_checklist_phases(aircraft_type)
    length = len(flight_phases)
    global current_checklist, completed
    
    while option != 14:

        clear()
        print("\n  ****  Checklist  ****")
        print(f"\n                                           Aircraft Type: {aircraft_type}")
        
        for i in range(length):

            if i in completed:
                print(color(f"{i + 1}. {flight_phases[i]} ✓", "GREEN"))

            elif i < current_checklist - 1:
                print(color(f"{i + 1}. {flight_phases[i]} ✗", "RED"))
            
            else:         
                print(f"{i + 1}. {flight_phases[i]}")

        print(f"{length + 1}. Back")
        option = get_integer()

        if option < 1 or option > length + 1:
            print("Invalid Option!")
            continue

        if option == length + 1:
            run_menu()
            return
        
        run_checkList(aircraft_type, flight_phases[option - 1])
        
        completed.append(option - 1)
        current_checklist = option