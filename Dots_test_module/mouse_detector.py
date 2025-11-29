import time
import json
import statistics
from pynput import mouse
import mouse_analyzer


def load_profile():
    with open('constellation_profile.json', "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def calc_z_score(std,mean,current):
    if std == 0:
        return 0
    
    z_score = abs(current-mean)/std
    return z_score

def main_tracker():

    listener = mouse.Listener(on_move=mouse_analyzer.record_movement)
    listener.start()
    profile = load_profile()

    profile_vel_mean = profile['avg speed']
    profile_acc_mean = profile['avg acceleration']
    profile_ang_mean = profile['avg angle']

    profile_vel_std = profile['std speed']
    profile_acc_std = profile['std acceleration']
    profile_ang_std = profile['std angle']

    while True:
        mouse_analyzer.clear_records()
        time.sleep(5)
        data = mouse_analyzer.get_data()

        if len(data)<10:
            continue

        velocities = []
        accelerations = []
        angels = []

        for i in range(2,len(data)):
            curr_movement = mouse_analyzer.analyze_movement(i)

            if curr_movement==None:
                continue

            vel = curr_movement[0]
            ang = curr_movement[1]
            acc = curr_movement[2]

            velocities.append(vel)
            angels.append(ang)
            accelerations.append(acc)

        if len(velocities) < 10 or len(accelerations) < 10 or len(angels) < 10:
            continue

        curr_vel_mean = statistics.mean(velocities)
        curr_acc_mean = statistics.mean(accelerations)
        curr_ang_mean = statistics.mean(angels)


        vel_z_score = calc_z_score(profile_vel_std,profile_vel_mean,curr_vel_mean)
        acc_z_score = calc_z_score(profile_acc_std,profile_acc_mean,curr_acc_mean)
        ang_z_score = calc_z_score(profile_ang_std,profile_ang_mean,curr_ang_mean)

        total_z_score = (vel_z_score * 0.4) + (acc_z_score * 0.4) + (ang_z_score * 0.2)


        if total_z_score<1.5:
            print("✅ User Verified")
        elif total_z_score>1.5:
            print(f"❌ Anomaly Detected! (Z-Score: {total_z_score}")


if __name__ == "__main__":
    main_tracker()



