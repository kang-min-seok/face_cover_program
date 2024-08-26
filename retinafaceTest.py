import cv2
import os
from retinaface import RetinaFace


def overlay_sticker_on_face(base_img, sticker, position):
    x, y, w, h = position

    # 스티커 크기를 얼굴 크기에 맞게 조정
    sticker_resized = cv2.resize(sticker, (w - x, h - y))

    # 스티커의 알파 채널 분리 (스티커 이미지가 투명도를 가진 경우)
    if sticker_resized.shape[2] == 4:  # 4 채널 (RGBA)
        sticker_alpha = sticker_resized[:, :, 3] / 255.0
        sticker_rgb = sticker_resized[:, :, :3]

        for c in range(0, 3):
            base_img[y:h, x:w, c] = (
                sticker_alpha * sticker_rgb[:, :, c] + (1.0 - sticker_alpha) * base_img[y:h, x:w, c]
            )
    else:
        # 스티커에 알파 채널이 없으면 그대로 덮어쓰기
        base_img[y:h, x:w] = sticker_resized

def process_images_in_folder(input_folder, output_folder, sticker_path):
    # 스티커 이미지 로드
    sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)
    
    # 입력 폴더의 모든 이미지 파일 처리
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)
            resp = RetinaFace.detect_faces(img_path, threshold=0.1)

            for idx, identity in resp.items():
                facial_area = identity["facial_area"]
                overlay_sticker_on_face(img, sticker, (facial_area[0], facial_area[1], facial_area[2], facial_area[3]))

            # 결과 이미지 저장
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img)


input_folder = "input_images/"
output_folder = "output_images/"
sticker_path = "smileIcon.png"

# 출력 폴더가 존재하지 않으면 생성
os.makedirs(output_folder, exist_ok=True)

process_images_in_folder(input_folder, output_folder, sticker_path)
