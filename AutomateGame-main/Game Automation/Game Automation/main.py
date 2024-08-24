import cv2
import mediapipe as mp
import time
from event_hand_check import click_and_hold_mouse_at_position

# Tạm dừng 2 giây để chuẩn bị cho việc khởi chạy camera
time.sleep(2.0)

# Khởi tạo các mô-đun của Mediapipe để vẽ và nhận diện tay
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

# Danh sách các đầu ngón tay (tipIds) để theo dõi các ngón tay
tipIds = [4, 8, 12, 16, 20]

# Mở camera để thu video từ webcam
video = cv2.VideoCapture(0)

# Sử dụng mô-đun Mediapipe Hands với các thông số tin cậy tối thiểu
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        # Đọc khung hình từ camera
        ret, image = video.read()
        
        # Chuyển đổi khung hình từ BGR (mặc định của OpenCV) sang RGB (yêu cầu bởi Mediapipe)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False  # Tắt chế độ ghi để tăng tốc độ xử lý
        results = hands.process(image)  # Xử lý khung hình để nhận diện bàn tay
        image.flags.writeable = True  # Bật lại chế độ ghi
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Chuyển đổi lại sang BGR để hiển thị với OpenCV

        lmList = []  # Danh sách để lưu tọa độ các điểm mốc (landmarks) của bàn tay
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    # Tính toán tọa độ x, y dựa trên kích thước khung hình
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])  # Lưu trữ ID và tọa độ của từng điểm mốc
                # Vẽ các điểm mốc và kết nối chúng trên bàn tay
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)

        if len(lmList) != 0:
            fingers = []  # Danh sách để theo dõi trạng thái (mở hoặc đóng) của từng ngón tay

            # Kiểm tra ngón cái (thumb)
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # Nếu ngón cái nằm bên phải của ngón trỏ (trên tay trái)
                fingers.append(1)  # Ngón cái mở
            else:
                fingers.append(0)  # Ngón cái đóng

            # Kiểm tra các ngón còn lại
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:  # Nếu ngón tay đang mở (vị trí đầu ngón cao hơn khớp gần)
                    fingers.append(1)  # Ngón tay mở
                else:
                    fingers.append(0)  # Ngón tay đóng

            # Đếm tổng số ngón tay đang mở
            total = fingers.count(1)

            # Nếu không có ngón tay nào mở, thực hiện thao tác phanh (brake)
            if total == 0:
                click_and_hold_mouse_at_position(815, 626, duration=0.3)
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 0, 0), 5)

            # Nếu tất cả các ngón tay đều mở, thực hiện thao tác ga (gas)
            elif total == 5:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "GAS", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 0, 0), 5)
                click_and_hold_mouse_at_position(1386, 629, 0.3)

        # Hiển thị khung hình đã xử lý trên màn hình
        cv2.imshow("Frame", image)
        
        # Nếu nhấn phím 'q', thoát khỏi vòng lặp
        if cv2.waitKey(1) == ord('q'):
            break

# Giải phóng camera và đóng tất cả các cửa sổ
video.release()
cv2.destroyAllWindows()
