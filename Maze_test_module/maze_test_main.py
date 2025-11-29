import json
import subprocess
import time
import sys
import maze_analyzer  

UI_SCRIPT = "Maze_test_module\\maze_test_ui.py"
GAME_DATA_FILE = "data\\maze_test_data.json"
PROFILE_FILE = "data\\maze_profile.json"

W_JITTER = 0.6  
W_SPEED = 0.2   
W_TIME = 0.2    

PASS_THRESHOLD = 1.5

def load_json(filename):
    try:
        with open(filename, "r") as f: return json.load(f)
    except FileNotFoundError:
        print(f"[-] Error: {filename} not found. Run training first.")
        exit()

def calc_z_score(std, mean, current):
    effective_std = max(std, 0.01)
    return abs(current - mean) / effective_std

def start_test():
    print("--- MAZE CHALLENGE ---")
    
    profile = load_json(PROFILE_FILE)
    print("[V] Biometric Profile Loaded.")

    print("Launching Maze Interface...")
    try:
        subprocess.run(["python", UI_SCRIPT], check=True)
    except Exception as e:
        print(f"Error running UI: {e}")
        return

    try:
        raw_data = load_json(GAME_DATA_FILE)
    except:
        print("[-] No data found. Did you finish the maze?")
        return

    print("Analyzing Motor Skills...")
    
    current_metrics = maze_analyzer.analyze_maze_path(raw_data)
    
    if not current_metrics:
        print("❌ FAILED: Invalid data.")
        return

    curr_jitter = current_metrics["jitter"]
    curr_speed = current_metrics["avg_speed"]
    curr_time = current_metrics["total_time"]

    # Jitter
    z_jitter = calc_z_score(profile["jitter"]["std"], 
                            profile["jitter"]["mean"], 
                            curr_jitter)
    
    # Speed
    z_speed = calc_z_score(profile["avg_speed"]["std"], 
                           profile["avg_speed"]["mean"], 
                           curr_speed)
    
    # Time
    z_time = calc_z_score(profile["total_time"]["std"], 
                          profile["total_time"]["mean"], 
                          curr_time)

    final_score = (z_jitter * W_JITTER) + (z_speed * W_SPEED) + (z_time * W_TIME)

    print("\n" + "="*30)
    print("MAZE BIOMETRIC REPORT")
    print("="*30)
    print(f"Jitter Z-Score: {z_jitter:.2f} (Weight: {W_JITTER})")
    print(f"Speed Z-Score:  {z_speed:.2f} (Weight: {W_SPEED})")
    print(f"Time Z-Score:   {z_time:.2f} (Weight: {W_TIME})")
    print("-" * 20)
    print(f"FINAL THREAT SCORE: {final_score:.2f}")
    print("="*30)

    if final_score < PASS_THRESHOLD:
        print("\n✅ ACCESS GRANTED")
        sys.exit(0)
        print("Motor skills verified.")
    else:
        print("\n❌ ACCESS DENIED")
        sys.exit(1)
        print("Movement does not match user profile.")

if __name__ == "__main__":
    start_test()