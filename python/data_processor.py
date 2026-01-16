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
        
        #
        mouth_open_raw = abs(landmarks[14].y - landmarks[13].y)
        mouth_open = mouth_open_raw * Config.MOUTH_MULTIPLIER
        mouth_open = np.clip(mouth_open, 0.0, 1.0)

        eye_left_raw = abs(landmarks[159].y - landmarks[145].y)
        eye_left = eye_left_raw * Config.EYE_MULTIPLIER
        eye_left = np.clip(eye_left, 0.0, 1.0)

        eye_right_raw = abs(landmarks[386].y - landmarks[374].y)
        eye_right = eye_right_raw * Config.EYE_MULTIPLIER
        eye_right = np.clip(eye_right, 0.0, 1.0)

