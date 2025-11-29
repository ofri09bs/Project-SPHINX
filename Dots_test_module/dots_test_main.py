import json
import statistics
import subprocess
import sys
import mouse_analyzer
import time

UI_SCRIPT = "Dots_test_module\\dots_test_ui.py"
GAME_DATA_FILE = "data\\dots_test_data.json"
PROFILE_FILE = "data\\dots_test_profile.json"

W_TIME = 0.4  
W_SPEED = 0.2  
W_ACCEL = 0.3 
W_ANGLE = 0.1  

PASS_THRESHOLD = 1.5

def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[-] Error: {filename} not found.")
        exit()

def calc_z_score(std, mean, current):
    effective_std = max(std, 0.01)
    return abs(current - mean) / effective_std      


def start_test():
    profile = load_json(PROFILE_FILE)

    start_time = time.time()
    try:
        subprocess.run(['python',UI_SCRIPT],check=True)
    except Exception as e:
        print(f"Error running UI: {e}")
        return
    
    end_time = time.time()
    current_duration = end_time - start_time

    raw_data = load_json(GAME_DATA_FILE)

    analyzer_data = []
    for event in raw_data:
        if event["event"] == "move" or event["event"] == "click_hit":
            analyzer_data.append((event["x"], event["y"], event["time"]))

    mouse_analyzer.load_data_from_list(analyzer_data)

    velocities = []
    accelerations = []
    angles = []

    data_len = len(mouse_analyzer.get_data())
    for i in range(2,data_len):
        result = mouse_analyzer.analyze_movement(i)
        if result:
            velocities.append(result[0])
            angles.append(result[1])
            accelerations.append(result[2])

    if not velocities:
        print("❌ FAILED: Not enough movement data.")
        return
    
    curr_vel = statistics.mean(velocities)
    curr_acc = statistics.mean(accelerations)
    curr_ang = statistics.mean(angles)

    z_vel = calc_z_score(profile['std speed'], profile['avg speed'], curr_vel)
    z_acc = calc_z_score(profile['std acceleration'], profile['avg acceleration'], curr_acc)
    z_ang = calc_z_score(profile['std angle'], profile['avg angle'], curr_ang)
    z_time = calc_z_score(profile['std time'], profile['avg time'], current_duration)

    final_score = (z_vel * W_SPEED)+(z_acc * W_ACCEL)+(z_ang * W_ANGLE)+(z_time * W_TIME)

    print("\n[BIOMETRIC ANALYSIS REPORT]")
    print(f"Time Taken: {current_duration:.2f}s (Avg: {profile['avg time']:.2f}s) -> Z: {z_time:.2f}")
    print(f"Velocity Z: {z_vel:.2f}")
    print(f"Accel Z:    {z_acc:.2f}")
    print("-" * 30)
    print(f"FINAL THREAT SCORE: {final_score:.2f} (Threshold: {PASS_THRESHOLD})")

    if final_score < PASS_THRESHOLD:
        print("\n✅ ACCESS GRANTED")
        sys.exit(0)
        print("Welcome back, User.")
    else:
        print("\n❌ ACCESS DENIED")
        sys.exit(1)
        print("Biometric mismatch detected.")
        print("Initiating lockdown sequence...")

if __name__ == "__main__":
    start_test()