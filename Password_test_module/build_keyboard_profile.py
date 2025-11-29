import json
from pynput.keyboard import Listener
import time
import keyboard_analyzer

TRAINING_TIME = 6

def build_profile():
    keyboard_analyzer.clear_data()
    print(f"--- KEYBOARD TRAINING STARTED ({TRAINING_TIME}s) ---")
    print("Please use your keyboard normally (browse web, open files...)")

    listener = Listener(on_press=keyboard_analyzer.on_press,on_release=keyboard_analyzer.on_release)
    listener.start()

    try:
        for i in range(TRAINING_TIME):
            print(f"Recording... {TRAINING_TIME - i}", end='\r')
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    listener.stop()

    keyboard_profile = keyboard_analyzer.analyze_typing()

    with open("my_keyboard_profile.json", "w") as f:
        json.dump(keyboard_profile, f, indent=4)

        
if __name__ == "__main__":
    build_profile()

    
    

    



    
