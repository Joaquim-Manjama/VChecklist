from scripts.utils import run_checkList

print("        ********    Welcome to VCHECKLIST    ********")

main_op = 0
aircraft_type = "C172"
divisor = "#####################################################"


while main_op != 14:

    # MENU
    print("\n                                           Aircraft Type: " + aircraft_type)
    print("1. Preflight")
    print("2. Before Start")
    print("3. After Start") 
    print("4. Before Taxi")
    print("5. Before Takeoff")
    print("6. After Takeoff")
    print("7. Climb")
    print("8. Cruise")
    print("9. Descent")
    print("10. Approach")
    print("11. Landing")
    print("12. Shutdown")
    print("13. Change Aircraft Type")
    print("14. Exit")
    main_op = int(input(": "))

    match main_op:
        case 14:
            print("Thanks for using VChecklist!")
        case _:
            print("Invalid option!")
            print(divisor)
        