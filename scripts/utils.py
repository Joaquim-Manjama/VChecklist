import json
import pyttsx3
import time
import os

BASE_PATH = "checklists/"
title = "        ********    Welcome to VCHECKLIST    ********"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_checklist(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        
    return dict(data)

def say(item):
    print(color(item, "CYAN"))
    engine = pyttsx3.init()
    time.sleep(1)
    engine.say(item)
    engine.runAndWait()
    engine.stop()

def run_checkList(aircraft, phase) :
    clear()
    file_path = f"{BASE_PATH}{aircraft}.json"
    checklist = load_checklist(file_path)
    
    items = checklist[phase]

    initial_phrase = f"{phase} Checklist!"
    say(initial_phrase)

    for item in items:
        say(item)

    final_phrase = f"{initial_phrase.rstrip("!")} Completed!" 
    say(final_phrase)


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
        
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(title)