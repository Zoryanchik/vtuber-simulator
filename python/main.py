import cv2 as cv
import time
from face_tracker import FaceTracker
from config import Config
from data_processor import DataProcessor


def print_banner():
    print("""
    ================================
        Vtuber Face Tracker
    ================================
    """)

    print( f"Camera: {Config.CameraWidth}x{Config.CameraHeight} = {Config.CameraFps}fps" )

    print("================================")
    print("")


def main():

    print_banner()
    tracker = FaceTracker()
    processor = DataProcessor()

    print("Starting video capture...")
    capture = cv.VideoCapture(Config.CameraID)

    # Set camera properties
    capture.set(cv.CAP_PROP_FRAME_WIDTH, Config.CameraWidth)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, Config.CameraHeight)
    capture.set(cv.CAP_PROP_FPS, Config.CameraFps)

    if not capture.isOpened():
        print("Error: Could not open video, please try again.")
        return
    print("Video capture started.")

    time_rn = time.time()
    frame_count = 0
    current_fps = 0

    while True:
        ret, frame = capture.read()# ret returtns true if frame is read correctly
        if not ret:
            print("Error: Could not read frame, exiting.")
            break
        
        if Config.Camera_Flip:
            frame = cv.flip(frame, 1)
        
        landmarks = tracker.get_face_landmarks(frame)

        if landmarks:

            raw_data = processor.extract_features(landmarks)
            smooth_data = processor.smooth_data(raw_data)

            if Config.Show_Dots:
                frame = tracker.show_landmarks(frame, landmarks)
            cv.putText(frame, "FACE DETECTED", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
            
            if Config.Show_Values:
                y_pos = 100
                cv.putText(frame, f"Mouth: {smooth_data['mouth_open']:.2f}", 
                          (10, y_pos), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                y_pos += 30
                cv.putText(frame, f"Eye L: {smooth_data['eye_left']:.2f}", 
                          (10, y_pos), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                y_pos += 30
                cv.putText(frame, f"Eye R: {smooth_data['eye_right']:.2f}", 
                          (10, y_pos), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                y_pos += 30
                cv.putText(frame, f"Head X: {smooth_data['head_x']:.2f}", 
                          (10, y_pos), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                y_pos += 30
                cv.putText(frame, f"Head Y: {smooth_data['head_y']:.2f}", 
                          (10, y_pos), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
      
      
        else:
            cv.putText(frame, "NO FACE", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

        # FPS calculation
        frame_count += 1
        if (time.time() - time_rn) >= 1.0:
            current_fps = frame_count
            frame_count = 0
            time_rn = time.time()

        if Config.Show_Fps:
            fps_color = (0, 255, 0) if current_fps >= 25 else (0, 165, 255)   

            cv.putText(frame, f"FPS: {current_fps}", (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, fps_color, 1)

        cv.imshow("Vtuber Face Tracker, press 'q' to quit", frame)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Exiting...")
            break

    capture.release()
    cv.destroyAllWindows()
    print("Resources released, program ended.")

if __name__ == "__main__":
    main()