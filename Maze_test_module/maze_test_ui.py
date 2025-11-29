import tkinter as tk
import time
import json
import math

BG_COLOR = "black"
WALL_COLOR = "white"
PATH_COLOR = "black"
START_COLOR = "red"
END_COLOR = "#00ff00"
PATH_WIDTH = 40

SAMPLE_RATE = 0.03 

root = None
canvas = None
is_running = False
raw_path = []
start_rect = None
end_rect = None
walls = []
last_sample_time = 0 

def build_maze():
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    
    canvas.delete("all")
    walls.clear()
    
    bg = canvas.create_rectangle(0, 0, width, height, fill=WALL_COLOR, outline="")
    
    path1 = (100, 200, width - 300, 200 + PATH_WIDTH)
    canvas.create_rectangle(*path1, fill=PATH_COLOR, outline="", tags="path")
    
    path2 = (width - 300, 200, width - 300 + PATH_WIDTH, 600)
    canvas.create_rectangle(*path2, fill=PATH_COLOR, outline="", tags="path")
    
    path3 = (200, 600, width - 300 + PATH_WIDTH, 600 + PATH_WIDTH)
    canvas.create_rectangle(*path3, fill=PATH_COLOR, outline="", tags="path")
    
    global start_rect, end_rect
    start_rect = canvas.create_rectangle(100, 200, 150, 200 + PATH_WIDTH, fill=START_COLOR, outline="")
    end_rect = canvas.create_rectangle(200, 600, 250, 600 + PATH_WIDTH, fill=END_COLOR, outline="")
    
    canvas.create_text(width//2, 100, text="MOVE MOUSE TO RED ZONE TO START AND DRAG HIM TO THE GREEN ZONE\nWITHOUT TOUCHING THE WALLS", 
                       font=("Courier", 20, "bold"), fill="black")

def check_collision(x, y):
    items = canvas.find_overlapping(x, y, x+1, y+1)
    
    is_safe = False
    for item in items:
        tags = canvas.gettags(item)
        if "path" in tags or item == start_rect or item == end_rect:
            is_safe = True
            break
            
    return not is_safe 

def on_move(event):
    global is_running, raw_path, last_sample_time
    x, y = event.x, event.y
    current_time = time.time()
    
    if not is_running:
        coords = canvas.coords(start_rect)
        if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
            is_running = True
            raw_path = []
            last_sample_time = current_time
            print("--- MAZE STARTED ---")
            canvas.delete("all") 
            build_maze()
            return

    if is_running:
        
        if check_collision(x, y):
            fail_test()
            return

        coords = canvas.coords(end_rect)
        if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
            finish_test()
            return

        if current_time - last_sample_time > SAMPLE_RATE:
            raw_path.append({"x": x, "y": y, "time": current_time})
            last_sample_time = current_time

def fail_test():
    global is_running
    is_running = False
    print("FAILED! Touched the wall.")
    
    canvas.create_rectangle(0,0, root.winfo_screenwidth(), root.winfo_screenheight(), fill="red")
    root.update()
    time.sleep(0.5)
    
    build_maze()

def finish_test():
    global is_running
    is_running = False
    
    lbl = tk.Label(root, text="MAZE COMPLETE.\nSaving Data...", 
                   font=("Courier", 30), bg=BG_COLOR, fg="#00ff00")
    lbl.place(relx=0.5, rely=0.5, anchor="center")
    
    with open("data\\maze_test_data.json", "w") as f:
        json.dump(raw_path, f, indent=4)
        
    print(f"[V] Saved {len(raw_path)} points (Optimized).")
    root.after(2000, root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    
    canvas = tk.Canvas(root, bg="white", highlightthickness=0)
    canvas.pack(fill='both', expand=True)
    
    build_maze()
    
    root.bind('<Motion>', on_move)
    root.bind('<Escape>', lambda e: root.destroy())
    
    root.mainloop()