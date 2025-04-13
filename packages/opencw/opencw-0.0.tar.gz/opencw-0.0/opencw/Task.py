import cv2 as cv
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

background = cv.imread('background.png')
background_height, background_width = background.shape[:2]

image_001 = cv.imread("image_001.png")
image_002 = cv.imread("image_002.png")

filtered_image_001 = cv.imread("image_filter_001.png")
filtered_image_002 = cv.imread("image_filter_002.png")

image_001_resized = cv.resize(image_001, (260, 195))
image_002_resized = cv.resize(image_002, (260, 195))
main_image_001_resized = cv.resize(image_001, (800, 600))
main_image_002_resized = cv.resize(image_002, (800, 600))

filtered_image_001_resized = cv.resize(filtered_image_001, (60, 60))
filtered_image_002_resized = cv.resize(filtered_image_002, (60, 60))
filtered_image_001_resized1 = cv.resize(filtered_image_001, (100, 100))
filtered_image_002_resized1 = cv.resize(filtered_image_002, (100, 100))

background[20:215, 20:280] = image_001_resized
background[235:430, 20:280] = image_002_resized

background[640:700, 320:380] = filtered_image_001_resized
background[640:700, 400:460] = filtered_image_002_resized

background[20:620, 320:1120] = main_image_001_resized

background[20:120, 1160:1260] = filtered_image_001_resized1
background[140:240, 1160:1260] = filtered_image_002_resized1

cursor_radius = 10
cursor_color = (0, 0, 255)
active_color = (0, 255, 0)
last_cursor_pos = (background_height//2, background_width//2)
selected_idx = -1

GESTURE_TRESHOLD = 20
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH,  1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

cv.imshow('Task #5', background)
while True:
    read_ok, frame = cap.read()
    if not read_ok:
        break

    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    gesture_detected = False
    current_cursor = last_cursor_pos

    if results.multi_hand_landmarks is not None:
        for hand_landmark, hand_nandedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            if hand_nandedness.classification[0].label != 'Right':
                continue

            thumb = hand_landmark.landmark[mp_hands. HandLandmark.THUMB_TIP]
            index = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            h, w = frame.shape[:2]
            thumb_x, thumb_y = int(thumb.x*w), int(thumb.y*h)
            index_x, index_y = int(index.x*w), int(index.y*h)

            distance = int(math.hypot(thumb_x - index_x, thumb_y - index_y))
            gesture_detected = distance < GESTURE_TRESHOLD

            current_cursor = (index_x, index_y)
            last_cursor_pos = current_cursor

    x, y = current_cursor
    x = max(cursor_radius, min(x, background_width - cursor_radius))
    y = max(cursor_radius, min(y, background_height - cursor_radius))
    current_cursor = (x, y)
    print(current_cursor)
    display_bg = background.copy()

    if gesture_detected:
        color = active_color
        if y >= 20 and y <= 215 and x >= 20 and x <= 280:
            background[20:620, 320:1120] = main_image_001_resized
        if y >= 235 and y <= 430 and x >= 20 and x <= 280:
            background[20:620, 320:1120] = main_image_002_resized
    else:
        color = cursor_color

    cv.circle(display_bg, current_cursor, cursor_radius, color, -1)

    cv.imshow( "Task #5", display_bg)
    k = cv.waitKey(30)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()