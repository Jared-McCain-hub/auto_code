import os
import shutil
import subprocess
import time
import cv2
import pyautogui

import pyperclip
import numpy as np
from crown_detect import CrownDetect
import easyocr

result_exocad = None
reader = easyocr.Reader(['ch_sim'])


def main():
    DentalDB_path = "D:/exocad-DentalCAD3.2-2024-02-14/exocad-DentalCAD3.2-2024-02-14/DentalDB/bin/DentalDB.exe"
    source_dir = r"D:\exocad-data\datas_2025-06-20-huaxing-exocalonly-2"
    iamges_true_path = os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir) + "_true_images")
    iamges_false_path = os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir) + "_false_images")
    file_true_path = os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir) + "_true.txt")
    file_false_path = os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir) + "_false.txt")
    if not os.path.exists(iamges_true_path):
        os.makedirs(iamges_true_path)
    if not os.path.exists(iamges_false_path):
        os.makedirs(iamges_false_path)

    detector = CrownDetect(r"crown_detect.pt")
    global result_exocad



    for file in os.listdir(source_dir):
        with open(file_true_path, 'r', encoding='utf-8') as f:
            existing_true = f.read().splitlines()
        with open(file_false_path, 'r', encoding='utf-8') as fi:
            existing_false = fi.read().splitlines()
        if (file not in existing_true) and (file not in existing_false):
            file_path = os.path.join(source_dir, file, file + ".dentalProject")
            print(file_path)
            time.sleep(5)
            pro = subprocess.Popen(DentalDB_path)  # 启动软件
            parent_pid = pro.pid
            print("parent_pid:", parent_pid)
            time.sleep(20)

            # pyautogui.hotkey("ctrl", "l")  #Load

            pyautogui.click(789, 58)  # Load

            time.sleep(2)
            pyautogui.click(143, 1271)  # exocad project
            time.sleep(2)
            pyautogui.click(900, 657)  # 点击路径输入框
            time.sleep(1)
            pyperclip.copy(file_path)
            print(file_path)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(2)
            pyautogui.hotkey("enter")
            time.sleep(2)

            pyautogui.click(1145, 610)
            time.sleep(1)
            pyautogui.click(1145, 930)
            time.sleep(1)

            region_img = (975, 540, 1000, 1000)
            save_img = pyautogui.screenshot(region=region_img)
            img_array = np.array(save_img)

            result = reader.readtext(img_array)
            sure_point = None
            for detection in result:
                text = detection[1]
                if text == "确定":
                    print(text)
                    corrdinates = detection[0]
                    save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                    save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                    sure_point = (save_x + 975, save_y + 540)
                    break
            if sure_point != None:
                pyautogui.click(x=sure_point[0], y=sure_point[1], clicks=1, button='left')  # 点击确定

            time.sleep(2)
            pyautogui.click(1397, 1423)  # 点击确定

            time.sleep(2)
            pyautogui.hotkey("enter")

            time.sleep(5)

            pyautogui.doubleClick(2135, 183)  # Design
            time.sleep(20)
            pyautogui.hotkey("enter")
            time.sleep(2)
            pyautogui.click(1230, 935)
            time.sleep(2)
            # 全屏显示
            pyautogui.click(1210, 820)
            time.sleep(1)
            pyautogui.hotkey("win", "up")

            time.sleep(1)
            pyautogui.click(1535, 855)
            # time.sleep(1)
            # pyautogui.click(1535, 855)

            region = (0, 0, 1000, 1000)
            save_img = pyautogui.screenshot(region=region)
            img_array = np.array(save_img)

            result = reader.readtext(img_array)
            for detection in result:
                text = detection[1]
                if text == "显示全部":
                    corrdinates = detection[0]
                    save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                    save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                    pyautogui.keyDown("ctrl")
                    pyautogui.click(x=save_x, y=save_y)
                    pyautogui.keyUp("ctrl")
                    time.sleep(1)

                    pyautogui.click(272, 705)
                    time.sleep(1)
                    pyautogui.hotkey("a")  # 对颌
                    time.sleep(1)
                    pyautogui.hotkey("s")  # 工作模型扫描
                    time.sleep(1)
                    pyautogui.hotkey("m")
                    time.sleep(1)
                    pyautogui.hotkey("e")

            time.sleep(2)
            pyautogui.click(x=2500, y=1363, clicks=1, button='left')
            time.sleep(2)

            #   下颌牙冠
            # time.sleep(4)
            pyautogui.click(2500, 1325)  # 下颌视角
            time.sleep(3)
            lowtoothmesh_path = pyautogui.screenshot()
            pngnamelow = os.path.join(iamges_true_path, file + "-LowerJaw.png")
            print(pngnamelow)
            lowtoothmesh_path.save(pngnamelow)

            time.sleep(1)
            region_low = (350, 100, 1750, 1200)

            # 获取牙冠并保存
            result = identify_exist_crown(pngnamelow)  # 判断是黄色还是灰色，看牙颌中是否存在冠
            boxes = detector.process(lowtoothmesh_path)
            print(boxes)
            if result == True and len(boxes) > 0:
                print("下颌box", boxes)
                get_box_point(boxes)

                # 保存下颌mesh
                time.sleep(3)
                result = click_toothmesh_with_box(pngnamelow)
                if result == False:
                    os.remove(pngnamelow)
                    pngfalselow = os.path.join(iamges_false_path, file + "-LowerJaw.png")
                    lowtoothmesh_path.save(pngfalselow)
                    result_exocad = False

                    time.sleep(2)
                    subprocess.call("TASKKILL /IM DentalDB.exe")
                    subprocess.call("TASKKILL /IM DentalCADApp.exe")
                    time.sleep(1)
                    # check_close_windows()
                    # time.sleep(2)
                    if result_exocad == False:
                        with open(file_false_path, 'r', encoding='utf-8') as fi:
                            existing_contents_false = fi.read().splitlines()
                        if file not in existing_contents_false:
                            with open(file_false_path, 'a') as fi:
                                fi.write(file + '\n')
                    elif result_exocad == True:
                        with open(file_true_path, 'r', encoding='utf-8') as f:
                            existing_contents_true = f.read().splitlines()
                        if file not in existing_contents_true:
                            with open(file_true_path, 'a') as f:
                                f.write(file + '\n')

                    continue


            else:
                result = click_toothmesh(region_low)
                if result == False:
                    os.remove(pngnamelow)
                    pngfalselow = os.path.join(iamges_false_path, file + "-LowerJaw.png")
                    lowtoothmesh_path.save(pngfalselow)
                    result_exocad = False

                    time.sleep(2)
                    subprocess.call("TASKKILL /IM DentalDB.exe")
                    subprocess.call("TASKKILL /IM DentalCADApp.exe")
                    time.sleep(1)
                    # check_close_windows()
                    # time.sleep(2)
                    if result_exocad == False:
                        with open(file_false_path, 'r', encoding='utf-8') as fi:
                            existing_contents_false = fi.read().splitlines()
                        if file not in existing_contents_false:
                            with open(file_false_path, 'a') as fi:
                                fi.write(file + '\n')
                    elif result_exocad == True:
                        with open(file_true_path, 'r', encoding='utf-8') as f:
                            existing_contents_true = f.read().splitlines()
                        if file not in existing_contents_true:
                            with open(file_true_path, 'a') as f:
                                f.write(file + '\n')

                    continue


            time.sleep(15)
            pyautogui.click(x=253, y=616, clicks=1, button='left')  # 点击文本输入框
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("backspace")
            time.sleep(2)
            lowerpath = os.path.join(source_dir, file, file + "-LowerJaw.stl")
            pyperclip.copy(lowerpath)
            print(lowerpath)
            time.sleep(1)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(2)
            pyautogui.click(x=1030, y=680, clicks=1, button='left')  # 保存文件
            # pyautogui.click(x=point[0], y=point[1], clicks=1, button='left')  # 保存文件
            time.sleep(2)
            pyautogui.hotkey("y")  # 是否替换已存在的数据
            time.sleep(1)
            pyautogui.click(x=1237, y=680, clicks=1, button='left')
            time.sleep(1)
            # pyautogui.click(x=point[0] + 80, y=point[1], clicks=1, button='left')  # 避免窗口还存在,点击取消
            time.sleep(1)
            result_exocad = True
            time.sleep(1)
            # shutil.copy(lowerpath, os.path.join(file_true_path, file))
            # time.sleep(2)

            # 上颌牙冠
            pyautogui.click(2500, 1395)  # 上颌视角

            time.sleep(3)
            upptoothmesh_path = pyautogui.screenshot()
            pngnameupp = os.path.join(iamges_true_path, file + "UpperJaw.png")
            upptoothmesh_path.save(pngnameupp)
            region_upp = (350, 100, 1750, 1200)

            time.sleep(1)
            # 获取牙冠并保存
            result1 = identify_exist_crown(pngnameupp)  # 判断是黄色还是灰色，看牙颌中是否存在冠
            boxes1 = detector.process(upptoothmesh_path)
            print(boxes1)
            if result1 == True and len(boxes1) > 0:
                print("上颌box", boxes1)
                get_box_point(boxes1)

                # 保存上颌mesh
                time.sleep(3)
                result = click_toothmesh_with_box(pngnameupp)
                if result == False:
                    os.remove(pngnameupp)
                    pngfalseupp = os.path.join(iamges_false_path, file + "-UpperJaw.png")
                    upptoothmesh_path.save(pngfalseupp)
                    result_exocad = False

                    time.sleep(2)
                    subprocess.call("TASKKILL /IM DentalDB.exe")
                    subprocess.call("TASKKILL /IM DentalCADApp.exe")
                    time.sleep(1)
                    # check_close_windows()
                    # time.sleep(2)
                    if result_exocad == False:
                        with open(file_false_path, 'r', encoding='utf-8') as fi:
                            existing_contents_false = fi.read().splitlines()
                        if file not in existing_contents_false:
                            with open(file_false_path, 'a') as fi:
                                fi.write(file + '\n')
                    elif result_exocad == True:
                        with open(file_true_path, 'r', encoding='utf-8') as f:
                            existing_contents_true = f.read().splitlines()
                        if file not in existing_contents_true:
                            with open(file_true_path, 'a') as f:
                                f.write(file + '\n')

                    continue


            else:
                result = click_toothmesh(region_upp)
                if result == False:
                    os.remove(pngnameupp)
                    pngfalseupp = os.path.join(iamges_false_path, file + "-UpperJaw.png")
                    upptoothmesh_path.save(pngfalseupp)
                    result_exocad = False

                    time.sleep(2)
                    subprocess.call("TASKKILL /IM DentalDB.exe")
                    subprocess.call("TASKKILL /IM DentalCADApp.exe")
                    time.sleep(1)
                    # check_close_windows()
                    # time.sleep(2)
                    if result_exocad == False:
                        with open(file_false_path, 'r', encoding='utf-8') as fi:
                            existing_contents_false = fi.read().splitlines()
                        if file not in existing_contents_false:
                            with open(file_false_path, 'a') as fi:
                                fi.write(file + '\n')
                    elif result_exocad == True:
                        with open(file_true_path, 'r', encoding='utf-8') as f:
                            existing_contents_true = f.read().splitlines()
                        if file not in existing_contents_true:
                            with open(file_true_path, 'a') as f:
                                f.write(file + '\n')
                    continue


            time.sleep(15)
            pyautogui.click(x=253, y=616, clicks=1, button='left')  # 点击文本输入框
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("backspace")
            time.sleep(2)
            upperpath = os.path.join(source_dir, file, file + "-UpperJaw.stl")
            pyperclip.copy(upperpath)
            print(upperpath)
            time.sleep(1)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(2)
            pyautogui.click(x=1030, y=685, clicks=1, button='left')  # 保存文件
            # pyautogui.click(x=point1[0], y=point1[1], clicks=1, button='left')  # 保存文件
            time.sleep(1)
            pyautogui.hotkey("y")  # 是否替换已存在的数据
            time.sleep(1)
            pyautogui.click(1237, 680)
            time.sleep(1)
            # pyautogui.click(x=point1[0]+80, y=point1[1], clicks=1, button='left')
            result_exocad = True

            time.sleep(2)
            subprocess.call("TASKKILL /IM DentalDB.exe")
            subprocess.call("TASKKILL /IM DentalCADApp.exe")
            time.sleep(1)
            # check_close_windows()
            # time.sleep(2)
            if result_exocad == False:
                with open(file_false_path, 'r', encoding='utf-8') as fi:
                    existing_contents_false = fi.read().splitlines()
                if file not in existing_contents_false:
                    with open(file_false_path, 'a') as fi:
                        fi.write(file + '\n')
            elif result_exocad == True:
                with open(file_true_path, 'r', encoding='utf-8') as f:
                    existing_contents_true = f.read().splitlines()
                if file not in existing_contents_true:
                    with open(file_true_path, 'a') as f:
                        f.write(file + '\n')


def get_box_point(boxes):
    for box in boxes:
        print(box[0], box[1])
        pyautogui.click(x=box[0], y=box[1], clicks=1, button='right', duration=1)  # 点击牙冠
        time.sleep(2)
        save_point = None
        region = (int(box[0]), int(box[1]), 1200, 1200)
        save_img = pyautogui.screenshot(region=region)
        img_array = np.array(save_img)
        result = reader.readtext(img_array)
        for detection in result:
            text = detection[1]
            if text == "保存到文件":
                print(text)
                corrdinates = detection[0]
                save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                save_point = (save_x, save_y)
                break
        time.sleep(1)
        if save_point == None:
            print("savae_point:", save_point)
        else:
            x = box[0] + save_point[0]
            y = box[1] + save_point[1]
            pyautogui.click(x=x, y=y, clicks=1, button='left')  # 点击save to file
            time.sleep(10)
            pyautogui.click(x=1030, y=685, clicks=1, button='left')  # 保存文件
            time.sleep(2)
            pyautogui.hotkey("y")
            time.sleep(2)
            pyautogui.click(x=1270, y=670, clicks=1, button='left')


def click_toothmesh_with_box(mesh_path):
    mesh = cv2.imread(mesh_path)
    image = cv2.cvtColor(np.array(mesh), cv2.COLOR_RGB2BGR)  # 将截图转为Opencv 支持的格式

    # 定义黄色范围
    con_point = None
    lower_yellow = np.array([150, 130, 100])
    upper_yellow = np.array([255, 215, 162])
    # 创建二值图像
    mask = cv2.inRange(image, lower_yellow, upper_yellow)
    _, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary2 = cv2.erode(binary, (120, 120), iterations=40)
    white_coords = np.where(binary2 == 255)
    if white_coords[0].size > 0:
        num_white_points = len(white_coords[0])
        print("白色区域长度：", num_white_points)
        start_index = num_white_points // 3
        print("1/3的索引起始处：", start_index)
        for idx in range(start_index, num_white_points):
            y, x = white_coords[0][idx], white_coords[1][idx]
            con_point = (x, y)
            print("白色像素点坐标：", con_point)
            break

        pyautogui.click(x=con_point[0], y=con_point[1], clicks=1, button='right', duration=1)  # 点击牙颌
        print(111111111)

        time.sleep(1)
        region = (int(con_point[0]), int(con_point[1]), 1200, 1200)
        save_img = pyautogui.screenshot(region=region)
        img_array = np.array(save_img)
        save_point = None

        result = reader.readtext(img_array)
        for detection in result:
            text = detection[1]
            if "保存" in text:
                print(text)
                corrdinates = detection[0]
                save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                save_point = (save_x, save_y)
                break

        # time.sleep(2)
        if save_point == None:
            print("未识别到保存文件这个按钮")
            return False
        else:
            pyautogui.click(x=con_point[0] + save_point[0], y=con_point[1] + save_point[1], clicks=1,
                            button='left')  # 点击保存到文件
            return True

    else:
        print("未找到白色像素的点")
        return False


def click_toothmesh(region):
    screenshot = pyautogui.screenshot(region=region)
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # 将截图转为Opencv支持的格式
    # 创建二值图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像

    # 使用阈值化方法来分割背景
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary2 = cv2.erode(binary, (120, 120), iterations=40)
    con_point = None
    white_coords = np.where(binary2 == 255)
    if white_coords[0].size > 0:
        num_white_points = len(white_coords[0])
        print("白色区域长度：", num_white_points)
        start_index = num_white_points // 3
        print("1/3的索引起始处：", start_index)
        for idx in range(start_index, num_white_points):
            y, x = white_coords[0][idx], white_coords[1][idx]
            con_point = (x + 350, y + 100)
            print("白色像素点坐标：", con_point)
            break
            # 选中mesh
        pyautogui.click(x=con_point[0], y=con_point[1], clicks=1, button='right', duration=1)  # 点击牙颌
        print(22222222222222222222222)

        time.sleep(1)
        region = (int(con_point[0]), int(con_point[1]), 1200, 1200)
        save_img = pyautogui.screenshot(region=region)
        img_array = np.array(save_img)
        save_point = None

        result = reader.readtext(img_array)
        for detection in result:
            text = detection[1]
            if "保存" in text:
                print(text)
                corrdinates = detection[0]
                save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                save_point = (save_x, save_y)
                break

        # time.sleep(2)
        if save_point == None:
            print("未识别到保存文件这个按钮")
            return False
        else:
            pyautogui.click(x=con_point[0] + save_point[0], y=con_point[1] + save_point[1], clicks=1,
                            button='left')  # 点击保存到文件
            return True

    else:
        print("未找到白色像素的点")
        return False


def identify_exist_crown(mehspath):
    mesh = cv2.imread(mehspath)
    image = cv2.cvtColor(np.array(mesh), cv2.COLOR_RGB2BGR)  # 将截图转为Opencv支持的格式

    # 定义黄色范围
    lower_yellow = np.array([150, 130, 100])
    upper_yellow = np.array([255, 215, 162])
    # 创建二值图像
    mask = cv2.inRange(image, lower_yellow, upper_yellow)
    _, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary2 = cv2.erode(binary, (120, 120), iterations=40)
    white_coords = np.where(binary2 == 255)
    if white_coords[0].size > 0:
        return True
    else:
        return False


# def wait_for_condition(timeout=30, interval=5):
#     '''每隔interval秒调用检查函数'''
#     elapsed = 0
#     while elapsed < timeout:
#         result,point = check_window_open()
#         if result == True:
#             print("检测到保存文件的窗口弹出")
#             return (True, point)
#         else:
#             print("未检测到保存文件的窗口弹出")
#             time.sleep(interval)
#             elapsed += interval
#     print("超过30秒都未检测到窗口弹出")
#     return (False, None)
#
#
# def check_window_open():
#     region_img = (350, 373, 1200, 800)
#     save_img = pyautogui.screenshot(region=region_img)
#     img_array = np.array(save_img)
#     # save_point = None
#
#     result = reader.readtext(img_array)
#     print(result)
#     for detection in result:
#         text = detection[1]
#         if text == "保存":
#             print(text)
#             corrdinates = detection[0]
#             save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
#             save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
#             save_point = (save_x + 350, save_y + 373)
#             print(save_point)
#             return (True, save_point)
#     return (False, None)
#
#
# def check_close_windows():
#     region = (763,434,1740,1113)
#     close_img = pyautogui.screenshot(region=region)
#     img_array = np.array(close_img)
#     close_point = None
#
#     result = reader.readtext(img_array)
#     for detection in result:
#         text = detection[1]
#         if (text == "不保存") or (text == "不保存场景文件"):
#             print(text)
#             corrdinates = detection[0]
#             close_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
#             close_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
#             close_point = (close_x+763, close_y+434)
#             print(close_point)
#             break
#
#     if close_point  == None:
#         print("未识别到不保存or不保存到场景文件这个按钮")
#         # return False
#     else:
#         pyautogui.click(x=close_point[0], y=close_point[1], clicks=1, button='left')  # 点击不保存场景文件



if __name__ == '__main__':
    main()
