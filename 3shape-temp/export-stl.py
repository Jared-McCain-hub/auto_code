import os
import shutil
import subprocess
import time
import cv2
import pyautogui
import pyperclip
import easyocr
import schedule
import numpy as np
from torchvision.models.video import mvit_v2_s

reader = easyocr.Reader(['ch_sim'])

def main():
    DentalManager_path = "C:/Program Files/3Shape/DentalManager/DentalManager.exe"
    source_dir = r"E:\3shape-2T-7-8#input"
    CAM_path = r"E:\ManufacturingDir"

    va_path = r"E:\Visualization output"
    while True:
        process = subprocess.Popen(DentalManager_path)  # 启动软件
        time.sleep(15)
        pyautogui.click(1280,795)
        time.sleep(2)
        pyautogui.hotkey("1")
        pyautogui.hotkey("2")
        pyautogui.hotkey("3")
        pyautogui.hotkey("4")
        pyautogui.hotkey("5")
        pyautogui.hotkey("6")
        time.sleep(10)

        txt_filepath = os.path.join(os.path.dirname(CAM_path), "3shape-2T-7-8#input.txt")
        error_path = os.path.join(os.path.dirname(va_path), os.path.basename(source_dir) + "_error")
        if not os.path.exists(error_path):
            os.makedirs(error_path)

        start_time = time.time()

        for file in os.listdir(source_dir):
            for xmlfile in os.listdir(os.path.join(source_dir, file)):
                if xmlfile.endswith('.xml') and xmlfile != "Materials.xml":
                    file_path = os.path.join(source_dir, file, xmlfile)
                    filename = xmlfile[0:-4]
                    txt_path = os.path.join(va_path,filename,f"{file}.txt")
                    if (not os.path.exists(os.path.join(va_path, filename)) and not os.path.exists(os.path.join(CAM_path, filename))
                            and  not os.path.exists(os.path.join(error_path, file))):
                        with open(txt_filepath, 'a') as f:
                            f.write(file + '\n')
                        time.sleep(3)

                        pyautogui.click(x=1990,y=605, clicks=1, button='right') # 右键
                        time.sleep(2)
                        pyautogui.hotkey("y")   #点击高级
                        time.sleep(1)
                        pyautogui.hotkey("z")     #点击导入
                        time.sleep(1)
                        pyautogui.click(x=1390,y=785, clicks=1, button='left')  #点击确定导入订单
                        time.sleep(8)
                        pyautogui.click(x=2190, y=1175, clicks=1, button='left')    #切换后缀为.xml
                        time.sleep(2)
                        pyautogui.click(x=2200, y=1220, clicks=1, button='left')  # 切换后缀为.xml
                        time.sleep(1)
                        pyautogui.click(x=1995, y=1180, clicks=1, button='left')  # 点击文本输入框
                        time.sleep(1)
                        pyperclip.copy(file_path)
                        print(file_path)
                        pyautogui.hotkey("ctrl", "v")
                        time.sleep(2)
                        pyautogui.hotkey("enter")
                        time.sleep(2)
                        pyautogui.click(1440,710)
                        time.sleep(1)
                        pyautogui.click(2270,490)
                        pyautogui.hotkey("enter")
                        time.sleep(1)
                        pyautogui.click(2270, 490)
                        pyautogui.hotkey("enter")
                        time.sleep(1)
                        pyautogui.click(2270, 490)
                        pyautogui.hotkey("enter")
                        time.sleep(1)
                        pyautogui.click(2270, 490)
                        pyautogui.hotkey("enter")
                        # 判断是否存在xml文件
                        return_result = get_xmlfile()
                        if return_result == True:
                            pyautogui.click(1432, 597)  # 对无法找到的订单点击确定
                            continue
                        else:

                            # time.sleep(2)

                            # image1 = (1100, 635, 300, 180)
                            # images_sure1 = pyautogui.screenshot(region=image1)
                            # array2 = np.array(images_sure1)
                            # cv2.imwrite("images_sure1.png", array2)
                            # sure_result1 = reader.readtext(array2)
                            # for txt in sure_result1:
                            #     sure_text = txt[1]
                            #     if sure_text == "确定":
                            time.sleep(5)
                            pyautogui.click(1280,735)  #对无法导入的订单点击确定
                            #         # 删除订单
                            #         # pyautogui.click(x=1560, y=135, clicks=1, button='right')  # 选中订单数据
                            #         # time.sleep(1)
                            #         # pyautogui.hotkey("s")  # 删除y
                            #         # time.sleep(2)
                            #         # # pyautogui.click(1830,450) # 删除订单
                            #         # pyautogui.hotkey("enter")
                            #         # time.sleep(2)
                            # # pyautogui.click(1335, 735)  # 点击Yes，确认删除订单
                            #
                            #     # time.sleep(3)
                            #
                            # else:
                            time.sleep(2)
                            #识别出确定并点击
                            img = (900, 900, 1000, 1000)
                            ok_img = pyautogui.screenshot(region=img)
                            array1 = np.array(ok_img)
                            cv2.imwrite("array1.png", array1)
                            imgresult = reader.readtext(array1)
                            surepoint = None
                            for t in imgresult:
                                sure_text = t[1]
                                if sure_text == "确定":
                                    print(sure_text)
                                    corrd = t[0]
                                    sure_x = int((corrd[0][0] + corrd[2][0]) / 2)
                                    sure_y = int((corrd[0][1] + corrd[2][1]) / 2)
                                    surepoint = (sure_x + 900, sure_y + 900)
                                    break
                            if surepoint != None:
                                # time.sleep(1)
                                pyautogui.click(x=surepoint[0], y=surepoint[1], clicks=1, button='left')  # 点击确定
                                time.sleep(3)

                            # time.sleep(2)
                            # 识别出确定并点击
                            img2 = (900, 900, 1000, 1000)
                            ok_img2 = pyautogui.screenshot(region=img2)
                            array2 = np.array(ok_img2)
                            imgresult2 = reader.readtext(array2)
                            surepoint2 = None
                            for t2 in imgresult2:
                                sure_text2 = t2[1]
                                if sure_text2 == "确定":
                                    print(sure_text2)
                                    corrd2 = t2[0]
                                    sure_x2 = int((corrd2[0][0] + corrd2[2][0]) / 2)
                                    sure_y2 = int((corrd2[0][1] + corrd2[2][1]) / 2)
                                    surepoint2 = (sure_x2 + 900, sure_y2 + 900)
                                    break
                            if surepoint2 != None:
                                # time.sleep(1)
                                pyautogui.click(x=surepoint2[0], y=surepoint2[1], clicks=1, button='left')  # 点击确定
                                time.sleep(2)



                            pyautogui.click(1124,65)
                            time.sleep(8)
                            # 导出可视化输出
                            pyautogui.click(x=1560, y=135, clicks=1, button='right')   #选中订单数据
                            time.sleep(2)
                            pyautogui.hotkey("v")    #高级
                            time.sleep(1)
                            # 判断是否存在可视化输出这个选项
                            cam_img = (1560, 135, 1200, 1200)
                            save_img = pyautogui.screenshot(region=cam_img)
                            img_array = np.array(save_img)
                            cv2.imwrite("img_array.png", img_array)
                            result = reader.readtext(img_array)
                            CAM_point = None
                            for detection1 in result:
                                text1 = detection1[1]
                                if "可视化" in text1:
                                    print(text1)
                                    corrdinates1 = detection1[0]
                                    save_x = int((corrdinates1[0][0] + corrdinates1[2][0]) / 2)
                                    save_y = int((corrdinates1[0][1] + corrdinates1[2][1]) / 2)
                                    CAM_point = (save_x + 1560, save_y + 135)
                                    print("CAM_point:", CAM_point)
                                    break
                            if CAM_point != None:
                                time.sleep(2)
                                pyautogui.click(x=CAM_point[0], y=CAM_point[1], clicks=1, button='left')  # 点击可视化输出
                                time.sleep(5)

                            # time.sleep(2)
                            pyautogui.click(1125,65)
                            time.sleep(8)

                            #生成CAM输出
                            pyautogui.click(x=1560, y=135, clicks=1, button='right')  # 选中订单数据
                            time.sleep(2)
                            pyautogui.hotkey("v")  # 高级
                            time.sleep(1)

                            # 判断是否存在CAM输出这个选项
                            sure_point = None
                            for detection in result:
                                text = detection[1]
                                if  "生成" in text:
                                    print(text)
                                    corrdinates = detection[0]
                                    sure_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                                    sure_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                                    sure_point = (sure_x + 1560, sure_y + 135)
                                    print("sure_point:", sure_point)
                                    break
                            if sure_point != None:
                                time.sleep(2)
                                pyautogui.click(x=sure_point[0], y=sure_point[1], clicks=1, button='left')  # 点击CAM输出
                                time.sleep(3)
                            # pyautogui.hotkey("z")  # 导出可视化输出
                            # time.sleep(5)
                            # time.sleep(2)
                            pyautogui.click(1125, 65)
                            time.sleep(8)

                            #删除订单
                            pyautogui.click(x=1560, y=135, clicks=1, button='right')  # 选中订单数据
                            time.sleep(1)
                            pyautogui.hotkey("s")  # 删除
                            time.sleep(2)
                            # pyautogui.click(1830,450) # 删除订单
                            pyautogui.hotkey("enter")
                            time.sleep(1)
                            pyautogui.click(1335,735)  #点击Yes，确认删除订单
                            time.sleep(2)

                            if os.path.exists(os.path.join(va_path,filename)):
                                if not os.path.exists(txt_path):
                                    with open(txt_path, 'w') as txt_file:
                                        txt_file.write(file)

                            if not os.path.exists(os.path.join(va_path, xmlfile[0:-4])):
                                re_path = os.path.join(source_dir, file)
                                de_path = os.path.join(error_path, file)
                                shutil.copytree(re_path, de_path)
                            # if not os.path.exists(os.path.join(va_path, filename)) and not os.path.exists(os.path.join(CAM_path, filename)):
                            #         with open(txt_error_filepath, 'a') as f:
                            #             f.write(file + '\n')

            if time.time() - start_time >= 30*60:
                break

        process.terminate()
        time.sleep(5)




def get_xmlfile():
    
    image1 = (1250, 695, 200, 40)
    images_sure1 = pyautogui.screenshot(region=image1)
    array2 = np.array(images_sure1)
    sure_result1 = reader.readtext(array2)
    for txt in sure_result1:
        sure_text = txt[1]
        if sure_text == "确定":
            return True
        else:
            return False







if __name__ == '__main__':
    main()
