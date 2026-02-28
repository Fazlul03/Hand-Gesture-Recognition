import cv2
import mediapipe as mp
import pyautogui
import time

# --- Mediapipe modules ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Initialize Hands detector
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Finger tip landmark IDs
tip_ids = [4, 8, 12, 16, 20]

# Action cooldown
prev_action_time = 0
action_delay = 1

def fingers_up(landmarks):
    fingers = []
    
    # Thumb (x-axis check for right hand)
    if landmarks[tip_ids[0]][1] < landmarks[tip_ids[0]-1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Other fingers (y-axis check)
    for i in range(1, 5):
        if landmarks[tip_ids[i]][2] < landmarks[tip_ids[i]-2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers

def next_track():
    """Works on YouTube, Spotify, VLC, WMP, etc."""
    # Method 1: Media key (works in Spotify, WMP, VLC, etc.)
    pyautogui.press('nexttrack')
    time.sleep(0.1)
    # Method 2: YouTube specific (Shift+N)
    with pyautogui.hold('shift'):
        pyautogui.press('n')

def prev_track():
    """Works on YouTube, Spotify, VLC, WMP, etc."""
    # Method 1: Media key (works in Spotify, WMP, VLC, etc.)
    pyautogui.press('prevtrack')
    time.sleep(0.1)
    # Method 2: YouTube specific (Shift+P)
    with pyautogui.hold('shift'):
        pyautogui.press('p')

# --- Start webcam ---
cap = cv2.VideoCapture(0)
cv2.namedWindow("Hand Gesture Recognition", cv2.WINDOW_NORMAL)

print("=" * 50)
print("HAND GESTURE MEDIA CONTROLLER")
print("=" * 50)
print("Works with: Browser videos, VLC, WMP, etc.")
print("")
print("Gestures:")
print("  ✊ Fist                 → Play/Pause")
print("  ✋ Open Palm            → Fullscreen/Exit Fullscreen")
print("  👍 Thumbs Up           → Volume Up")
print("  👎 Pinky Only          → Volume Down")
print("  ✌️ Index + Pinky       → Next Track")
print("  🖐  Four Fingers (no thumb)       → Mute/Unmute")
print("  👌 Three Fingers (no thumb & index) → Previous Track")
print("  ✌️ Index + Middle      → +10 Seconds")
print("  👆 Index Only          → -10 Seconds")
print("")
print("Note: Use Right Hand Palm for accurate gestures")
print("")
print("Press 'q' to quit")
print("=" * 50)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            h, w, _ = frame.shape
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if lm_list:
                fingers = fingers_up(lm_list)
                current_time = time.time()

                # --- Gesture actions ---
                
                # Fist → PLAY/PAUSE
                if fingers == [0, 0, 0, 0, 0]:
                    cv2.putText(frame, "✊ FIST: Play/Pause", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    if current_time - prev_action_time > action_delay:
                        pyautogui.press('space')
                        prev_action_time = current_time

                # Open Palm → Fullscreen/Exit Fullscreen
                elif fingers == [1, 1, 1, 1, 1]:
                    cv2.putText(frame, "✋ OPEN PALM: Fullscreen/Exit", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    if current_time - prev_action_time > action_delay:
                        pyautogui.press('f')
                        prev_action_time = current_time

                # Thumbs Up → Volume Up
                elif fingers == [1, 0, 0, 0, 0]:
                    cv2.putText(frame, "👍 THUMBS UP: Volume +", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    if current_time - prev_action_time > action_delay:
                        pyautogui.press("volumeup")
                        prev_action_time = current_time
                
                # Pinky Only → Volume Down
                elif fingers == [0, 0, 0, 0, 1]:
                    cv2.putText(frame, "👎 PINKY ONLY: Volume -", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    if current_time - prev_action_time > action_delay:
                        pyautogui.press("volumedown")
                        prev_action_time = current_time
                
                # Index + Pinky → Next Track
                elif fingers == [0, 1, 0, 0, 1]:
                    cv2.putText(frame, "✌️ INDEX + PINKY: Next Track", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                    if current_time - prev_action_time > action_delay:
                        next_track()
                        prev_action_time = current_time
                
                # Index + Middle + Ring + Pinky (all except thumb) → Mute/Unmute
                elif fingers == [0, 1, 1, 1, 1]:
                    cv2.putText(frame, "🖐 4 FINGERS (no thumb): Mute/Unmute", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    if current_time - prev_action_time > action_delay:
                        pyautogui.press('m')
                        prev_action_time = current_time
                
                # Middle + Ring + Pinky → Previous Track
                elif fingers == [0, 0, 1, 1, 1]:
                    cv2.putText(frame, "👌 3 FINGERS (no thumb & Index): Previous Track", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 128, 0), 2)
                    if current_time - prev_action_time > action_delay:
                        prev_track()
                        prev_action_time = current_time
                
                # Index + Middle → +10 Seconds
                elif fingers == [0, 1, 1, 0, 0]:
                    cv2.putText(frame, "✌️ INDEX + MIDDLE: +10 Seconds", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    if current_time - prev_action_time > action_delay:
                        pyautogui.press('right')
                        prev_action_time = current_time
                
                # Index Only → -10 Seconds
                elif fingers == [0, 1, 0, 0, 0]:
                    cv2.putText(frame, "👆 INDEX ONLY: -10 Seconds", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)
                    if current_time - prev_action_time > action_delay:
                        pyautogui.press('left')
                        prev_action_time = current_time

    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if cv2.getWindowProperty("Hand Gesture Recognition", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()