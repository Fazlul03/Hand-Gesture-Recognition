# Hand Gesture Recognition Control

A real-time hand gesture recognition system that allows you to control media playback (play/pause, volume, next track) using hand gestures via your webcam.

(i) Hand Gesture Recognition

(ii) OpenCV

(iii) Mediapipe

Features:
---------
🎯 Real-time hand tracking using Mediapipe

🎮 Control media playback without touching keyboard

🔊 Volume control with hand gestures

⏯️ Play/Pause/Stop media

⏭️ Skip to next track / Previous Track

Prerequisites:
--------------
-> Python 3.11 (Python 3.14+ not supported)

-> Webcam

-> Windows OS (for media key controls)

Installation:
-------------
1. Clone the Repository:
  Cmd:

  git clone https://github.com/Fazlul03/hand-gesture-recognition.git

  cd hand-gesture-recognition

2. Install Python 3.11:

  Download from: https://www.python.org/downloads/release/python-3119/

3. Install Dependencies:
  Cmd:

  py -3.11 -m pip install mediapipe==0.10.8 opencv-python pyautogui
  Usage- Connect your webcam

Run the application:
--------------------
Cmd:

py -3.11 hand_gesture_demo.py

A window will open showing your webcam feed

Make gestures to control media:
-------------------------------

-> Show a fist to play/pause

-> Show open palm to Fullscreen/exit

-> Show thumbs up to increase volume

-> Show Pinky finger to decrease volume

-> Show index finger to backward 10 secs

-> show peace sign to forward 10 secs

-> show rock sign to go next track.

-> show super sign to go previous track.

-> show four fingers except thumb to Mute/Unmute.

-> Press 'q' or click the X button to quit



Troubleshooting:
----------------
### Problem: 

"module 'mediapipe' has no attribute 'solutions'"
  
(This usually means you're using Python 3.14 or a newer Mediapipe version.)


### Solution:

py -3.11 -m pip install mediapipe==0.10.8



### Webcam not opening:

-> Check if webcam is connected

-> Close other applications using webcam

-> Try changing 0 to 1 in cv2.VideoCapture(0)

### Gestures not recognized:

-> Ensure good lighting

-> Keep your hand within the camera frame

-> Make clear, distinct gestures

-> Stay at a comfortable distance from the camera

Customization:
--------------
Change Action Delay
Modify the action_delay variable (in seconds):


Supported Media Players:
------------------------
-> YouTube (browser)

-> VLC Media Player

-> Windows Media Player

-> Spotify

-> Any app responding to keyboard media keys

Acknowledgments:
----------------
-> Mediapipe for hand tracking technology

-> OpenCV for computer vision capabilities

-> PyAutoGUI for keyboard automation
