import os
import shutil
import subprocess
import time
import cv2
import pyautogui
import sys

import pyperclip
import numpy as np
from crown_detect import CrownDetect
import easyocr



result_exocad = None
reader = easyocr.Reader(['ch_sim'])

def main():
    DentalDB_path = "D:/exocad-DentalCAD3.2-2024-02-14/exocad-DentalCAD3.2-2024-02-14/DentalDB/bin/DentalDB.exe"
    source_dir = r"D:\test_data\need-test"
    iamges_true_path= os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir)+ "_true_images")
    iamges_false_path = os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir) + "_false_images")
    file_true_path = os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir) + "_true.txt")
    file_false_path = os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir) + "_false.txt") # 存放导出失败的数据
    file_throw_path = os.path.join(os.path.dirname(source_dir), os.path.basename(source_dir) + "_throw.txt") # 存放不要的数据

    if not os.path.exists(iamges_true_path):
        os.makedirs(iamges_true_path)
    if not os.path.exists(iamges_false_path):
        os.makedirs(iamges_false_path)

    detector = CrownDetect(r"crown_detect.pt")
    global result_exocad

    # with open(txt_path, 'r', encoding='utf-8') as f:
    #     existing_contents_vis = f.read().splitlines()
    # if file not in existing_contents_vis:
    #     with open(txt_path, 'a') as f:
    #         f.write(file + '\n')


    for file in os.listdir(source_dir):
        with open(file_true_path, 'r', encoding='utf-8') as f:
            existing_true = f.read().splitlines() # 打开true.txt
        with open(file_false_path, 'r', encoding='utf-8') as fi:
            existing_false= fi.read().splitlines() # 打开false.txt
        if (file not in existing_true) and (file not in existing_false):
            time.sleep(5)
            pro = subprocess.Popen(DentalDB_path)  # 启动软件
            parent_pid = pro.pid
            print("parent_pid:", parent_pid)
            file_path = os.path.join(source_dir, file, file + ".dentalProject")
            print(file_path)
            time.sleep(16)

            # pyautogui.hotkey("ctrl", "l")  #Load
            pyautogui.click(790, 57) #Load
            time.sleep(3)
            pyautogui.click(143,1271) #exocad project
            time.sleep(3)
            pyautogui.click(900,657)   #点击路径输入框
            time.sleep(1)
            pyperclip.copy(file_path)
            print(file_path)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(2)
            pyautogui.hotkey("enter")
            time.sleep(2)

            pyautogui.click(1145,610)
            time.sleep(1)
            pyautogui.click(1145,930)
            time.sleep(1)

            region_img = (975,540,1000,1000)
            save_img = pyautogui.screenshot(region=region_img)
            img_array = np.array(save_img)

            result = reader.readtext(img_array)
            sure_point = None
            for detection in result:
                text = detection[1]
                if ("确定" in text) or ("是" in text):
                    print(text)
                    corrdinates = detection[0]
                    save_x = int((corrdinates[


                                       0][0] + corrdinates[2][0]) / 2)
                    save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                    sure_point = (save_x+975, save_y+540)
                    break
            if sure_point != None:
                # time.sleep(2)
                pyautogui.click(x=sure_point[0], y=sure_point[1], clicks=1, button='left')  # 点击确定

            time.sleep(2)
            pyautogui.click(1397,1423) # 点击确定

            time.sleep(2)
            pyautogui.hotkey("enter")

            time.sleep(2)

            pyautogui.doubleClick(2135,183)   # Design设计
            time.sleep(15)
            pyautogui.hotkey("enter")
            time.sleep(2)

            #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            #----------------------------------------------------------------------------------第一界面和第二界面分界线-------------------------------------------------------------------------------------------------
            #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            # 全屏显示
            pyautogui.click(1170, 835)
            time.sleep(1)
            pyautogui.hotkey("win", "up")
            time.sleep(1)

            if not detect_in_region_and_exit():
                print("退出操作，填入到throw.txt中")
                with open(file_throw_path, 'r', encoding='utf-8') as fi:
                    existing_contents_throw = fi.read().splitlines()
                if file not in existing_contents_throw:
                    with open(file_throw_path, 'a') as fi:
                        fi.write(file + '\n')
                

            else:
                if detect_bridge_type() == "bridge":
                    # 牙桥
                    print("检测到牙桥类型，开始处理桥体...")
                    save_bridge_components(file, source_dir, iamges_true_path, iamges_false_path, file_true_path, file_false_path)                                    


                else:
                    # 单冠
                    time.sleep(1)
                    pyautogui.click(1535, 855)
                    time.sleep(1)

                    region = (0, 0, 1000, 1000)
                    save_img = pyautogui.screenshot(region=region)
                    img_array = np.array(save_img)

                    result = reader.readtext(img_array)
                    for detection in result:
                        text = detection[1]
                        if "全部" in text:
                            corrdinates = detection[0]
                            save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                            save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                            # 隐藏所有对象
                            pyautogui.keyDown("ctrl")
                            pyautogui.click(x=save_x, y=save_y)
                            pyautogui.keyUp("ctrl")
                            time.sleep(1)
                            break

                    pyautogui.click(272, 705)
                    time.sleep(1)
                    pyautogui.hotkey("a")  # 对颌
                    print(1111111111111111)
                    time.sleep(1)
                    pyautogui.hotkey("s")  # 工作模型扫描
                    print(2222222222222222)
                    time.sleep(2)
                    pyautogui.hotkey("m")
                    print(3333333333333333)
                    time.sleep(2)
                    pyautogui.hotkey("e")
                    print(4444444444444444)


                    time.sleep(2)
                    print(555555555555555555555)
                    pyautogui.click(x=2500,y=1363,clicks=1,button='left') #模型显示到正中心
                    time.sleep(2)

                    #   下颌牙冠
                    # time.sleep(4)
                    pyautogui.click(2500,1325)    #下颌视角
                    time.sleep(3)
                    lowtoothmesh_path = pyautogui.screenshot()
                    pngnamelow = os.path.join(iamges_true_path, file + "-LowerJaw.png")
                    print(pngnamelow)
                    lowtoothmesh_path.save(pngnamelow)

                    time.sleep(1)
                    region_low = (350, 100, 1750, 1200)

                    # 获取牙冠并保存
                    result = identify_exist_crown(pngnamelow)            # 判断是黄色还是灰色，看牙颌中是否存在冠
                    boxes = detector.process(lowtoothmesh_path)          #读取图片
                    print(boxes)
                    if result == True and len(boxes)>0:
                        print("下颌box",boxes)
                        get_box_point(boxes)

                        # 保存下颌mesh
                        time.sleep(3)
                        result = click_toothmesh_with_box(pngnamelow)
                        if result == False:
                            os.remove(pngnamelow)
                            pngfalselow = os.path.join(iamges_false_path, file + "-LowerJaw.png")
                            lowtoothmesh_path.save(pngfalselow)
                            result_exocad = False

                            time.sleep(1)
                            subprocess.call("TASKKILL /IM DentalDB.exe")
                            subprocess.call("TASKKILL /IM DentalCADApp.exe")
                            time.sleep(1)
                            check_close_windows()
                            time.sleep(1)
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

                            time.sleep(1)
                            subprocess.call("TASKKILL /IM DentalDB.exe")
                            subprocess.call("TASKKILL /IM DentalCADApp.exe")
                            time.sleep(1)
                            check_close_windows()
                            time.sleep(1)
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


                    # 检查保存窗口是否弹出
                    time.sleep(5)
                    wait_result, point = wait_for_condition()
                    if not wait_result:
                        result_exocad = False
                        subprocess.call("TASKKILL /IM DentalCADApp.exe")
                        time.sleep(1)
                        check_close_windows()
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
                    else:
                        pyautogui.click(x=point[0], y=point[1]-70, clicks=1, button='left')  # 保存文件
                        pyautogui.hotkey("ctrl", "a")
                        pyautogui.hotkey("backspace")
                        time.sleep(1)
                        lowerpath = os.path.join(source_dir, file, file + "-LowerJaw.stl")
                        pyperclip.copy(lowerpath)
                        print(lowerpath)
                        time.sleep(1)
                        pyautogui.hotkey("ctrl", "v")
                        time.sleep(1)
                        # pyautogui.click(x=1030,y=680,clicks=1,button='left')  # 保存文件
                        pyautogui.click(x=point[0], y=point[1], clicks=1, button='left')  # 保存文件
                        time.sleep(2)
                        pyautogui.hotkey("y")  # 是否替换已存在的数据
                        time.sleep(1)
                        pyautogui.click(x=1237, y=680, clicks=1,button='left')
                        time.sleep(1)
                        pyautogui.click(x=point[0] + 80, y=point[1], clicks=1, button='left')  # 避免窗口还存在,点击取消
                        time.sleep(1)
                        result_exocad = True

                        time.sleep(1)



                        #上颌牙冠
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

                                time.sleep(1)
                                subprocess.call("TASKKILL /IM DentalDB.exe")
                                subprocess.call("TASKKILL /IM DentalCADApp.exe")
                                time.sleep(1)
                                check_close_windows()
                                time.sleep(1)
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
                            # else:
                            #     de_filePath = os.path.join(file_true_path, file)
                            #     if os.path.exists(de_filePath):
                            #         shutil.rmtree(de_filePath)
                            #     shutil.copytree(filePath, de_filePath)


                        else:
                            result = click_toothmesh(region_upp)
                            if result == False:
                                os.remove(pngnameupp)
                                pngfalseupp = os.path.join(iamges_false_path, file + "-UpperJaw.png")
                                upptoothmesh_path.save(pngfalseupp)
                                result_exocad = False

                                time.sleep(1)
                                subprocess.call("TASKKILL /IM DentalDB.exe")
                                subprocess.call("TASKKILL /IM DentalCADApp.exe")
                                time.sleep(1)
                                check_close_windows()

                                time.sleep(1)
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
                            # else:
                            #     de_filePath = os.path.join(file_true_path, file)
                            #     if os.path.exists(de_filePath):
                            #         shutil.rmtree(de_filePath)
                            #     shutil.copytree(filePath, de_filePath)
                        time.sleep(5)
                        wait_result1, point1 = wait_for_condition()
                        if not wait_result1:
                            result_exocad = False
                            subprocess.call("TASKKILL /IM DentalDB.exe")
                            subprocess.call("TASKKILL /IM DentalCADApp.exe")
                            time.sleep(1)
                            check_close_windows()
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
                        else:
                            # pyautogui.click(x=253, y=616, clicks=1, button='left')  # 点击文本输入框
                            pyautogui.click(x=point1[0], y=point1[1]-70, clicks=1, button='left')  # 保存文件
                            pyautogui.hotkey("ctrl", "a")
                            pyautogui.hotkey("backspace")
                            time.sleep(1)
                            upperpath = os.path.join(source_dir, file, file + "-UpperJaw.stl")
                            pyperclip.copy(upperpath)
                            print(upperpath)
                            time.sleep(1)
                            pyautogui.hotkey("ctrl", "v")
                            time.sleep(1)
                            # pyautogui.click(x=1030, y=685, clicks=1, button='left')  # 保存文件
                            pyautogui.click(x=point1[0], y=point1[1], clicks=1, button='left')  # 保存文件
                            time.sleep(1)
                            pyautogui.hotkey("y")  # 是否替换已存在的数据
                            time.sleep(1)
                            pyautogui.click(1237, 680)
                            time.sleep(1)
                            pyautogui.click(x=point1[0] + 80, y=point1[1], clicks=1, button='left')
                            result_exocad = True

                            time.sleep(2)
                            subprocess.call("TASKKILL /IM DentalDB.exe")
                            subprocess.call("TASKKILL /IM DentalCADApp.exe")
                            time.sleep(1)
                            check_close_windows()


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
        pyautogui.click(x=box[0], y=box[1], clicks=1,button='right',duration=1)  # 点击牙冠
        time.sleep(2)
        save_point = None
        region = (int(box[0]), int(box[1]), 1200, 1200)
        save_img = pyautogui.screenshot(region=region)
        img_array = np.array(save_img)
        result = reader.readtext(img_array)
        for detection in result:
            text = detection[1]
            if "保存" in text:
                print(text)
                corrdinates = detection[0]
                save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                save_point = (save_x,save_y)
                break
        time.sleep(1)
        if save_point == None:
            print("savae_point:", save_point)
        else:
            x = box[0] + save_point[0]
            y = box[1] + save_point[1]
            pyautogui.click(x=x, y=y, clicks=1,button='left')  # 点击save to file
            time.sleep(10)

            # pyautogui.click(x=1030, y=685, clicks=1, button='left')  # 保存文件
            pyautogui.click(x=1029, y=688, clicks=1, button='left')  # 保存文件
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
            y,x = white_coords[0][idx], white_coords[1][idx]
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
                save_point=(save_x,save_y)
                break

        # time.sleep(2)
        if save_point == None:
            print("未识别到保存文件这个按钮")
            return False
        else:
            pyautogui.click(x=con_point[0] + save_point[0], y=con_point[1] + save_point[1], clicks=1, button='left')  # 点击保存到文件
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
            con_point = (x+350, y+100)
            print("白色像素点坐标：", con_point)
            break
            #选中mesh
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
                save_point=(save_x,save_y)
                break

        # time.sleep(2)
        if save_point  == None:
            print("未识别到保存文件这个按钮")
            return False
        else:
            pyautogui.click(x=con_point[0] + save_point[0], y=con_point[1] + save_point[1], clicks=1, button='left')  # 点击保存到文件
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

def wait_for_condition(timeout=30, interval=5):
    '''每隔interval秒调用检查函数'''
    elapsed = 0
    while elapsed < timeout:
        result,point = check_window_open()
        if result == True:
            print("检测到保存文件的窗口弹出")
            return (True,point)
        else:
            print("未检测到保存文件的窗口弹出")
            time.sleep(interval)
            elapsed += interval
    print("超过30秒都未检测到窗口弹出")
    return (False,None)


def check_window_open():
    region_img = (110, 260, 1200, 900)

    save_img = pyautogui.screenshot(region=region_img)
    img_array = np.array(save_img)
    pngfalseupp = "D:/exocad-data/1.png"
    save_img.save(pngfalseupp)
    # save_point = None

    result = reader.readtext(img_array)
    print(result)
    for detection in result:
        text = detection[1]
        if "保存" in text:
            print(text)
            corrdinates = detection[0]
            save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
            save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
            save_point = (save_x + 110, save_y + 260)
            print(save_point)
            return (True, save_point)
    return (False, None)


def check_close_windows():
    region = (763,434,1740,1113)
    close_img = pyautogui.screenshot(region=region)
    img_array = np.array(close_img)
    close_point = None

    result = reader.readtext(img_array)
    for detection in result:
        text = detection[1]
        if (text == "不保存") or (text == "不保存场景文件"):
            print(text)
            corrdinates = detection[0]
            close_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
            close_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
            close_point = (close_x+763, close_y+434)
            print(close_point)
            break

    if close_point  == None:
        print("未识别到不保存or不保存到场景文件这个按钮")
        # return False
    else:
        pyautogui.click(x=close_point[0], y=close_point[1], clicks=1, button='left')  # 点击不保存场景文件


def perform_original_exit():
    # 退出
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
    sys.exit()

def detect_in_region_and_exit():
    # 关键字列表
    # EXIT_KEYWORDS = ['牙龈扫描', '回切部分', '螺丝', '基台', '贴面', '嵌体']
    # 合并部分关键词
    MERGE_KEYWORD = '合并部分'

    # 定义各区域坐标
    HIDE_REGION = (20, 273, 91 - 20, 376 - 273)         # 原“隐藏”按钮区域
    EXPAND_REGION = (18, 15, 280 - 18, 841 - 15)        # 展开后检测区域


    # 1. 点击“隐藏”按钮
    hide_x, hide_y, hide_w, hide_h = HIDE_REGION
    hide_img = np.array(pyautogui.screenshot(region=HIDE_REGION))
    results = reader.readtext(hide_img)
    print("OCR result:", results)
    for bbox, text, _ in results:
        if '隐' in text:
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
    # for kw in EXIT_KEYWORDS:
    #     if any(kw in t for t in texts):
    #         print(f"检测到退出关键词 '{kw}'，关闭当前 Exocad 会话。")
    #         subprocess.call(["TASKKILL", "/IM", "DentalDB.exe", "/F"])
    #         subprocess.call(["TASKKILL", "/IM", "DentalCADApp.exe", "/F"])
    #         return False

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


def detect_anatomical_morphology():
    keyword = "解剖形态"
    hide_region = (18, 15, 280 - 18, 284 - 15)
    hide_x, hide_y, hide_w, hide_h = hide_region
    hide_img = np.array(pyautogui.screenshot(region=hide_region))
    results = reader.readtext(hide_img)
    print("OCR result:", results)
    for bbox, text, _ in results:
        if '解剖形态' in text:
            xs = [pt[0] for pt in bbox]
            ys = [pt[1] for pt in bbox]
            cx = int(sum(xs)/4) + hide_x
            cy = int(sum(ys)/4) + hide_y
            return True

    return False




def detect_bridge_type():
    X0_BRIDGE, Y0_BRIDGE = 18, 15
    W_BRIDGE, H_BRIDGE = 280 - X0_BRIDGE, 284 - Y0_BRIDGE

    BRIDGE_KEYWORD = '连接杆'
    img = np.array(pyautogui.screenshot(region=(X0_BRIDGE, Y0_BRIDGE, W_BRIDGE, H_BRIDGE)))
    results = reader.readtext(img)
    texts = [text for _, text, _ in results]
    if any(BRIDGE_KEYWORD in t for t in texts):
        print("检测到 '连接杆'，判定为牙桥（Bridge）。")
        return 'bridge'
    else:
        print("未检测到 '连接杆'，判定为单冠（Single Crown）。")
        return 'single'


def save_bridge_components(file, source_dir, iamges_true_path, iamges_false_path, file_true_path, file_false_path):
    """
    保存牙桥组件的函数
    """
    global result_exocad
    
    print("开始处理牙桥组件...")
    
    print("开始处理下颌...")

    # 切换到下颌视角
    pyautogui.click(2500, 1325)  # 下颌视角
    time.sleep(3)

    # 保存下颌图片
    # lowtoothmesh_path = pyautogui.screenshot()
    # pngnamelow = os.path.join(iamges_true_path, file + "-LowerJaw.png")
    # print(pngnamelow)
    # lowtoothmesh_path.save(pngnamelow)
    

    pyautogui.hotkey("a")  # 对颌
    time.sleep(1)
    pyautogui.hotkey("s")  
    time.sleep(2)
    
    # 截取下颌第一张图
    screenshot_before = pyautogui.screenshot()
    png_before = os.path.join(iamges_true_path, file + "-BeforeBridge_LowerJaw.png")
    screenshot_before.save(png_before)
    

    pyautogui.hotkey("m")  # 显示桥体合并部分
    time.sleep(3)
    
    # 截取第二张图
    screenshot_after = pyautogui.screenshot()
    png_after = os.path.join(iamges_true_path, file + "-AfterBridge_LowerJaw.png")
    screenshot_after.save(png_after)
    
    
    bridge_centers = find_all_bridge_centers(png_before, png_after) # 比对两张图片，找到所有桥体位置
    
    if bridge_centers:
        print(f"找到 {len(bridge_centers)} 个桥体组件")
        
        success_count = 0
        for i, bridge_center in enumerate(bridge_centers):
            print(f"处理第 {i+1} 个桥体组件，位置: {bridge_center}")
            
            # 点击桥体中心位置
            pyautogui.click(x=bridge_center[0], y=bridge_center[1], clicks=1, button='right', duration=1)
            time.sleep(2)
            
            # 查找并点击保存选项
            region = (bridge_center[0], bridge_center[1], 1200, 1200)
            save_img = pyautogui.screenshot(region=region)
            img_array = np.array(save_img)
            result = reader.readtext(img_array)
            
            save_point = None
            for detection in result:
                text = detection[1]
                if "保存" in text:
                    print(f"找到保存选项: {text}")
                    corrdinates = detection[0]
                    save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                    save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                    save_point = (save_x, save_y)
                    break
            
            if save_point:
                # 点击保存到文件
                pyautogui.click(x=bridge_center[0] + save_point[0], y=bridge_center[1] + save_point[1], clicks=1, button='left')
                time.sleep(10)
                
                # 等待保存窗口弹出
                wait_result, point = wait_for_condition()
                if wait_result:
                    # 填写保存路径
                    pyautogui.click(x=point[0], y=point[1]-70, clicks=1, button='left')
                    pyautogui.hotkey("ctrl", "a")
                    pyautogui.hotkey("backspace")
                    time.sleep(1)
                    
                    bridge_path = os.path.join(source_dir, file, file + "-bridge_slm_cad.stl")
                    pyperclip.copy(bridge_path)
                    print(f"保存桥体到: {bridge_path}")
                    time.sleep(1)
                    pyautogui.hotkey("ctrl", "v")
                    time.sleep(1)
                    
                    # 点击保存按钮
                    pyautogui.click(x=point[0], y=point[1], clicks=1, button='left')
                    time.sleep(2)
                    pyautogui.hotkey("y")  # 确认替换
                    time.sleep(1)
                    pyautogui.click(x=point[0] + 80, y=point[1], clicks=1, button='left')  # 点击取消
                    time.sleep(1)
                    
                    success_count += 1
                    print(f"第 {i+1} 个桥体保存成功")
                else:
                    print(f"第 {i+1} 个桥体保存窗口未弹出")
            else:
                print(f"第 {i+1} 个桥体未找到保存选项")


    print("开始处理上颌...")

    pyautogui.click(2500, 1395)  # 上颌视角
    time.sleep(3)

    # 保存上颌图片
    # lowtoothmesh_path = pyautogui.screenshot()
    # pngnamelow = os.path.join(iamges_true_path, file + "-UpperJaw.png")
    # print(pngnamelow)
    # lowtoothmesh_path.save(pngnamelow)

    pyautogui.hotkey("m")  # 消除桥体合并部分
    time.sleep(3)

    # 截取上颌第一张图
    screenshot_before = pyautogui.screenshot()
    png_before = os.path.join(iamges_true_path, file + "-BeforeBridge_UpperJaw.png")
    screenshot_before.save(png_before)
    

    pyautogui.hotkey("m")  # 显示桥体合并部分
    time.sleep(3)
    
    # 截取第二张图
    screenshot_after = pyautogui.screenshot()
    png_after = os.path.join(iamges_true_path, file + "-AfterBridge_UpperJaw.png")
    screenshot_after.save(png_after)
    
    
    bridge_centers = find_all_bridge_centers(png_before, png_after) # 比对两张图片，找到所有桥体位置
    
    if bridge_centers:
        print(f"找到 {len(bridge_centers)} 个桥体组件")
        
        success_count = 0
        for i, bridge_center in enumerate(bridge_centers):
            print(f"处理第 {i+1} 个桥体组件，位置: {bridge_center}")
            
            # 点击桥体中心位置
            pyautogui.click(x=bridge_center[0], y=bridge_center[1], clicks=1, button='right', duration=1)
            time.sleep(2)
            
            # 查找并点击保存选项
            region = (bridge_center[0], bridge_center[1], 1200, 1200)
            save_img = pyautogui.screenshot(region=region)
            img_array = np.array(save_img)
            result = reader.readtext(img_array)
            
            save_point = None
            for detection in result:
                text = detection[1]
                if "保存" in text:
                    print(f"找到保存选项: {text}")
                    corrdinates = detection[0]
                    save_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                    save_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                    save_point = (save_x, save_y)
                    break
            
            if save_point:
                # 点击保存到文件
                pyautogui.click(x=bridge_center[0] + save_point[0], y=bridge_center[1] + save_point[1], clicks=1, button='left')
                time.sleep(10)
                
                # 等待保存窗口弹出
                wait_result, point = wait_for_condition()
                if wait_result:
                    # 填写保存路径
                    pyautogui.click(x=point[0], y=point[1]-70, clicks=1, button='left')
                    pyautogui.hotkey("ctrl", "a")
                    pyautogui.hotkey("backspace")
                    time.sleep(1)
                    
                    bridge_path = os.path.join(source_dir, file, file + "-bridge_slm_cad.stl")
                    pyperclip.copy(bridge_path)
                    print(f"保存桥体到: {bridge_path}")
                    time.sleep(1)
                    pyautogui.hotkey("ctrl", "v")
                    time.sleep(1)
                    
                    # 点击保存按钮
                    pyautogui.click(x=point[0], y=point[1], clicks=1, button='left')
                    time.sleep(2)
                    pyautogui.hotkey("y")  # 确认替换
                    time.sleep(1)
                    pyautogui.click(x=point[0] + 80, y=point[1], clicks=1, button='left')  # 点击取消
                    time.sleep(1)
                    
                    success_count += 1
                    print(f"第 {i+1} 个桥体保存成功")
                else:
                    print(f"第 {i+1} 个桥体保存窗口未弹出")
            else:
                print(f"第 {i+1} 个桥体未找到保存选项")

        
        if success_count > 0:
            result_exocad = True
            print(f"成功保存 {success_count} 个桥体组件")
        else:
            result_exocad = False
            print("所有桥体组件保存失败")
    else:
        print("未找到桥体中心位置")
        result_exocad = False
  
  
    # 保存下颌本身
    print("开始保存下颌本身...")

    pyautogui.click(2500, 1325) # 下颌视角
    time.sleep(3)

    # 截取下颌截图
    lowtoothmesh_path = pyautogui.screenshot()
    pngnamelow = os.path.join(iamges_true_path, file + "-LowerJaw.png")
    lowtoothmesh_path.save(pngnamelow)

    time.sleep(1)
    region_low = (350, 100, 1750, 1200)

    # 获取下颌并保存
    result = identify_exist_crown(pngnamelow) # 判断是否存在冠
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
        else:
            # 检查保存窗口是否弹出
            time.sleep(5)
            wait_result, point = wait_for_condition()
            if not wait_result:
                result_exocad = False
            else:
                pyautogui.click(x=point[0], y=point[1]-70, clicks=1, button='left') # 保存文件
                pyautogui.hotkey("ctrl", "a")
                pyautogui.hotkey("backspace")
                time.sleep(1)
                lowerpath = os.path.join(source_dir, file, file + "-LowerJaw.stl")
                pyperclip.copy(lowerpath)
                print(lowerpath)
                time.sleep(1)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(1)
                pyautogui.click(x=point[0], y=point[1], clicks=1, button='left') # 保存文件
                time.sleep(2)
                pyautogui.hotkey("y") # 是否替换已存在的数据
                time.sleep(1)
                pyautogui.click(x=1237, y=680, clicks=1, button='left')
                time.sleep(1)
                pyautogui.click(x=point[0] + 80, y=point[1], clicks=1, button='left') # 避免窗口还存在,点击取消
                time.sleep(1)
                result_exocad = True
                print("下颌保存完成。")     
    else:
        result = click_toothmesh(region_low)
        if result == False:
            os.remove(pngnamelow)
            pngfalselow = os.path.join(iamges_false_path, file + "-LowerJaw.png")
            lowtoothmesh_path.save(pngfalselow)
            result_exocad = False
        else:
            # 检查保存窗口是否弹出
            time.sleep(5)
            wait_result, point = wait_for_condition()
            if not wait_result:
                result_exocad = False
            else:
                pyautogui.click(x=point[0], y=point[1]-70, clicks=1, button='left') # 保存文件
                pyautogui.hotkey("ctrl", "a")
                pyautogui.hotkey("backspace")
                time.sleep(1)
                lowerpath = os.path.join(source_dir, file, file + "-LowerJaw.stl")
                pyperclip.copy(lowerpath)
                print(lowerpath)
                time.sleep(1)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(1)
                pyautogui.click(x=point[0], y=point[1], clicks=1, button='left') # 保存文件
                time.sleep(2)
                pyautogui.hotkey("y") # 是否替换已存在的数据
                time.sleep(1)
                pyautogui.click(x=1237, y=680, clicks=1, button='left')
                time.sleep(1)
                pyautogui.click(x=point[0] + 80, y=point[1], clicks=1, button='left') # 避免窗口还存在,点击取消
                time.sleep(1)
                result_exocad = True
                print("下颌保存成功")    




    
    
    # 保存上颌本身
    print("开始保存上颌本身...")

    pyautogui.click(2500, 1395) # 上颌视角
    time.sleep(3)

    # 截取上颌截图
    lowtoothmesh_path = pyautogui.screenshot()
    pngnamelow = os.path.join(iamges_true_path, file + "-UpperJaw.png")
    lowtoothmesh_path.save(pngnamelow)

    time.sleep(1)
    region_upp = (350, 100, 1750, 1200)

    # 获取上颌并保存
    result = identify_exist_crown(pngnamelow) # 判断是否存在冠
    boxes = detector.process(lowtoothmesh_path)
    print(boxes)

    if result == True and len(boxes) > 0:
        print("上颌box", boxes)
        get_box_point(boxes)
    
        # 保存上颌mesh
        time.sleep(3)
        result = click_toothmesh_with_box(pngnamelow)
        if result == False:
            os.remove(pngnamelow)
            pngfalselow = os.path.join(iamges_false_path, file + "-UpperJaw.png")
            lowtoothmesh_path.save(pngfalselow)
            result_exocad = False
        else:
            # 检查保存窗口是否弹出
            time.sleep(5)
            wait_result, point = wait_for_condition()
            if not wait_result:
                result_exocad = False
            else:
                pyautogui.click(x=point[0], y=point[1]-70, clicks=1, button='left') # 保存文件
                pyautogui.hotkey("ctrl", "a")
                pyautogui.hotkey("backspace")
                time.sleep(1)
                lowerpath = os.path.join(source_dir, file, file + "-UpperJaw.stl")
                pyperclip.copy(lowerpath)
                print(lowerpath)
                time.sleep(1)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(1)
                pyautogui.click(x=point[0], y=point[1], clicks=1, button='left') # 保存文件
                time.sleep(2)
                pyautogui.hotkey("y") # 是否替换已存在的数据
                time.sleep(1)
                pyautogui.click(x=1237, y=680, clicks=1, button='left')
                time.sleep(1)
                pyautogui.click(x=point[0] + 80, y=point[1], clicks=1, button='left') # 避免窗口还存在,点击取消
                time.sleep(1)
                result_exocad = True
                print("上颌保存完成。")

    else:
        result = click_toothmesh(region_upp)
        if result == False:
            os.remove(pngnamelow)
            pngfalselow = os.path.join(iamges_false_path, file + "-UpperJaw.png")
            lowtoothmesh_path.save(pngfalselow)
            result_exocad = False
        else:
            # 检查保存窗口是否弹出
            time.sleep(5)
            wait_result, point = wait_for_condition()
            if not wait_result:
                result_exocad = False
            else:
                pyautogui.click(x=point[0], y=point[1]-70, clicks=1, button='left') # 保存文件
                pyautogui.hotkey("ctrl", "a")
                pyautogui.hotkey("backspace")
                time.sleep(1)
                lowerpath = os.path.join(source_dir, file, file + "-UpperJaw.stl")
                pyperclip.copy(lowerpath)
                print(lowerpath)
                time.sleep(1)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(1)
                pyautogui.click(x=point[0], y=point[1], clicks=1, button='left') # 保存文件
                time.sleep(2)
                pyautogui.hotkey("y") # 是否替换已存在的数据
                time.sleep(1)
                pyautogui.click(x=1237, y=680, clicks=1, button='left')
                time.sleep(1)
                pyautogui.click(x=point[0] + 80, y=point[1], clicks=1, button='left') # 避免窗口还存在,点击取消
                time.sleep(1)
                result_exocad = True
                print("上颌保存成功")   







    # 记录结果
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
    
    # 清理进程
    time.sleep(2)
    subprocess.call("TASKKILL /IM DentalDB.exe")
    subprocess.call("TASKKILL /IM DentalCADApp.exe")
    time.sleep(1)
    check_close_windows()


def find_bridge_center(before_image_path, after_image_path):
    """
    通过比对两张图片找到桥体中心位置
    """
    # 读取两张图片
    img_before = cv2.imread(before_image_path)
    img_after = cv2.imread(after_image_path)
    
    if img_before is None or img_after is None:
        print("无法读取图片文件")
        return None
    
    # 转换为灰度图
    gray_before = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    gray_after = cv2.cvtColor(img_after, cv2.COLOR_BGR2GRAY)
    
    # 计算差异
    diff = cv2.absdiff(gray_before, gray_after)
    
    # 应用阈值，突出差异区域
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    # 形态学操作，去除噪声
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # 保存差异图片用于调试
    diff_debug_path = before_image_path.replace("-BeforeBridge_", "-DiffDebug.png")
    cv2.imwrite(diff_debug_path, thresh)
    print(f"差异图片已保存到: {diff_debug_path}")
    
    # 查找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # 找到最大的轮廓（假设桥体是最大的新增区域）
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 计算轮廓的中心点
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            print(f"桥体中心位置: ({cx}, {cy})")
            
            # 在原图上标记中心点用于调试
            img_debug = cv2.imread(after_image_path)
            cv2.circle(img_debug, (cx, cy), 10, (0, 255, 0), -1)  # 绿色圆点
            debug_marked_path = after_image_path.replace("-AfterBridge_", "-MarkedCenter.png")
            cv2.imwrite(debug_marked_path, img_debug)
            print(f"标记中心点的图片已保存到: {debug_marked_path}")
            
            return (cx, cy)
    
    print("未找到明显的桥体区域")
    return None


def find_all_bridge_centers(before_image_path, after_image_path):
    """
    通过比对两张图片找到所有桥体中心位置
    """
    # 读取两张图片
    img_before = cv2.imread(before_image_path)
    img_after = cv2.imread(after_image_path)
    
    if img_before is None or img_after is None:
        print("无法读取图片文件")
        return []
    
    # 转换为灰度图
    gray_before = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    gray_after = cv2.cvtColor(img_after, cv2.COLOR_BGR2GRAY)
    
    # 计算差异
    diff = cv2.absdiff(gray_before, gray_after)
    
    # 应用阈值，突出差异区域
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    # 形态学操作，去除噪声
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # 保存差异图片用于调试
    diff_debug_path = before_image_path.replace("-BeforeBridge_", "-DiffDebug.png")
    cv2.imwrite(diff_debug_path, thresh)
    print(f"差异图片已保存到: {diff_debug_path}")
    
    # 查找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bridge_centers = []
    if contours:
        # 按面积排序轮廓，找到所有足够大的区域
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # 过滤掉太小的轮廓（噪声）
        min_area = 1000  # 最小面积阈值
        valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
        
        print(f"找到 {len(valid_contours)} 个有效的桥体区域")
        
        # 在原图上标记所有中心点用于调试
        img_debug = cv2.imread(after_image_path)
        
        for i, contour in enumerate(valid_contours):
            # 计算轮廓的中心点
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # 检查是否与已找到的中心点距离太近（避免重复）
                min_distance = 50  # 最小距离阈值
                too_close = False
                for existing_center in bridge_centers:
                    distance = ((cx - existing_center[0])**2 + (cy - existing_center[1])**2)**0.5
                    if distance < min_distance:
                        too_close = True
                        break
                
                if not too_close:
                    bridge_centers.append((cx, cy))
                    print(f"桥体 {i+1} 中心位置: ({cx}, {cy})")
                    
                    # 在调试图片上标记中心点
                    color = (0, 255, 0) if i == 0 else (255, 0, 0)  # 第一个绿色，其他红色
                    cv2.circle(img_debug, (cx, cy), 10, color, -1)
                    cv2.putText(img_debug, f"{i+1}", (cx+15, cy+5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # 保存标记了所有中心点的调试图片
        debug_marked_path = after_image_path.replace("-AfterBridge_", "-MarkedAllCenters.png")
        cv2.imwrite(debug_marked_path, img_debug)
        print(f"标记所有中心点的图片已保存到: {debug_marked_path}")
    
    if not bridge_centers:
        print("未找到明显的桥体区域")
    
    return bridge_centers





if __name__ == '__main__':
    main()
