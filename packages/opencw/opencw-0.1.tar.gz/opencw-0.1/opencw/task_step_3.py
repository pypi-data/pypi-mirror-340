import cv2 as cv
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
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
active_filter_size = (60, 60)

image_001_gallery = cv.resize(image_001, gallery_size)
image_002_gallery = cv.resize(image_002, gallery_size)
image_003_gallery = cv.resize(image_003, gallery_size)

image_001_preview = cv.resize(image_001, preview_size)
image_002_preview = cv.resize(image_002, preview_size)
image_003_preview = cv.resize(image_003, preview_size)

filter_image_001_panel = cv.resize(filter_image_001, filter_size)
filter_image_002_panel = cv.resize(filter_image_002, filter_size)
filter_image_001_active = cv.resize(filter_image_001, active_filter_size)
filter_image_002_active = cv.resize(filter_image_002, active_filter_size)

gallery_coords = [(20, 20), (20, 235), (20, 450)]
preview_area = (320, 20, 1120, 620)
filter_panel_coords = [(1160, 20), (1160, 140)]
active_filter_panel = (320, 640, 1120, 700)

def init_background():
    bg = background.copy()
    bg[20:215, 20:280] = image_001_gallery
    bg[235:430, 20:280] = image_002_gallery
    bg[450:645, 20:280] = image_003_gallery
    bg[20:120, 1160:1260] = filter_image_001_panel
    bg[140:240, 1160:1260] = filter_image_002_panel
    return bg

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

cursor_radius = 10
cursor_color = (0, 0, 255)
active_cursor_color = (0, 255, 0)
last_cursor_pos = (background_width // 2, background_height // 2)
gesture_threshold = 30

selected_image_idx = 1
active_filters = []
dragging_filter = None
display_bg = init_background()

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

    if gesture_detected:
        cursor_color_current = active_cursor_color
        for idx, (gx, gy) in enumerate(gallery_coords, 1):
            if gx <= x <= gx + 260 and gy <= y <= gy + 195:
                selected_image_idx = idx
                break
    else:
        cursor_color_current = cursor_color

    if gesture_detected and dragging_filter is None:
        for idx, (fx, fy) in enumerate(filter_panel_coords, 1):
            if fx <= x <= fx + 100 and fy <= y <= fy + 100:
                dragging_filter = idx
                break

    if dragging_filter:
        fx = x - filter_size[0] // 2
        fy = y - filter_size[1] // 2
        fx = max(0, min(fx, background_width - filter_size[0]))
        fy = max(0, min(fy, background_height - filter_size[1]))
        filter_img = filter_image_001_panel if dragging_filter == 1 else filter_image_002_panel
        display_bg[fy:fy+100, fx:fx+100] = filter_img

        if not gesture_detected:
            if (preview_area[0] <= fx <= preview_area[2] - filter_size[0] and
                preview_area[1] <= fy <= preview_area[3] - filter_size[1]):
                if len(active_filters) < 2 and dragging_filter not in active_filters:
                    active_filters.append(dragging_filter)
            dragging_filter = None

    if gesture_detected:
        for idx, filter_idx in enumerate(active_filters[:]):
            fx = 320 + idx * 80
            fy = 640
            if fx <= x <= fx + 60 and fy <= y <= fy + 60:
                active_filters.pop(idx)
                break

    selected_image = {
        1: image_001_preview,
        2: image_002_preview,
        3: image_003_preview
    }.get(selected_image_idx, image_001_preview)

    display_bg[20:620, 320:1120] = selected_image

    for idx, (gx, gy) in enumerate(gallery_coords, 1):
        if idx == selected_image_idx:
            cv.rectangle(display_bg, (gx, gy), (gx + 260, gy + 195), (76, 177, 34), 2)

    for idx, filter_idx in enumerate(active_filters):
        fx = 320 + idx * 80
        filter_img = filter_image_001_active if filter_idx == 1 else filter_image_002_active
        display_bg[640:700, fx:fx+60] = filter_img

    cv.circle(display_bg, current_cursor, cursor_radius, cursor_color_current, -1)

    cv.imshow('Image Filters', display_bg)
    key = cv.waitKey(30)
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()