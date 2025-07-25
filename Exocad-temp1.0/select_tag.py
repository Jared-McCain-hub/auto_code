import sys
import numpy as np
import pyautogui
from easyocr import Reader
import time

# 全局 OCR 实例（已在脚本开头创建）
# reader = Reader(['ch_sim', 'en'], gpu=False)




def perform_original_exit():
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
    sys.exit()

def detect_in_region_and_exit():
    EXIT_KEYWORDS = ['牙龈扫描', '回切部分', '螺丝通道', '基台', '贴面', '嵌体']
    other_exit_keywords = ["合并部分"]

    # 计算区域宽高
    x0, y0 = 18, 15
    x1, y1 = 280, 284
    width = x1 - x0
    height = y1 - y0

    # 截取区域截图并 OCR
    img = np.array(pyautogui.screenshot(region=(x0, y0, width, height)))
    results = reader.readtext(img)

    # 遍历 OCR 结果，检查关键词
    for bbox, text, conf in results:
        for kw in EXIT_KEYWORDS:
            if kw in text:
                print(f"检测到关键词 '{kw}'，执行退出操作。")
                perform_original_exit()
                return False
            
        for kw_1 in other_exit_keywords:
            if kw_1 not in text:
                print(f"未检测到关键词{kw_1},执行退出操作。")
                perform_original_exit()
                return False

    # 继续执行
    print("继续后面流程")

