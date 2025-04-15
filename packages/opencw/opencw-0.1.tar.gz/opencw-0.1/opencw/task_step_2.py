import cv2 as cv
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

background = cv.imread('background.png')
image_001 = cv.imread('image_001.png')
image_002 = cv.imread('image_002.png')
image_003 = cv.imread('image_003.png')
filter_image_001 = cv.imread('filter_image_001.png')
filter_image_002 = cv.imread('filter_image_002.png')

if any(img is None for img in [background, image_001, image_002, image_003, filter_image_001, filter_image_002]):
    print("Ошибка загрузки одного из изображений")
    exit()

background_height, background_width = 720, 1280
gallery_size = (260, 195)
preview_size = (800, 600)
filter_size = (100, 100)

image_001_gallery = cv.resize(image_001, gallery_size)
image_002_gallery = cv.resize(image_002, gallery_size)
image_003_gallery = cv.resize(image_003, gallery_size)
image_001_preview = cv.resize(image_001, preview_size)
filter_image_001_panel = cv.resize(filter_image_001, filter_size)
filter_image_002_panel = cv.resize(filter_image_002, filter_size)

def init_background():
    bg = background.copy()
    bg[20:215, 20:280] = image_001_gallery
    bg[235:430, 20:280] = image_002_gallery
    bg[450:645, 20:280] = image_003_gallery
    bg[20:120, 1160:1260] = filter_image_001_panel
    bg[140:240, 1160:1260] = filter_image_002_panel
    bg[20:620, 320:1120] = image_001_preview
    return bg

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

cursor_radius = 10
cursor_color = (0, 0, 255)  # Красный
active_cursor_color = (0, 255, 0)  # Зеленый при жесте
last_cursor_pos = (background_width // 2, background_height // 2)
gesture_threshold = 30  # Порог для жеста

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка чтения кадра")
        break

    frame = cv.flip(frame, 1)
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    frame = cv.cvtColor(frame_rgb, cv.COLOR_RGB2BGR)

    gesture_detected = False
    current_cursor = last_cursor_pos
    display_bg = init_background()

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            if handedness.classification[0].label != 'Right':
                continue

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            h, w = frame.shape[:2]
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            distance = math.hypot(thumb_x - index_x, thumb_y - index_y)
            gesture_detected = distance < gesture_threshold

            current_cursor = (index_x, index_y)
            last_cursor_pos = current_cursor

    x, y = current_cursor
    x = max(cursor_radius, min(x, background_width - cursor_radius))
    y = max(cursor_radius, min(y, background_height - cursor_radius))
    current_cursor = (x, y)

    cursor_color_current = active_cursor_color if gesture_detected else cursor_color

    cv.circle(display_bg, current_cursor, cursor_radius, cursor_color_current, -1)

    cv.imshow('Image Filters', display_bg)
    key = cv.waitKey(30)
    if key == 27:  # ESC
        break

cap.release()
cv.destroyAllWindows()