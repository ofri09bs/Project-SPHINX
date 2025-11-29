import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import time
import threading

STAGES = [
    {
        "name": "Phase 1: The Constellation",
        "desc": "Mouse Response & Path Efficiency",
        "script": "Dots_test_module\\dots_test_main.py"
    },
    {
        "name": "Phase 2: The Mantra",
        "desc": "Keystroke Dynamics & Rhythm",
        "script": "Password_test_module\\password_test_ui.py"
    },
    {
        "name": "Phase 3: The Labyrinth",
        "desc": "Fine Motor Skills & Stability",
        "script": "Maze_test_module\\maze_test_main.py"
    }
]

BG_COLOR = "#050505"
TEXT_COLOR = "#00ffcc"
FAIL_COLOR = "#ff3333"

root = None
lbl_stage = None
lbl_desc = None
btn_action = None

def update_status(text, color):
    lbl_stage.config(text=text, fg=color)
    root.update()

def fail_sequence(failed_stage_name):
    update_status("❌ ACCESS DENIED", FAIL_COLOR)
    lbl_desc.config(text=f"Biometric mismatch detected during {failed_stage_name}.")
    
    btn_action.config(text="SYSTEM LOCKED", bg="red", state="disabled")
    
    for _ in range(5):
        root.configure(bg="#330000")
        root.update()
        time.sleep(0.1)
        root.configure(bg="black")
        root.update()
        time.sleep(0.1)

def success_sequence():
    update_status("✅ IDENTITY CONFIRMED", "#00ff00")
    lbl_desc.config(text="Welcome back, Administrator.")
    
    btn_action.config(text="UNLOCKING...", bg="#00ff00")
    root.update()
    time.sleep(2)
    
    root.destroy()
    sys.exit(0)

def run_stages():
    
    for stage in STAGES:
        stage_name = stage["name"]
        script_file = stage["script"]
        
        lbl_desc.config(text=stage["desc"])
        update_status(f"LOADING {stage_name}...", "cyan")
        time.sleep(1.5) 
        
        update_status(f"RUNNING: {stage_name}", "white")
        
        try:
            process = subprocess.run(
                ["python", script_file], 
                capture_output=False, 
                check=False 
            )
            
            exit_code = process.returncode
            
            if exit_code == 0:
                update_status(f"✅ {stage_name}: PASSED", "#00ff00")
                time.sleep(1)
            else:
                fail_sequence(stage_name)
                return 

        except Exception as e:
            update_status(f"SYSTEM ERROR: {e}", "red")
            return

    success_sequence()

def start_sequence():
    btn_action.config(state="disabled")
    threading.Thread(target=run_stages, daemon=True).start()

def main():
    global root, lbl_stage, lbl_desc, btn_action
    
    root = tk.Tk()
    root.title("PROJECT SPHINX")
    root.attributes('-fullscreen', True)
    root.configure(bg=BG_COLOR)
    
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(frame, text="PROJECT SPHINX", font=("Impact", 70), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)
    tk.Label(frame, text="MULTI-FACTOR BIOMETRIC AUTHENTICATION", font=("Consolas", 16, "bold"), bg=BG_COLOR, fg="white").pack(pady=(0, 40))

    lbl_stage = tk.Label(frame, text="INITIALIZING...", font=("Courier", 24, "bold"), bg=BG_COLOR, fg="yellow")
    lbl_stage.pack(pady=20)
    
    lbl_desc = tk.Label(frame, text="", font=("Arial", 14), bg=BG_COLOR, fg="#888888")
    lbl_desc.pack(pady=5)

    btn_action = tk.Button(frame, text="BEGIN AUTHENTICATION", font=("Arial", 16, "bold"), bg="#0044cc", fg="white",
                           command=start_sequence, width=25, height=2)
    btn_action.pack(pady=40)

    root.bind('<Escape>', lambda e: sys.exit())

    root.mainloop()

if __name__ == "__main__":
    main()