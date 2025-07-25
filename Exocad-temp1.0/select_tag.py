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
    # 关键字列表
    EXIT_KEYWORDS = ['牙龈扫描', '回切部分', '螺丝', '基台', '贴面', '嵌体']
    # 合并部分关键词
    MERGE_KEYWORD = '合并部分'

    # 定义各区域坐标
    HIDE_REGION = (20, 273, 89 - 20, 306 - 273)         # 原“隐藏”按钮区域
    EXPAND_REGION = (18, 15, 280 - 18, 841 - 15)        # 展开后检测区域


    # 1. 点击“隐藏”按钮
    hide_x, hide_y, hide_w, hide_h = HIDE_REGION
    hide_img = np.array(pyautogui.screenshot(region=HIDE_REGION))
    results = reader.readtext(hide_img)
    for bbox, text, _ in results:
        if '隐藏' in text:
            xs = [pt[0] for pt in bbox]
            ys = [pt[1] for pt in bbox]
            cx = int(sum(xs)/4) + hide_x
            cy = int(sum(ys)/4) + hide_y
            pyautogui.click(x=cx, y=cy)
            time.sleep(1)
            break

    # 2. 在新区域内 OCR 识别
    ex_x, ex_y, ex_w, ex_h = EXPAND_REGION
    img = np.array(pyautogui.screenshot(region=EXPAND_REGION))
    results = reader.readtext(img)
    texts = [t for _, t, _ in results]

    # 3a. 检测退出关键词
    for kw in EXIT_KEYWORDS:
        if any(kw in t for t in texts):
            print(f"检测到退出关键词 '{kw}'，关闭当前 Exocad 会话。")
            subprocess.call(["TASKKILL", "/IM", "DentalDB.exe", "/F"])
            subprocess.call(["TASKKILL", "/IM", "DentalCADApp.exe", "/F"])
            return False

    # 3b. 检测合并部分关键词
    if not any(MERGE_KEYWORD in t for t in texts):
        print(f"未检测到关键筛选词 '{MERGE_KEYWORD}'，关闭当前 Exocad 会话。")
        subprocess.call(["TASKKILL", "/IM", "DentalDB.exe", "/F"])
        subprocess.call(["TASKKILL", "/IM", "DentalCADApp.exe", "/F"])
        return False

    # 4. 筛选通过，重新点击“隐藏”按钮以收起列表
    print("区域文字筛选通过，继续后续流程。收起列表。")
    pyautogui.click(x=cx, y=cy)
    time.sleep(1)
    return True

