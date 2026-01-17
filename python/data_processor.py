import numpy as np
import cv2 as cv
from config import Config
from collections import deque

class DataProcessor:
    def __init__(self):
        
        print("Starting Data Initialization...")

        self.mouth_history = deque(maxlen=Config.SMOOTHING)
        #we save only 5 last values for smoothing
        #A deque stands for Double-Ended Queue. It is a special type of data structure that allows you to add and remove elements from both ends efficiently
        self.eye_left_history = deque(maxlen=Config.SMOOTHING)
        self.eye_right_history = deque(maxlen=Config.SMOOTHING)
        self.head_x_history = deque(maxlen=Config.SMOOTHING)
        self.head_y_history = deque(maxlen=Config.SMOOTHING)
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
        eye_left = eye_left_raw * Config.EYE_MULTIPLIER
        eye_left = np.clip(eye_left, 0.0, 1.0)
        #Rihqt eye blink
        eye_right_raw = abs(landmarks[386].y - landmarks[374].y)
        eye_right = eye_right_raw * Config.EYE_MULTIPLIER
        eye_right = np.clip(eye_right, 0.0, 1.0)

        #Head movement 
        head_x = (landmarks[1].x - 0.5) * 2
        head_y = (landmarks[1].y - 0.5) * -2

        return {
            'mouth_open': float(mouth_open),
            'eye_left': float(eye_left),
            'eye_right': float(eye_right),
            'head_x': float(head_x),
            'head_y': float(head_y)
        }
    
    def smooth_data(self, data):
        if data is None:
            return None
        
        self.mouth_history.append(data['mouth_open'])
        self.eye_left_history.append(data['eye_left'])
        self.eye_right_history.append(data['eye_right'])
        self.head_x_history.append(data['head_x'])
        self.head_y_history.append(data['head_y'])

        return {
            'mouth_open': float(np.mean(self.mouth_history)),
            'eye_left': float(np.mean(self.eye_left_history)),
            'eye_right': float(np.mean(self.eye_right_history)),
            'head_x': float(np.mean(self.head_x_history)),
            'head_y': float(np.mean(self.head_y_history))
        }
        

