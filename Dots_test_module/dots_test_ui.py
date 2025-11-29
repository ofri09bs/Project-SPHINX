import tkinter as tk
import time
import math
import json

DOT_RADIUS = 15
DOT_COLOR = "#00ffcc"
BG_COLOR = "black"
NUM_DOTS = 5
SAMPLE_RATE = 0.03

FIXED_PATTERN_RATIOS = [
    (0.3, 0.1), 
    (0.9, 0.4),     
    (0.4, 0.6), 
    (0.1, 0.7), 
    (0.8, 0.8) 
]

root = None
canvas = None
start_label = None
last_sample_time = 0

targets = []      
current_target = 0 
raw_path = []     
is_running = False

def generate_targets():
    global targets
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    
    targets = []
    for rx, ry in FIXED_PATTERN_RATIOS:
        x = int(width * rx)
        y = int(height * ry)
        targets.append((x, y))

def show_next_target():
    global current_target
    
    canvas.delete("target") 
    
    if current_target < len(targets):
        x, y = targets[current_target]
        
        x1, y1 = x - DOT_RADIUS, y - DOT_RADIUS
        x2, y2 = x + DOT_RADIUS, y + DOT_RADIUS
        canvas.create_oval(x1, y1, x2, y2, fill=DOT_COLOR, outline="white", tags="target")
        
        raw_path.append({
            "event": "target_appeared",
            "target_x": x,
            "target_y": y,
            "time": time.time()
        })
    else:
        finish_test()

def start_test(event=None):
    global is_running
    
    if is_running: return

    if start_label:
        start_label.destroy()
        
    is_running = True
    raw_path = []
    generate_targets()

    
    raw_path.append({"event": "start", "time": time.time()})
    
    show_next_target()

def on_click(event):
    global current_target
    
    if not is_running:
        start_test()
        return

    target_x, target_y = targets[current_target]
    distance = math.sqrt((event.x - target_x)**2 + (event.y - target_y)**2)
    
    if distance <= DOT_RADIUS + 5: 
        raw_path.append({
            "event": "click_hit",
            "x": event.x,
            "y": event.y,
            "time": time.time()
        })
        current_target += 1
        show_next_target()
    else:
        raw_path.append({
            "event": "click_miss",
            "x": event.x,
            "y": event.y,
            "time": time.time()
        })

def on_move(event):
    global last_sample_time
    
    if is_running:
        current_time = time.time()
        
        if current_time - last_sample_time > SAMPLE_RATE:
            raw_path.append({
                "event": "move",
                "x": event.x,
                "y": event.y,
                "time": current_time
            })
            last_sample_time = current_time

def finish_test():
    global is_running
    is_running = False
    canvas.delete("all")
    
    lbl = tk.Label(root, text="PATTERN COMPLETE.\nSaving Profile...", 
                   font=("Courier", 30), bg=BG_COLOR, fg="#00ff00")
    lbl.place(relx=0.5, rely=0.5, anchor="center")
    
    with open("data\\dots_test_data.json", "w") as f:
        json.dump(raw_path, f, indent=4)
        
    print(f"[V] Saved {len(raw_path)} data points (optimized).")
    
    root.after(2000, root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg=BG_COLOR)
    
    canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    
    start_label = tk.Label(root, text="CLICK TO START SEQUENCE", 
                           font=("Courier", 30), bg=BG_COLOR, fg="white")
    start_label.place(relx=0.5, rely=0.5, anchor="center")
    
    root.bind('<Button-1>', on_click)
    root.bind('<Motion>', on_move)
    root.bind('<Escape>', lambda e: root.destroy())
    
    root.mainloop()