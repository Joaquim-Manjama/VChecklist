import json
import pyttsx3
import time

BASE_PATH = "checklists/"

def load_checklist(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        
    return dict(data)

def say(item):
    time.sleep(1)
    print(item)
    engine = pyttsx3.init()
    engine.say(item)
    engine.runAndWait()
    engine.stop()

def run_checkList(aircraft, phase) :
    file_path = BASE_PATH + aircraft + ".json"
    checklist = load_checklist(file_path)
    
    items = checklist[phase]

    initial_phrase = phase + " Checklist!"
    say(initial_phrase)

    for item in items:
        say(item)

    final_phrase = initial_phrase.rstrip("!") + " Completed!" 
    say(final_phrase)