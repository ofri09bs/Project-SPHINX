import sys
import tkinter as tk
from tkinter import messagebox
import json
import statistics
import time
from pynput import keyboard
import keyboard_analyzer

PROFILE_FILE = 'data\\my_keyboard_profile.json'
TARGET_PASSWORD = "hello world"
PASS_THRESHOLD = 1.5 
BG_COLOR = "#121212" 
ERROR_COLOR = "#550000" 

FLIGHT_WEIGHT = 0.67
PRESS_WEIGHT = 0.33

root = None
entry = None
lbl_status = None
btn_verify = None
profile_data = None
listener = None

def load_profile():
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def calc_z_score(std, mean, current):
    effective_std = max(std, 0.005)
    return abs(current - mean) / effective_std

def flash_screen():
    original_bg = root.cget("bg")
    
    for _ in range(3):
        root.configure(bg=ERROR_COLOR)
        root.update()
        time.sleep(0.1)
        root.configure(bg=original_bg)
        root.update()
        time.sleep(0.1)


def reset_test():
    entry.delete(0, tk.END)
    keyboard_analyzer.clear_data()
    lbl_status.config(text="Try again...", fg="orange")


def check_login(event=None):
    user_input = entry.get()
    
    if user_input != TARGET_PASSWORD:
        lbl_status.config(text="❌ WRONG PASSWORD", fg="#ff3333")
        flash_screen()
        reset_test()
        return

    print("Analyzing biometrics...")
    user_stats = keyboard_analyzer.analyze_typing()
    press_z_scores = []
    flight_z_scores = []

    for key in user_stats['press times stats']:
        if key in profile_data['press times stats']:
            p_mean = profile_data['press times stats'][key][0]
            p_std = profile_data['press times stats'][key][1]
            curr = user_stats['press times stats'][key][0]
            press_z_scores.append(calc_z_score(p_std, p_mean, curr))

    for key in user_stats['flight times stats']:
        if key in profile_data['flight times stats']:
            p_mean = profile_data['flight times stats'][key][0]
            p_std = profile_data['flight times stats'][key][1]
            curr = user_stats['flight times stats'][key][0]
            flight_z_scores.append(calc_z_score(p_std, p_mean, curr))

    if not press_z_scores:
        lbl_status.config(text="⚠️ NOT ENOUGH DATA", fg="orange")
        reset_test()
        return

    avg_press_score = statistics.mean(press_z_scores)
    avg_flight_score = statistics.mean(flight_z_scores)

    final_score = (avg_press_score * PRESS_WEIGHT)+(avg_flight_score*FLIGHT_WEIGHT)

    if final_score < PASS_THRESHOLD:
        lbl_status.config(text=f"✅ ACCESS GRANTED (Score: {final_score:.2f})", fg="#00ff00")
        entry.config(state="disabled")
        btn_verify.config(bg="#00aa00", text="UNLOCKED", state="disabled")
        root.after(2000, root.destroy)
        sys.exit(0)
    else:
        lbl_status.config(text=f"❌ BIOMETRIC MISMATCH (Score: {final_score:.2f})", fg="#ff3333")
        flash_screen()
        reset_test()
        sys.exit(1)


def main():
    global root, entry, lbl_status, btn_verify, profile_data, listener
    
    profile_data = load_profile()
    if not profile_data:
        print("Error: Profile not found.")
        return

    keyboard_analyzer.clear_data()
    listener = keyboard.Listener(
        on_press=keyboard_analyzer.on_press,
        on_release=keyboard_analyzer.on_release
    )
    listener.start()

    root = tk.Tk()
    root.title("Security Check")
    root.attributes('-fullscreen', True)
    root.geometry("500x350")
    root.configure(bg="#121212")
    root.resizable(False, False)

    tk.Label(root, text="SECURITY CHECKPOINT", font=("Consolas", 24, "bold"), bg="#121212", fg="#00ffcc").pack(pady=(40, 10))
    tk.Label(root, text=f"Type: '{TARGET_PASSWORD}'", font=("Arial", 12), bg="#121212", fg="#aaaaaa").pack(pady=10)

    entry = tk.Entry(root, font=("Consolas", 20), justify="center", bg="#333333", fg="white", insertbackground="white")
    entry.pack(pady=10, ipady=5)
    entry.focus_set()

    btn_verify = tk.Button(root, text="VERIFY IDENTITY", font=("Arial", 12, "bold"), bg="#0055ff", fg="white", 
                           command=check_login, height=2, width=20)
    btn_verify.pack(pady=20)

    lbl_status = tk.Label(root, text="Waiting for input...", font=("Arial", 10), bg="#121212", fg="#666666")
    lbl_status.pack(side="bottom", pady=10)

    root.bind('<Return>', check_login)

    root.mainloop()
    
    listener.stop()

if __name__ == "__main__":
    main()