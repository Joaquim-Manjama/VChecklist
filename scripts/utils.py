import json
import keyboard
import os
import pyttsx3
import queue
import speech_recognition as sr
import threading
import time

# CONSTANTS
# Base file path of checklists .json files
CHECKLISTS_PATH = "checklists/"

# Base file path of other files
BASE_PATH = "files/"

# Program title
title = "        ********    Welcome to VCHECKlIST    ********"

# Colors to be used in the terminal
class bcolors:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# TERMINAL
# Color the text
def color(text, color):
    match color:
        case "GREEN":
            return f"{bcolors.OKGREEN}{text}{bcolors.ENDC}"
        case "CYAN":
            return f"{bcolors.OKCYAN}{text}{bcolors.ENDC}"
        case "YELLOW":
            return f"{bcolors.WARNING}{text}{bcolors.ENDC}"
        case "RED":
            return f"{bcolors.FAIL}{text}{bcolors.ENDC}"
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

# Load microphone shortcut
def load_shortcut():
    with open(f"{BASE_PATH}mic_shortcut.txt", "r") as file:
        data = file.readline()

    return data

# Save microphone shortcut
def save_shortcut():
    while True:
        clear()
        print("  ****  Microphone Shortcut  ****")
        print("Press your new shortcut ('Esc' to finish): ")
        recorded = keyboard.record(until='esc')
        key_presses = process_input(recorded)
        op = input(f"Confirm '{key_presses}' as new shortcut? (y/n): ")

        if op.lower() == "y" or op.lower() == "yes" :
            file = open(F"{BASE_PATH}mic_shortcut.txt", "w")
            file.write(key_presses)
            file.close()
            break

# Process user key presses
def process_input(record=[]):
    key_presses = ""
    length = len(record)

    if length == 0:
        print("No key presses detected!")
        return
    
    for i in range(length):
        key = str(record[i])

        if not " up)" in key and not "esc" in key:
            key_presses += str(record[i])
            key_presses += "+"

    key_presses = key_presses.rstrip("+").replace("KeyboardEvent", "").replace("(", "").replace(" down", "").replace(")", "")
    return key_presses.upper()

# TTS
# Transform text into speech
def say(item):
    time.sleep(1)
    engine = pyttsx3.init()
    engine.say(item)
    engine.runAndWait()
    engine.stop()


# STT
# Listen to microphone
def listen():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            text = text.lower()
            print(text)
            return text 
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return "error"
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "error"
    except KeyboardInterrupt:
        print("Program terminated by user")
        return "error"

# CHECKLIST
# Go through all checklist items for a specific flight phase
def run_checklist(aircraft, phase):
    clear()
    file_path = f"{CHECKLISTS_PATH}{aircraft}.json"
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

    for file in os.listdir(CHECKLISTS_PATH):

        if file != "template.json" and file.endswith(".json"):
            checklists.append(file.rstrip(".json"))

    checklists.sort()

    return checklists

# Get Checklists phases
def get_checklist_phases(aircacft):
    file_path = f"{CHECKLISTS_PATH}{aircacft}.json"
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

def get_input():
    shortcut = load_shortcut().lower()
    input_result = [None]
    result_queue = queue.Queue()
    
    # Handle voice input
    def voice_handler():
        result = listen()
        if result:
            result_queue.put(('voice', result))

    # Thread to handle keyboard input
    def keyboard_input_thread():
        while True:
            try:
                user_input = input(": ")
                if user_input.strip():
                    result_queue.put(('keyboard', int(user_input)))
                    break
            except ValueError:
                print("Invalid Entry!")
            except:
                break    
        
    keyboard.add_hotkey(shortcut, voice_handler)
    
    # Start keyboard input thread
    input_thread = threading.Thread(target=keyboard_input_thread, daemon=True)
    input_thread.start()
    
    # Wait for either voice or keyboard input
    while True:
        try:
            source, value = result_queue.get(timeout=0.1)
            input_result[0] = value
            break
        except queue.Empty:
            continue
        except KeyboardInterrupt:
            keyboard.unhook_all()
            raise
    
    keyboard.unhook_all()
    return input_result[0]