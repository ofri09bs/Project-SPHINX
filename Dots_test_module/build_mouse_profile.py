import subprocess
import time
import json
import statistics
from pynput import mouse
import mouse_analyzer

UI_SCRIPT = "dots_test_ui.py"  
GAME_DATA_FILE = "data\\dots_test_data.json"
PROFILE_FILE = "data\\dots_test_profile.json"
NUM_SESSIONS = 5

def build_profile():
    all_velocities = []
    all_accelerations = []
    all_angles = []
    sessions_time = []
    mouse_analyzer.clear_records()
    print(f"--- MOUSE TRAINING STARTED ({NUM_SESSIONS}s) ---")
    print("Please use your mouse normally (browse web, open files...)")

    for i in range(NUM_SESSIONS):
        start_time = time.time()
        print(f"\n[Round {i+1}/{NUM_SESSIONS}] Launching Game...")

        try:
            subprocess.run(['python',UI_SCRIPT],check=True)
        except Exception as e:
            print(f"Error running game: {e}")
            return
        
        end_time = time.time()
        
        try:
            with open(GAME_DATA_FILE,"r") as f:
                raw_game_data = json.load(f)
        except FileNotFoundError:
            print("Error: Game data not found.")
            return
        
        
        duration = end_time - start_time
        sessions_time.append(duration)
        
        analyzer_data = []
        for event in raw_game_data:
            if event["event"] == "move" or event["event"] == "click_hit":
                analyzer_data.append((event["x"], event["y"], event["time"]))

        mouse_analyzer.load_data_from_list(analyzer_data)

        data_len = len(mouse_analyzer.get_data())
        for j in range(2, data_len):
            res = mouse_analyzer.analyze_movement(j)
            
            if res:
                vel, ang, acc = res
                all_velocities.append(vel)
                all_angles.append(ang)
                all_accelerations.append(acc)
        
        print(f"  -> Processed {data_len} movement points.")
        time.sleep(1)

    if not all_velocities:
        print("Error: No movement data collected.")
        return

    end_time = time.time()

    print("\n--- CALCULATION ---")

    if len(sessions_time) > 1:
        avg_time = statistics.mean(sessions_time)
        std_time = statistics.stdev(sessions_time)
    else:
        avg_time = sessions_time[0] if sessions_time else 0
        std_time = 0

    profile = {
        "avg speed": statistics.mean(all_velocities),
        "std speed": statistics.stdev(all_velocities),
        "avg acceleration": statistics.mean(all_accelerations),
        "std acceleration": statistics.stdev(all_accelerations),
        "avg angle": statistics.mean(all_angles),
        "std angle": statistics.stdev(all_angles),
        "total_points": len(all_velocities),
        "avg time": avg_time,
        "std time": std_time
    }

    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=4)
        
    print(f"✅ New profile saved to {PROFILE_FILE}")
    print(f"   Avg Speed: {profile['avg speed']:.2f}")
    print(f"   Avg Accel: {profile['avg acceleration']:.2f}")

if __name__ == "__main__":
    build_profile()
            


    


                              
