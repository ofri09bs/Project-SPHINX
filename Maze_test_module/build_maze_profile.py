import json
import statistics
import subprocess
import time
import os
import maze_analyzer

UI_SCRIPT = "Maze_test_module\\maze_test_ui.py"
GAME_DATA_FILE = "data\\maze_test_data.json"
PROFILE_FILE = "data\\maze_profile.json"
NUM_SESSIONS = 5

def build_profile():
    metrics = {
        "total_time": [],
        "avg_speed": [],
        "jitter": []
    }

    print(f"--- MAZE TRAINING ({NUM_SESSIONS} rounds) ---")
    print("Move the mouse smoothly from RED to GREEN without touching walls.")

    for i in range(NUM_SESSIONS):
        print(f"\n[Round {i+1}/{NUM_SESSIONS}] Launching Maze...")
        
        try:
            subprocess.run(["python", UI_SCRIPT], check=True)
            
            with open(GAME_DATA_FILE, "r") as f:
                raw_data = json.load(f)
            
            result = maze_analyzer.analyze_maze_path(raw_data)
            
            if result:
                metrics["total_time"].append(result["total_time"])
                metrics["avg_speed"].append(result["avg_speed"])
                metrics["jitter"].append(result["jitter"])
                print(f"  -> Jitter Score: {result['jitter']:.2f}")
            else:
                print("  -> Failed to analyze (did you finish the maze?)")

            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {e}")
            return

    print("\n--- CALCULATING STABILITY PROFILE ---")
    if not metrics["jitter"]:
        print("No valid data collected.")
        return

    final_profile = {}
    for key, values in metrics.items():
        final_profile[key] = {
            "mean": statistics.mean(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0.01
        }

    with open(PROFILE_FILE, "w") as f:
        json.dump(final_profile, f, indent=4)
        
    print(f"✅ Profile saved to {PROFILE_FILE}")
    print(f"   Avg Jitter: {final_profile['jitter']['mean']:.2f}")
    print(f"   Avg Time:   {final_profile['total_time']['mean']:.2f}s")

if __name__ == "__main__":
    build_profile()