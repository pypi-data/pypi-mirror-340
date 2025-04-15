import cv2 as cv

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

display_bg = init_background()
cv.imshow('Image Filters', display_bg)

while True:
    key = cv.waitKey(30)
    if key == 27:  # ESC
        break

cv.destroyAllWindows()