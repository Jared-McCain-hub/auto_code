import pyautogui
import time

wait_seconds = 7 
print(f"请在{wait_seconds}中内将鼠标移动到目标上")
time.sleep(wait_seconds)
pos = pyautogui.position()
print(f"检测到坐标{pos}")