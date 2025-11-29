import json
from pynput.keyboard import Listener
import keyboard_analyzer
 
PRESS_WEIGHT = 1.0   
FLIGHT_WEIGHT = 3.0  
ANOMALY_THRESHOLD = 1.5

def load_profile():
    with open('my_keyboard_profile.json', "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def calc_z_score(std,mean,current):
    effective_std = max(std, 0.005)

    z_score = abs(current-mean)/effective_std
    return z_score

def main_tracker():
    my_profile = load_profile()
    keyboard_analyzer.clear_data()
    
    flight_scores = []
    press_scores = []

    listener = Listener(on_press=keyboard_analyzer.on_press,on_release=keyboard_analyzer.on_release)
    listener.start()
    password = input("Enter password:")
    if password!='hello world':
        print("Password Incorrect!")
        return
    listener.stop()

    user_profile = keyboard_analyzer.analyze_typing()

    for key in user_profile['press times stats']:

        if key in my_profile['press times stats']:
            mean = my_profile['press times stats'][key][0]
            std = my_profile['press times stats'][key][1]
            current_mean = user_profile['press times stats'][key][0]
            z_score = calc_z_score(std,mean,current_mean)
            press_scores.append(z_score)
            

    for key in user_profile['flight times stats']:

        if key in my_profile['flight times stats']:
            mean = my_profile['flight times stats'][key][0]
            std = my_profile['flight times stats'][key][1]
            current_mean = user_profile['flight times stats'][key][0]
            z_score = calc_z_score(std,mean,current_mean)
            flight_scores.append(z_score)

    if not press_scores and not flight_scores:
        print("[-] Not enough data.")
        return

    bad_flights = sum(1 for s in flight_scores if s > ANOMALY_THRESHOLD)
    bad_presses = sum(1 for s in press_scores if s > ANOMALY_THRESHOLD)

    total_penalty = (bad_presses * PRESS_WEIGHT) + (bad_flights * FLIGHT_WEIGHT)
    max_possible_penalty = (len(press_scores) * PRESS_WEIGHT) + (len(flight_scores) * FLIGHT_WEIGHT)

    if max_possible_penalty == 0: 
        violation_ratio = 0
    else:
        violation_ratio = total_penalty / max_possible_penalty
    

    print(f"---------------------------------")
    print(f"Bad Dwells:  {bad_presses} (x{PRESS_WEIGHT})")
    print(f"Bad Flights: {bad_flights} (x{FLIGHT_WEIGHT})")
    print(f"Weighted Violation Ratio: {violation_ratio*100:.1f}%")
    print(f"---------------------------------")

    MAX_ALLOWED_VIOLATION = 0.30

    if violation_ratio < MAX_ALLOWED_VIOLATION:
        print("✅ IDENTITY VERIFIED")
    else:
        print("❌ ACCESS DENIED (Too many anomalies)")


if __name__ == "__main__":
    main_tracker()



