import numpy as np
import cv2 as cv
from config import Config
from collections import deque

class DataProcessor:
    def __init__(self):
        
        print("Starting Data Initialization...")

        smooth_frames = max(1, int(1.0 / Config.SMOOTHING))
        #Redone smoothing with deque for better performance
        self.mouth_history = deque(maxlen=smooth_frames)
        self.eye_left_history = deque(maxlen=smooth_frames)
        self.eye_right_history = deque(maxlen=smooth_frames)
        self.head_x_history = deque(maxlen=smooth_frames)
        self.head_y_history = deque(maxlen=smooth_frames)
        self.happy_history = deque(maxlen=smooth_frames)
        
        print("Data Initialization Complete.")

    def extract_features(self, landmarks):
        if landmarks is None:
            return None
        
        #Mouth open
        mouth_open_raw = abs(landmarks[14].y - landmarks[13].y)
        mouth_open = mouth_open_raw * Config.MOUTH_MULTIPLIER
        mouth_open = np.clip(mouth_open, 0.0, 1.0) # Clip value between 0 and 1 so close and open
        #Left eye blink
        eye_left_raw = abs(landmarks[159].y - landmarks[145].y)
        eye_left = 1.0 - (eye_left_raw * Config.EYE_MULTIPLIER)
        eye_left = np.clip(eye_left, 0.0, 1.0)
        #Rihqt eye blink
        eye_right_raw = abs(landmarks[386].y - landmarks[374].y)
        eye_right = 1.0 - (eye_right_raw * Config.EYE_MULTIPLIER)
        eye_right = np.clip(eye_right, 0.0, 1.0)

        # Happy based on mouth corner vertical position relative to upper lip
        corner_avg_y = (landmarks[61].y + landmarks[291].y) * 0.5
        upper_lip_y = landmarks[13].y
        corner_delta = upper_lip_y - corner_avg_y
        happy = np.clip(corner_delta * Config.HAPPY_MULTIPLIER, 0.0, 1.0)

        #Head movement 
        head_x = (landmarks[1].x - 0.5) * 2
        head_y = (landmarks[1].y - 0.5) * -2

        return {
            'mouth_open': float(mouth_open),
            'eye_left': float(eye_left),
            'eye_right': float(eye_right),
            'head_x': float(head_x),
            'head_y': float(head_y),
            'happy': float(happy)
        }
    
    def smooth_data(self, data):
        if data is None:
            return None
        
        self.mouth_history.append(data['mouth_open'])
        self.eye_left_history.append(data['eye_left'])
        self.eye_right_history.append(data['eye_right'])
        self.head_x_history.append(data['head_x'])
        self.head_y_history.append(data['head_y'])
        self.happy_history.append(data['happy'])

        return {
            'mouth_open': float(np.mean(self.mouth_history)),
            'eye_left': float(np.mean(self.eye_left_history)),
            'eye_right': float(np.mean(self.eye_right_history)),
            'head_x': float(np.mean(self.head_x_history)),
            'head_y': float(np.mean(self.head_y_history)),
            'happy': float(np.mean(self.happy_history))
        }
        

