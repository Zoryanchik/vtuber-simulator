import cv2 as cv
import time
from face_tracker import FaceTracker
from config import Config


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

    print("Starting video captureture...")
    capture = cv.Videocaptureture(Config.CameraID)

    # Set camera properties
    capture.set(cv.capture_PROP_FRAME_WIDTH, Config.CameraWidth)
    capture.set(cv.capture_PROP_FRAME_HEIGHT, Config.CameraHeight)
    capture.set(cv.capture_PROP_FPS, Config.CameraFps)

    if not capture.isOpened():
        print("Error: Could not open video, please try again.")
        return
    print("Video captureture started.")

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
            if Config.Show_Dots:
                frame = tracker.show_landmarks(frame, landmarks)
         
            
            cv.putText(frame, "FACE DETECTED", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv.putText(frame, "NO FACE", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # FPS calculation
        frame_count += 1
        if (time.time() - time_rn) >= 1.0:
            current_fps = frame_count
            frame_count = 0
            time_rn = time.time()

        if Config.Show_Fps:
            fps_color = (0, 255, 0) if current_fps >= 25 else (0, 165, 255)   

            cv.putText(frame, f"FPS: {current_fps}", (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, fps_color, 2)

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