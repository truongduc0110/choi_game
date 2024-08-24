import cv2
import mediapipe as mp
import time
from directkeys import right_pressed,left_pressed
from directkeys import PressKey, ReleaseKey  

from pynput import mouse, keyboard

# Tạo đối tượng để điều khiển chuột
mouse_controller = mouse.Controller()

def click_and_hold_mouse_at_position(x, y, duration=1):
    mouse_controller.position = (x, y)  # Di chuyển chuột đến vị trí (x, y)
    mouse_controller.press(mouse.Button.left)  # Nhấn chuột trái tại vị trí đó
    time.sleep(duration)  # Giữ chuột trong khoảng thời gian
    mouse_controller.release(mouse.Button.left)
# Hàm để click và giữ chuột trái
def click_and_hold_mouse(duration=1):
    mouse_controller.press(mouse.Button.left)  # Nhấn chuột trái
    time.sleep(duration)  # Giữ chuột trong một khoảng thời gian
    mouse_controller.release(mouse.Button.left)  # Thả chuột trái

# Hàm để click chuột trái
def click_mouse():
    mouse_controller.click(mouse.Button.left)

# Hàm này được gọi khi một phím được nhấn
def on_press(key):
    try:
        # Kiểm tra nếu phím được nhấn là số
        if key.char.isdigit():
            click_mouse()
            print(f"Clicked mouse because {key.char} was pressed")
    except AttributeError:
        pass

# Hàm này được gọi khi một phím được thả ra (không sử dụng trong ví dụ này)
def on_release(key):
    pass
def move_mouse_to_position(x, y):
    mouse_controller.position = (x, y)  # Di chuyển chuột đến vị trí (x, y)
    print(f"Chuột đã được di chuyển đến vị trí: {x}, {y}")

break_key_pressed=left_pressed
accelerato_key_pressed=right_pressed

time.sleep(2.0)
current_key_pressed = set()

mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands


tipIds=[4,8,12,16,20]

video=cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:
    while True:
        
        keyPressed = False
        break_pressed=False
        accelerator_pressed=False
        key_count=0
        key_pressed=0
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers=[]
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            if total==0:
                click_and_hold_mouse_at_position(815, 626, duration=0.3)
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "BRAKE", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                # PressKey(break_key_pressed)
                break_pressed=True
                current_key_pressed.add(break_key_pressed)
                key_pressed=break_key_pressed
                keyPressed = True
                key_count=key_count+1
            elif total==5:
                #moi them dong nay
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, " GAS", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                click_and_hold_mouse_at_position(1386, 629, 0.3)
                # PressKey(accelerato_key_pressed)
                key_pressed=accelerato_key_pressed
                accelerator_pressed=True
                keyPressed = True
                current_key_pressed.add(accelerato_key_pressed)
                key_count=key_count+1
       


            # if lmList[8][2] < lmList[6][2]:
            #     print("Open")
            # else:
            #     print("Close")
        cv2.imshow("Frame",image)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break
video.release()
cv2.destroyAllWindows()

