import time
from pynput import mouse, keyboard# Tạo đối tượng để điều khiển chuột
# có sự hỗ trợ của chatGPT ở file này để lấy sự kiện chuột
mouse_controller = mouse.Controller()

def click_and_hold_mouse_at_position(x, y, duration=1):
    mouse_controller.position = (x, y)  # Di chuyển chuột đến vị trí (x, y)
    mouse_controller.press(mouse.Button.left)  # Nhấn chuột trái tại vị trí đó
    time.sleep(duration)  # Giữ chuột trong khoảng thời gian
    mouse_controller.release(mouse.Button.left)

