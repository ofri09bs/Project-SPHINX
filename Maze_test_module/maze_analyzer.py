import math
import statistics

def calc_dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def calc_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def analyze_maze_path(raw_data):
    points = []
    
    for event in raw_data:
        if "x" in event:
            points.append((event["x"], event["y"], event["time"]))
            
    if len(points) < 5:
        return None 

    total_distance = 0
    total_angle_change = 0
    velocities = []
    
    for i in range(1, len(points)):
        p1 = points[i-1]
        p2 = points[i]
        
        dist = calc_dist(p1, p2)
        time_delta = p2[2] - p1[2]
        
        if time_delta > 0:
            velocities.append(dist / time_delta)
            
        total_distance += dist
        
        if i > 1:
            p0 = points[i-2]
            angle1 = calc_angle(p0, p1)
            angle2 = calc_angle(p1, p2)
            
            angle_diff = abs(angle2 - angle1)
            

            if angle_diff > math.pi:
                angle_diff = (2 * math.pi) - angle_diff
                
            total_angle_change += angle_diff


    
    total_time = points[-1][2] - points[0][2]
    
    avg_speed = statistics.mean(velocities) if velocities else 0
    

    jitter_score = 0
    if total_distance > 0:
        jitter_score = (total_angle_change / total_distance) * 1000 

    return {
        "total_time": total_time,
        "avg_speed": avg_speed,
        "jitter": jitter_score
    }