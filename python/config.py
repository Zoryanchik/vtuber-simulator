"""
Project: Config

"""

class Config: #Same as in java or c#, we talk through Config.smthing
    #Camera settings

    CameraID = 0
    #If you have a few cameras, you can change the camera ID here
    CameraWidth = 640
    CameraHeight = 480
    #I use 640x480 resolution for my camera bc it is faster but you can try and do 1280x720 or 1920x1080
    CameraFps = 60
    #Most 0f cameras use 30/60 fps

    #Mediapipe settings

    MinDetectionConfidence = 0.7
    MinTrackingConfidence = 0.7
    #You can change these values to increase/decrease detection/tracking quality
    MaxNumFaces= 1 # For now lets just do 1 face at a time
    REFINE_LANDMARKS = True# improve quality for better capture of face(lips, eyes, irises, pupils)

    #Multiplyers for more natural movement
    #MAkje number bigger for more exagerated movement or less for more subtle movement
    SMOOTHING = 5
    MOUTH_MULTIPLIER = 4.0
    EYE_MULTIPLIER = 25

    #Unity settings
    UnityPort = 5005 # ur unity port here
    UnityIp = "127.0.0.1" #Ur ip adress here

    #Debug settings
    Show_Dots = True
    #Show dots on face for debugging
    Show_Fps = True
    #Show fps counter
    Show_Values = True
    #Show values of mouth and eyes for debugging
    Camera_Flip = False
    #Flip camera horizontally