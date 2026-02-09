from scripts.utils import load_shortcut, listen
import threading

# At the top of your script, create a global listener
import keyboard
import queue

voice_input_queue = queue.Queue()
listener_active = True

def setup_global_voice_listener():
    """Call this once at program startup"""
    shortcut = load_shortcut().lower()
    
    def global_voice_handler():
        if listener_active:
            result = listen()
            if result:
                voice_input_queue.put(result)
    
    keyboard.add_hotkey(shortcut, global_voice_handler)

# Modified get_input that uses the global listener
def get_input():
    
    input_result = [None]
    result_queue = queue.Queue()
    
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
    
    # Start keyboard input thread
    input_thread = threading.Thread(target=keyboard_input_thread, daemon=True)
    input_thread.start()
    
    # Wait for either voice or keyboard input
    while True:
        # Check voice queue first
        try:
            voice_result = voice_input_queue.get_nowait()
            input_result[0] = voice_result
            break
        except queue.Empty:
            pass
        
        # Then check keyboard queue
        try:
            source, value = result_queue.get(timeout=0.1)
            input_result[0] = value
            break
        except queue.Empty:
            continue
        except KeyboardInterrupt:
            raise
    
    return input_result[0]

# In your main function:
if __name__ == "__main__":
    setup_global_voice_listener()
    value = get_input()
    print(value)  
    # Set up once
    keyboard.unhook_all()  # Unhook any existing hotkeys to avoid conflicts
    # ... rest of your program