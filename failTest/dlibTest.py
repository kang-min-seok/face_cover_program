import cv2
import dlib

# dlib의 얼굴 검출기를 로드합니다.
detector = dlib.get_frontal_face_detector()

# 이미지 파일을 읽어옵니다.
image = cv2.imread("C:/Users/min10/Desktop/KakaoTalk_20240808_135302995_08.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 스티커 이미지 파일을 읽어옵니다.
sticker = cv2.imread("C:/Users/min10/Desktop/10001grinningface_109983.png", cv2.IMREAD_UNCHANGED)

# 얼굴을 검출합니다.
faces = detector(gray)

# 검출된 얼굴에 스티커를 붙입니다.
for face in faces:
    x, y, w, h = face.left(), face.top(), face.width(), face.height()

    # 스티커 이미지를 얼굴 크기에 맞게 조절합니다.
    sticker_resized = cv2.resize(sticker, (w, h))

    # 스티커 이미지가 알파 채널을 가지고 있을 때 처리
    if sticker_resized.shape[2] == 4:
        alpha_s = sticker_resized[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            image[y:y+h, x:x+w, c] = (alpha_s * sticker_resized[:, :, c] +
                                      alpha_l * image[y:y+h, x:x+w, c])
    else:
        image[y:y+h, x:x+w] = sticker_resized

# 결과 이미지를 출력합니다.
cv2.imshow('Detected Faces with Sticker', image)
cv2.waitKey(0)
cv2.destroyAllWindows()