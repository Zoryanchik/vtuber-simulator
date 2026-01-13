"""
MediaPipe Face Tracking Module =)
"""
import mediapipe as mp
import cv2 as cv

from config import Config

class FaceTracker:
    print("All good rn ") 

    def __init__(self):

        # Mediapipe face mesh initialization
        self.mp_face_mesh = mp.solutions.face_mesh(
        # Settings from config.py, we initialize them here, you can change them in config.py
            max_num_faces = Config.MaxNumFaces,
            refine_landmarks = Config.REFINE_LANDMARKS,
            min_detection_confidence = Config.MinDetectionConfidence,
            min_tracking_confidence = Config.MinTrackingConfidence
     )
        
    print("All initalized well")

    def get_face_landmarks(self, frame):

        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) # Convert BGR to RGB, because mediapipe uses RGB and OpenCV uses BGR
        results = self.mp_face_mesh.process(rgb_frame) # Process the frame and get the face landmarks(dots)

        if results.multi_face_landmarks: # If we have found face
            return results.multi_face_landmarks[0] # Return the first face found
        else:
            return None
        
    print("Face landmarks obtained")

    def show_landmarks(self, frame, landmarks):
        #The actual viuralization of the dots on the face
        if landmarks is None:
            return frame # If no landmarks, return original frame
        
        height, width, _ = frame.shape

        key_points = { 
            #here we use bgr format
            1: (255, 0, 0),      # Nose tip - Blue
            13: (0, 255, 0),     # Upper lip - Green
            14: (0, 255, 0),     # Lower lip - Green
            159: (0, 0, 255),    # Left eye upper - Red
            145: (0, 0, 255),    # Left eye lower - Red
            386: (0, 0, 255),    # Right eye upper - Red
            374: (0, 0, 255),    # Right eye lower - Red
        }

        for index, color in key_points.items(): #tuple unpacking

            x = int(landmarks[index].x * width)
            y = int(landmarks[index].y * height)

            cv.circle(frame, (x, y), 4, color, -1) # Draw circle at the landmark position


            cv.putText(frame, str(index), (x + 6, y - 6), cv.FONT_HERSHEY_SIMPLEX, 0.4, color, 1) # Draw index near dot

        return frame
