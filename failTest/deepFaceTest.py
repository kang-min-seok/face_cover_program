import cv2
from deepface import DeepFace

result = DeepFace.verify(
  img1_path = "C:/Users/min10/Desktop/KakaoTalk_20240808_135302995_08.jpg",
  img2_path = "C:/Users/min10/Desktop/KakaoTalk_20240808_135302995_08.jpg",
)


# # 이미지 파일을 읽어옵니다.
# image_path = "C:/Users/min10/Desktop/KakaoTalk_20240808_135302995_08.jpg"
# image = cv2.imread(image_path)

# # 스티커 이미지 파일을 읽어옵니다.
# sticker_path = "C:/Users/min10/Desktop/10001grinningface_109983.png"
# sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)

# # 얼굴을 검출합니다.
# faces = DeepFace.extract_faces(img_path=image_path, detector_backend='retinaface')

# # 검출된 얼굴에 스티커를 붙입니다.
# for face in faces:
#     facial_area = face['facial_area']  # 딕셔너리에서 'facial_area' 키를 사용하여 좌표 가져오기
#     x, y, w, h = facial_area[0], facial_area[1], facial_area[2], facial_area[3]

#     # 얼굴 영역이 이미지 크기를 벗어나지 않도록 조정
#     x_end = min(x + w, image.shape[1])
#     y_end = min(y + h, image.shape[0])
#     w = x_end - x
#     h = y_end - y

#     # 스티커 이미지를 얼굴 크기에 맞게 비율을 유지하여 조절합니다.
#     sticker_aspect_ratio = sticker.shape[1] / sticker.shape[0]
#     if w / h > sticker_aspect_ratio:
#         new_h = h
#         new_w = int(sticker_aspect_ratio * new_h)
#     else:
#         new_w = w
#         new_h = int(new_w / sticker_aspect_ratio)

#     sticker_resized = cv2.resize(sticker, (new_w, new_h))

#     # 스티커를 이미지 위에 위치시킵니다.
#     x_offset = x + (w - new_w) // 2
#     y_offset = y + (h - new_h) // 2

#     # 스티커 이미지가 알파 채널을 가지고 있을 때 처리
#     if sticker_resized.shape[2] == 4:
#         alpha_s = sticker_resized[:, :, 3] / 255.0
#         alpha_l = 1.0 - alpha_s

#         for c in range(0, 3):
#             image[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c] = (
#                 alpha_s * sticker_resized[:, :, c] +
#                 alpha_l * image[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c]
#             )
#     else:
#         image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = sticker_resized

# # 결과 이미지를 출력합니다.
# cv2.imshow('Detected Faces with Sticker', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
