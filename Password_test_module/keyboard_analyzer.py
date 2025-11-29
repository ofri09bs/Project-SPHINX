from pynput.keyboard import Listener
import time
import statistics

press_times = {}
flight_times = {}
active_keys = {}
last_key_time = None
last_key_char = None

def get_key_name(key):
    try:
        return key.char
    except:
        return str(key)

def on_press(key):
    global last_key_time, last_key_char,active_keys,flight_times
    key_name = get_key_name(key)
    current_time = time.time()

    if last_key_time is not None and last_key_time > 0:

        flight_time = current_time - last_key_time
    
        if 0<flight_time<3:

            dict_key = last_key_char + '->' + key_name
            if dict_key in flight_times:
                flight_times[dict_key].append(flight_time)
            else:
                flight_times[dict_key] = [flight_time]

        else:
            last_key_time = None

    active_keys[key_name] = current_time



def on_release(key):
    global last_key_time, last_key_char,active_keys,press_times
    current_time = time.time()
    key_name = get_key_name(key)

    if key_name in active_keys:
        start_time = active_keys[key_name]
        press_time = current_time-start_time

        if key_name in press_times:
            press_times[key_name].append(press_time)
        else:
            press_times[key_name] = [press_time]

        del active_keys[key_name]

    last_key_time = current_time
    last_key_char = key_name


def clear_data():
    global last_key_time, last_key_char,active_keys,flight_times,press_times
    press_times = {}
    flight_times = {}
    active_keys = {}
    last_key_char = None
    last_key_time = None


def get_press_times():
    return press_times

def get_flight_times():
    return flight_times

def analyze_typing():
    global press_times,flight_times
    press_times_stats = {}
    flight_times_stats = {}
    times_list = []

    for key in press_times:

        for time_var in press_times[key]:
            times_list.append(time_var)

        if len(press_times[key])>1:
            avg_time = statistics.mean(times_list)
            std = statistics.stdev(times_list)
        else:
            avg_time = press_times[key][0]
            std = 0.001

        press_times_stats[key] = [avg_time,std]

    times_list = []

    for key in flight_times:
        
        for time_var in flight_times[key]:
            times_list.append(time_var)

        if len(flight_times[key])>1:
            avg_time = statistics.mean(times_list)
            std = statistics.stdev(times_list)
        else:
            avg_time = flight_times[key][0]
            std = 0.001

        flight_times_stats[key] = [avg_time,std]

    keyboard_profile = {"press times stats":press_times_stats,"flight times stats":flight_times_stats}

    return keyboard_profile
