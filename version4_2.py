import cv2
import os
import mediapipe as mp
import math
import numpy as np
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
width_cam, height_cam = 640, 480
cap.set(3, width_cam)
cap.set(4, height_cam)
left_point = (100, height_cam // 2)  
right_point = (width_cam - 100, height_cam // 2)  
touch_threshold = 100
cooldown_time = 2
last_action_time = {'previous' :0, 'next' :0}
volume = 50 
os.system(f"osascript -e 'set volume output volume {volume}'")
previous_angle = None  
total_angle_change = 0  
angle_threshold = 5  
rotation_per_volume_change = 10 
smoothing_factor = 0.3  
smoothed_angle_change = 0  
def calculate_angle(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))
def control_music(action):
    if action == 'previous':
        os.system("osascript -e 'tell application \"Spotify\" to previous track'")  
    elif action == 'next':
        os.system("osascript -e 'tell application \"Spotify\" to next track'")  
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    left_radius = 30  
    right_radius = 30  
    overlay = frame.copy()
    cv2.circle(overlay, left_point, left_radius, (0, 255, 0, 127), -1)
    cv2.circle(overlay, right_point, right_radius, (0, 0, 255, 127), -1)  
    cv2.addWeighted(overlay, 0.5, frame, 1 - 0.5, 0, frame)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        wrist_x, wrist_y = int(wrist.x * width_cam), int(wrist.y * height_cam)
        index_tip_x, index_tip_y = int(index_tip.x * width_cam), int(index_tip.y * height_cam)
        distance = calculate_distance(wrist_x, wrist_y, index_tip_x, index_tip_y)
        current_angle = calculate_angle(wrist_x, wrist_y, index_tip_x, index_tip_y)
        if previous_angle is not None:
            angle_difference = current_angle - previous_angle

            if angle_difference > 180:
                angle_difference -= 360
            elif angle_difference < -180:
                angle_difference += 360

            smoothed_angle_change = smoothing_factor * angle_difference + (1 - smoothing_factor) * smoothed_angle_change

            total_angle_change += smoothed_angle_change

            if abs(total_angle_change) > angle_threshold:
                volume_change = total_angle_change / rotation_per_volume_change 
                volume += int(volume_change)  
                volume = max(0, min(100, volume))  


                total_angle_change = 0


        previous_angle = current_angle


        volume_height = int(height_cam * (volume / 100))  
        cv2.rectangle(frame, (10, height_cam - volume_height), (50, height_cam), (0, 255, 0), -1)
        cv2.putText(frame, f"Volume: {volume}%", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.circle(frame, (index_tip_x, index_tip_y), 10, (0, 255, 255), -1)  
        cv2.circle(frame, (wrist_x, wrist_y), 10, (255, 0, 0), -1)  
        left_distance = calculate_distance(index_tip_x, index_tip_y, left_point[0], left_point[1])
        right_distance = calculate_distance(index_tip_x, index_tip_y, right_point[0], right_point[1])
        song_triggered = {'next': False, 'previous': False}

        if left_distance < touch_threshold and not song_triggered['previous']:
            current_time = time.time()
            if current_time - last_action_time['previous'] >= cooldown_time:
                print("Previous task triggered")
                control_music('previous')
                song_triggered['previous'] = True
                last_action_time['previous'] = current_time 

        elif right_distance < touch_threshold and not song_triggered['next']:
            current_time = time.time()
            
            if current_time - last_action_time['next'] >= cooldown_time:
                control_music('next')                     
                song_triggered['next'] = True
                print("Next task triggered")
                last_action_time['next'] = current_time

        if left_distance > touch_threshold and right_distance > touch_threshold:
            song_triggered['previous'] = False
            song_triggered['next'] = False    

    if not results.multi_hand_landmarks:
        os.system(f"osascript -e 'set volume output volume {volume}'")

    cv2.imshow("Volume Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
