from pynput.mouse import Controller
import math
import time

mouse = Controller()
mouse_records = []

def calc_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calc_velocity(distance, time_delta):
    if time_delta <= 0:
        return 0.0
    return distance / time_delta

def calc_acceleration(v1, v2, time_delta):
    if time_delta <= 0:
        return 0.0
    return (v2 - v1) / time_delta

def calc_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
    delta_x = x2 - x1
    delta_y = y2 - y1
    
    return math.atan2(delta_y, delta_x)


def record_movement(x=None, y=None):
    global mouse_records
    if x is None or y is None:
        x, y = mouse.position
    
    curr_time = time.time()
    mouse_records.append((x, y, curr_time))


def analyze_movement(i):
    global mouse_records

    if(len(mouse_records)<3):
        return None
    
    p_1 = mouse_records[i]
    p_2 = mouse_records[i-1]
    p_3 = mouse_records[i-2]

    pos1 = (p_1[0],p_1[1])
    pos2 = (p_2[0],p_2[1])
    pos3 = (p_3[0],p_3[1])
    delta_t_2 = p_1[2]-p_2[2]
    delta_t_1 = p_2[2]-p_3[2]

    dist_2 = calc_distance(pos1,pos2)
    dist_1 = calc_distance(pos3,pos2)
    velocity_2 = calc_velocity(dist_2,delta_t_2)
    velocity_1 = calc_velocity(dist_1,delta_t_1)
    acceleration = calc_acceleration(velocity_1,velocity_2,delta_t_1+delta_t_2)
    angle = calc_angle(pos1,pos2)

    if dist_1<2 or dist_2 <2:
        return None
    
    
    return abs(velocity_2),abs(angle),abs(acceleration)

def clear_records():
    global mouse_records
    mouse_records = []

def get_data():
    global mouse_records
    return mouse_records

def load_data_from_list(data_list):
    global mouse_records
    mouse_records = data_list
