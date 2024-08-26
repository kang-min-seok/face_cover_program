import os
import queue
import threading
import time
import cv2
import face_recognition


# 스티커 이미지 파일 경로
sticker_path = "smileIcon.png"
sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)

# 이미지가 있는 폴더와 저장할 폴더 경로
input_folder = "input_images/" 
output_folder = "output_images/"

# 출력 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 글로벌 변수 초기화
start_point = None
end_point = None
drawing = False
sticker_positions = []
mosaic_positions = []
image = None
image_copy = None
face_queue = queue.Queue()

def face_recognition_worker(input_folder, face_queue):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image {filename}")
                continue  # 이미지가 로드되지 않았으면 넘어감
            fr_image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(fr_image)
            if not face_locations:
                print(f"No faces found in {filename}")
            face_queue.put((filename, image, face_locations))

def show_image(window_name, img, scale_factor=0.5):
    resized_img = cv2.resize(img, (int(img.shape[1] * scale_factor), int(img.shape[0] * scale_factor)))
    cv2.imshow(window_name, resized_img)
    cv2.waitKey(1)
    return scale_factor

# 마우스 클릭 콜백 함수
def draw_rectangle(event, x, y, flags, param):
    global start_point, end_point, drawing, image, sticker_positions, mosaic_positions, image_copy, scale_factor

    # 클릭 좌표를 원본 이미지 크기에 맞게 조정
    x = int(x / scale_factor)
    y = int(y / scale_factor)

    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 누름: 드래그 시작 (스티커 추가)
        for (x_offset, y_offset, new_w, new_h) in sticker_positions:
            if x_offset <= x <= x_offset + new_w and y_offset <= y <= y_offset + new_h:
                image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = image_copy[y_offset:y_offset+new_h, x_offset:x_offset+new_w]
                sticker_positions.remove((x_offset, y_offset, new_w, new_h))
                show_image('Detected Faces with Sticker', image, scale_factor)
                drawing = False  # 드래그 효과 방지
                return

        start_point = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:  # 마우스 이동: 드래그 중
        if drawing:
            end_point = (x, y)
            temp_image = image.copy()
            if flags & cv2.EVENT_FLAG_LBUTTON:
                cv2.rectangle(temp_image, start_point, end_point, (0, 255, 0), 2)  # 녹색 사각형
            elif flags & cv2.EVENT_FLAG_RBUTTON:
                cv2.rectangle(temp_image, start_point, end_point, (0, 0, 255), 2)  # 빨간색 사각형
            
            show_image('Detected Faces with Sticker', temp_image, scale_factor)

    elif event == cv2.EVENT_LBUTTONUP:  # 왼쪽 버튼 뗌: 드래그 종료
        if not drawing:
            return

        drawing = False
        end_point = (x, y)
        x1, y1 = min(start_point[0], end_point[0]), min(start_point[1], end_point[1])
        x2, y2 = max(start_point[0], end_point[0]), max(start_point[1], end_point[1])

        if x1 == x2 or y1 == y2:
            return

        w = x2 - x1
        h = y2 - y1

        sticker_aspect_ratio = sticker.shape[1] / sticker.shape[0]
        if w / h > sticker_aspect_ratio:
            new_h = h
            new_w = int(sticker_aspect_ratio * new_h)
        else:
            new_w = w
            new_h = int(new_w / sticker_aspect_ratio)

        sticker_resized = cv2.resize(sticker, (new_w, new_h))
        x_offset = x1 + (w - new_w) // 2
        y_offset = y1 + (h - new_h) // 2

        sticker_positions.append((x_offset, y_offset, new_w, new_h))

        if sticker_resized.shape[2] == 4:
            alpha_s = sticker_resized[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s

            for c in range(0, 3):
                image[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c] = (
                    alpha_s * sticker_resized[:, :, c] +
                    alpha_l * image[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c]
                )
        else:
            image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = sticker_resized

        show_image('Detected Faces with Sticker', image, scale_factor)

    elif event == cv2.EVENT_RBUTTONDOWN:  # 오른쪽 버튼 누름: 드래그 시작 (모자이크 추가)
        for (x1, y1, x2, y2) in mosaic_positions:
            if x1 <= x <= x2 and y1 <= y <= y2:
                image[y1:y2, x1:x2] = image_copy[y1:y2, x1:x2]
                mosaic_positions.remove((x1, y1, x2, y2))
                show_image('Detected Faces with Sticker', image, scale_factor)
                drawing = False
                return

        start_point = (x, y)
        drawing = True

    elif event == cv2.EVENT_RBUTTONUP:  # 오른쪽 버튼 뗌: 드래그 종료
        if not drawing:
            return

        drawing = False
        end_point = (x, y)
        x1, y1 = min(start_point[0], end_point[0]), min(start_point[1], end_point[1])
        x2, y2 = max(start_point[0], end_point[0]), max(start_point[1], end_point[1])

        if x1 == x2 or y1 == y2:
            return

        mosaic_area = image[y1:y2, x1:x2]
        mosaic_size = 10
        mosaic_area = cv2.resize(mosaic_area, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
        mosaic_area = cv2.resize(mosaic_area, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
        image[y1:y2, x1:x2] = mosaic_area

        mosaic_positions.append((x1, y1, x2, y2))
        show_image('Detected Faces with Sticker', image, scale_factor)

# 백그라운드에서 얼굴 인식 작업을 시작
threading.Thread(target=face_recognition_worker, args=(input_folder, face_queue)).start()

# 얼굴 인식 결과를 메인 스레드에서 처리
while True:
    try:
        filename, image, face_locations = face_queue.get(timeout=5)  # 큐에서 가져오기
        image_copy = image.copy()
        sticker_positions = []
        mosaic_positions = []

        # 검출된 얼굴에 스티커 붙이기
        for top, right, bottom, left in face_locations:
            w = right - left
            h = bottom - top

            sticker_aspect_ratio = sticker.shape[1] / sticker.shape[0]
            if w / h > sticker_aspect_ratio:
                new_h = h
                new_w = int(sticker_aspect_ratio * new_h)
            else:
                new_w = w
                new_h = int(new_w / sticker_aspect_ratio)

            sticker_resized = cv2.resize(sticker, (new_w, new_h))
            x_offset = left + (w - new_w) // 2
            y_offset = top + (h - new_h) // 2

            # 스티커 위치 저장
            sticker_positions.append((x_offset, y_offset, new_w, new_h))

            if sticker_resized.shape[2] == 4:
                alpha_s = sticker_resized[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s

                for c in range(0, 3):
                    image[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c] = (
                        alpha_s * sticker_resized[:, :, c] +
                        alpha_l * image[y_offset:y_offset+new_h, x_offset:x_offset+new_w, c]
                    )
            else:
                image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = sticker_resized

        # 얼굴이 제대로 가려졌는지 확인하기 위해 이미지 표시
        scale_factor = show_image('Detected Faces with Sticker', image)  # scale_factor를 반환받아 사용
        cv2.setMouseCallback('Detected Faces with Sticker', draw_rectangle)

        cv2.waitKey(0)

        # 수정된 이미지를 출력 폴더에 저장
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, image)
        print(f"{filename} 저장 완료")
    except queue.Empty:
        time.sleep(1)  # 큐가 비어있을 경우 잠시 대기
        continue  # 큐에서 다시 가져오기 시도

    if face_queue.empty() and threading.active_count() == 1:
        # 큐가 비어 있고 백그라운드 작업이 종료된 경우
        print("모든 얼굴 인식 작업 완료.")
        break

cv2.destroyAllWindows()