
import cv2
import mediapipe as mp
import pyautogui
import time
import keyboard   # <-- NEW: for global ESC quit
from collections import deque
pyautogui.FAILSAFE = False

# Deques for smoothing last few positions
smooth_x, smooth_y = deque(maxlen=5), deque(maxlen=5)

# Calibration factors (tweak if needed)
x_min, x_max = 0.25, 0.75
y_min, y_max = 0.25, 0.75

# Initialize Mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Capture webcam
cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()
click_cooldown = 1.0  # seconds between clicks
scroll_cooldown = 0.3  # seconds between scrolls
last_click_time = 0
last_scroll_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally (mirror view)
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process face landmarks
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Right and Left Iris landmarks
            right_eye = face_landmarks.landmark[474]
            left_eye = face_landmarks.landmark[469]

            # Convert to pixel coordinates
            right_x, right_y = int(right_eye.x * frame.shape[1]), int(right_eye.y * frame.shape[0])
            left_x, left_y = int(left_eye.x * frame.shape[1]), int(left_eye.y * frame.shape[0])

            # Draw circles on both eyes
            cv2.circle(frame, (right_x, right_y), 5, (0, 255, 0), -1)
            cv2.circle(frame, (left_x, left_y), 5, (255, 0, 0), -1)

            # Append current eye landmark values
            smooth_x.append(right_eye.x)   # FIXED
            smooth_y.append(right_eye.y)

            # Calculate moving average (smoothing)
            avg_x = sum(smooth_x) / len(smooth_x)
            avg_y = sum(smooth_y) / len(smooth_y)

            # Normalize within calibration range
            norm_x = (avg_x - x_min) / (x_max - x_min)
            norm_y = (avg_y - y_min) / (y_max - y_min)

            # Clamp to valid [0,1] range
            norm_x = max(0, min(1, norm_x))
            norm_y = max(0, min(1, norm_y))

            # Map to screen size
            screen_x = int(norm_x * screen_w)
            screen_y = int(norm_y * screen_h)

            # Move cursor
            pyautogui.moveTo(screen_x, screen_y)

            # Everyday actions
            current_time = time.time()

            # Blink detection (distance between upper & lower eyelid)
            right_top = face_landmarks.landmark[159]
            right_bottom = face_landmarks.landmark[145]
            vertical_dist = abs(right_top.y - right_bottom.y)

            if vertical_dist < 0.01:  # Eye closed (blink)
                if current_time - last_click_time > click_cooldown:
                    pyautogui.click()
                    last_click_time = current_time

            # Long blink for right click
            if vertical_dist < 0.01 and (current_time - last_click_time > 1.5):
                pyautogui.rightClick()
                last_click_time = current_time

            # Scroll using LEFT eye movement
            screen_scroll = (left_eye.y - 0.5) * 1000
            if abs(screen_scroll) > 80:  # threshold
                if current_time - last_scroll_time > scroll_cooldown:
                    pyautogui.scroll(int(-screen_scroll // 10))  # smoother scrolling
                    last_scroll_time = current_time

    cv2.imshow("Eye Controlled Mouse", frame)

    # Global ESC quit (works even if window not in focus)
    if keyboard.is_pressed("esc"):
        break

cap.release()
cv2.destroyAllWindows()
