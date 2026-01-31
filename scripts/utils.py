import json
import pyttsx3
import time
import os


# CONSTANTS

# Base file path of checklists .json files
BASE_PATH = "checklists/"

title = "        ********    Welcome to VCHECKLIST    ********"

# Colors to be used in the terminal
class bcolors:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'


# TERMINAL

# Color the text
def color(text, color):

    match color:
        case "GREEN":
            return f"{bcolors.OKGREEN}{text}{bcolors.ENDC}"
        case "CYAN":
            return f"{bcolors.OKCYAN}{text}{bcolors.ENDC}"
        case "RED":
            return f"{bcolors.WARNING}{text}{bcolors.ENDC}"
        case _:
            return text

# Clear the terminal
def clear():
    print('\033[2J\033[H', end='', flush=True)
    print(title)


# FILES

# Load the checklist .json file
def load_checklist(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        
    return dict(data)


# TTS

# Transform text into speech
def say(item):
    time.sleep(1)
    engine = pyttsx3.init()
    engine.say(item)
    engine.runAndWait()
    engine.stop()


# CHECKLIST

# Go through all checklist items for a specific flight phase
def run_checkList(aircraft, phase):
    clear()
    file_path = f"{BASE_PATH}{aircraft}.json"
    checklist = load_checklist(file_path)
    
    items = checklist[phase]

    initial_phrase = f"\n{phase} Checklist!"
    print(color(initial_phrase, "CYAN"))
    say(initial_phrase)
    
    for item in (items):
        say(item)
        print(color(f"{item} ✓", "GREEN"))
        
    final_phrase = f"{initial_phrase.lstrip("\n").rstrip("!")} Completed!" 
    print(color(f"{final_phrase}", "CYAN"))
    say(final_phrase)
    

# Get Available Checklists:
def get_available_checklists():
    checklists = []

    for file in os.listdir(BASE_PATH):

        if file != "template.json" and file.endswith(".json"):
            checklists.append(file.rstrip(".json"))

    checklists.sort()

    return checklists

# Get Checklists phases
def get_checklist_phases(aircacft):
    
    file_path = f"{BASE_PATH}{aircacft}.json"
    checklist = load_checklist(file_path)

    return list(checklist.keys())

# INPUT
def get_integer():

    integer_received = False
    while not integer_received:
        try:
            value = int(input(": "))
            integer_received = True
        except:
            print("Invalid Entry!")

    return value


