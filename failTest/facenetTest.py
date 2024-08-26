import cv2
from mtcnn import MTCNN
import numpy as np

# MTCNN 초기화
detector = MTCNN()

# 스티커 이미지 파일 읽기 (스티커는 PNG 파일이어야 하며, 알파 채널을 가지고 있어야 함)
sticker = cv2.imread('smileIcon.png', cv2.IMREAD_UNCHANGED)

# 이미지 파일을 읽어옵니다.
image_path = 'test3.jpg'
image = cv2.imread(image_path)

pixel = np.asarray(image)
result = detector.detect_faces(pixel)

# 검출된 얼굴 정보 출력 (디버깅 용도)
print(f"Detected {len(result)} faces")

# 검출된 얼굴에 스티커를 붙입니다.
for i, face in enumerate(result):
    x, y, w, h = face['box']
    print(f"Face {i+1}: x={x}, y={y}, w={w}, h={h}")

    # 스티커 이미지를 얼굴 크기에 맞게 조절합니다.
    sticker_resized = cv2.resize(sticker, (w, h))

    # 스티커를 얼굴 위치에 맞춰 중앙에 배치합니다.
    y1, y2 = y, y + h
    x1, x2 = x, x + w

    # 스티커 이미지가 알파 채널을 가지고 있을 때 처리
    if sticker_resized.shape[2] == 4:
        alpha_s = sticker_resized[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            image[y1:y2, x1:x2, c] = (alpha_s * sticker_resized[:, :, c] +
                                      alpha_l * image[y1:y2, x1:x2, c])
    else:
        image[y1:y2, x1:x2] = sticker_resized

# 결과 이미지를 출력합니다.
# 결과 이미지를 출력하기 전에 크기를 줄입니다.
scale_percent = 50  # 이미지 크기를 50%로 줄이기
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# 이미지 리사이즈
resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

# 리사이즈된 이미지를 출력합니다.
cv2.imshow('Detected Faces with Stickers', resized_image)
#cv2.imshow('Detected Faces with Stickers', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
