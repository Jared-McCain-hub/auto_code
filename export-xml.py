import os
import shutil
import subprocess
import time
import cv2
import pyautogui
import pyperclip
import easyocr

import numpy as np
from torchvision.models.video import mvit_v2_s

# 初始化OCR阅读器
reader = easyocr.Reader(['ch_sim'])

def get_processed_folders(txt_filepath):
    """读取input.txt中的已处理文件夹，返回去重集合"""
    processed = set()
    if os.path.exists(txt_filepath):
        # 将编码改为gbk以适应Windows系统默认编码
        with open(txt_filepath, 'r', encoding='gbk', errors='ignore') as f:
            for line in f:
                folder = line.strip()
                if folder:  # 跳过空行
                    processed.add(folder)
    return processed

def get_error_folders(error_filepath):
    """获取错误文件夹列表，返回集合"""
    error_folders = set()
    if os.path.exists(error_filepath):
        for item in os.listdir(error_filepath):
            item_path = os.path.join(error_filepath, item)
            if os.path.isdir(item_path):
                error_folders.add(item)
    return error_folders

def main():
    # 路径配置
    DentalManager_path = "C:/Program Files/3Shape/DentalManager/DentalManager.exe"
    source_dir = r"H:\3shape-data\7号牙\3shape"
    CAM_path = r"H:\3shape-data\7号牙\ManufacturingDir"
    va_path = r"H:\3shape-data\7号牙\Visualization output"
    error_filepath = r"H:\3shape-data\7号牙\error"
    miss_CAM = r"H:\3shape-data\7号牙\ManufacturingDir.txt"
    miss_visual = r"H:\3shape-data\7号牙\Visualization output.txt"
    txt_filepath = os.path.join(os.path.dirname(source_dir), "input.txt")

    while True:
        # 获取已处理和错误的文件夹集合（去重）
        processed_folders = get_processed_folders(txt_filepath)
        error_folders = get_error_folders(error_filepath)
        all_processed = processed_folders.union(error_folders)  # 合并为已处理集合

        # 启动3Shape软件
        process = subprocess.Popen(DentalManager_path)
        time.sleep(20)
        pyautogui.click(1277, 695)  # 点击头像登录
        time.sleep(5)
        pyautogui.click(1277, 695)
        # 输入PIN码并确认
        pyautogui.hotkey("1")
        pyautogui.hotkey("2")
        pyautogui.hotkey("3")
        pyautogui.hotkey("4")
        pyautogui.hotkey("5")
        pyautogui.hotkey("6")
        pyautogui.hotkey("enter")
        time.sleep(20)  # 等待页面加载

        start_time = time.time()  # 开始计时
        has_new_folder = False  # 标记是否有新文件夹需要处理

        # 第一层循环：遍历根目录下的文件夹
        for level1 in os.listdir(source_dir):
            level1_path = os.path.join(source_dir, level1)
            # 跳过非文件夹和已处理的文件夹
            if not os.path.isdir(level1_path) or level1 in all_processed:
                continue
            
            has_new_folder = True  # 存在新文件夹
            # 第二层循环：遍历第一层文件夹下的子文件夹
            for level2 in os.listdir(level1_path):
                level2_path = os.path.join(level1_path, level2)
                if not os.path.isdir(level2_path):
                    continue  # 跳过非文件夹

                # 第三层循环：查找XML文件
                for xmlfile in os.listdir(level2_path):
                    if xmlfile.endswith('.xml') and xmlfile != "Materials.xml":
                        xml_path = os.path.join(level2_path, xmlfile)
                        xml_name = xmlfile[:-4]  # 去除.xml后缀
                        txt_path = os.path.join(va_path, xml_name, f"{level1}.txt")

                        # 检查是否需要处理（未生成输出且不在错误目录）
                        if (not os.path.exists(os.path.join(va_path, xml_name)) 
                            and not os.path.exists(os.path.join(CAM_path, xml_name))
                            and not os.path.exists(os.path.join(error_filepath, level1))):

                            # 写入input.txt（确保不重复）
                            if level1 not in processed_folders:
                                # 写入时也使用gbk编码，保持一致
                                with open(txt_filepath, 'a', encoding='gbk') as f:
                                    f.write(level1 + '\n')
                                processed_folders.add(level1)  # 加入已处理集合，避免本次循环重复写入
                                print(f"已记录新文件夹: {level1}")
                            time.sleep(5)

                            # 执行导入操作
                            pyautogui.click(x=2063, y=460, clicks=1, button='right')
                            time.sleep(2)
                            pyautogui.hotkey("y")  # 高级
                            time.sleep(1)
                            pyautogui.hotkey("z")  # 导入
                            time.sleep(1)
                            pyautogui.click(x=1390, y=808, clicks=1, button='left')  # 确定导入
                            time.sleep(5)
                            pyautogui.click(x=2211, y=1254, clicks=1, button='left')  # 切换后缀
                            time.sleep(2)
                            pyautogui.click(x=2211, y=1293, clicks=1, button='left')
                            time.sleep(1)
                            pyautogui.click(x=1971, y=1254, clicks=1, button='left')  # 输入框
                            time.sleep(1)
                            pyperclip.copy(xml_path)
                            print(f"导入XML: {xml_path}")
                            pyautogui.hotkey("ctrl", "v")
                            time.sleep(2)
                            pyautogui.hotkey("enter")
                            time.sleep(2)

                            # 判断是否导入失败
                            if get_xmlfile():
                                pyautogui.click(1277, 757)  # 点击确定
                                time.sleep(2)
                                # 复制到错误文件夹
                                error_dest = os.path.join(error_filepath, level1)
                                if os.path.exists(error_dest):
                                    shutil.rmtree(error_dest)
                                shutil.copytree(level1_path, error_dest)
                                print(f"导入失败，已移至错误文件夹: {level1}")
                                error_folders.add(level1)  # 加入错误集合
                                continue  # 处理下一个文件夹

                            # 处理确定按钮
                            time.sleep(5)
                            # 第一次识别确定按钮
                            img = (900, 900, 1000, 500)
                            ok_img = pyautogui.screenshot(region=img)
                            array1 = np.array(ok_img)
                            cv2.imwrite("array1.png", array1)
                            imgresult = reader.readtext(array1)
                            surepoint = None
                            for t in imgresult:
                                if "确定" in t[1]:
                                    corrd = t[0]
                                    sure_x = int((corrd[0][0] + corrd[2][0]) / 2)
                                    sure_y = int((corrd[0][1] + corrd[2][1]) / 2)
                                    surepoint = (sure_x + 900, sure_y + 900)
                                    break
                            if surepoint:
                                pyautogui.click(surepoint)
                                time.sleep(3)

                            # 第二次识别确定按钮
                            img2 = (900, 900, 1000, 500)
                            ok_img2 = pyautogui.screenshot(region=img2)
                            array2 = np.array(ok_img2)
                            imgresult2 = reader.readtext(array2)
                            surepoint2 = None
                            for t2 in imgresult2:
                                if "确定" in t2[1]:
                                    corrd2 = t2[0]
                                    sure_x2 = int((corrd2[0][0] + corrd2[2][0]) / 2)
                                    sure_y2 = int((corrd2[0][1] + corrd2[2][1]) / 2)
                                    surepoint2 = (sure_x2 + 900, sure_y2 + 900)
                                    break
                            if surepoint2:
                                pyautogui.click(surepoint2)
                                time.sleep(2)

                            # 导出可视化输出
                            pyautogui.click(1124, 65)
                            time.sleep(6)
                            pyautogui.click(x=1347, y=137, clicks=1, button='right')
                            time.sleep(2)
                            pyautogui.hotkey("v")  # 高级
                            time.sleep(1)
                            # 识别可视化输出选项
                            vis_img = (1347, 137, 313, 643)
                            save_img = pyautogui.screenshot(region=vis_img)
                            img_array = np.array(save_img)
                            cv2.imwrite("img_array.png", img_array)
                            result = reader.readtext(img_array)
                            vis_point = None
                            print(result)
                            for detection1 in result:
                                if "可视化" in detection1[1] or "可" in detection1[1] or "视" in detection1[1] or "化" in detection1[1]:
                                    corrdinates1 = detection1[0]
                                    save_x = int((corrdinates1[0][0] + corrdinates1[2][0]) / 2)
                                    save_y = int((corrdinates1[0][1] + corrdinates1[2][1]) / 2)
                                    vis_point = (save_x + 1347, save_y + 137)
                                    break
                            if vis_point:
                                pyautogui.click(vis_point)
                                time.sleep(5)

                            # 生成CAM输出
                            pyautogui.click(1125, 65)
                            time.sleep(6)
                            pyautogui.click(x=1347, y=137, clicks=1, button='right')
                            time.sleep(2)
                            pyautogui.hotkey("v")  # 高级
                            time.sleep(1)
                            # 识别CAM输出选项
                            sure_point = None
                            for detection in result:
                                if "生成" in detection[1] or "CAM" in detection[1]:
                                    corrdinates = detection[0]
                                    sure_x = int((corrdinates[0][0] + corrdinates[2][0]) / 2)
                                    sure_y = int((corrdinates[0][1] + corrdinates[2][1]) / 2)
                                    sure_point = (sure_x + 1347, sure_y + 137)
                                    break
                            if sure_point:
                                pyautogui.click(sure_point)
                                time.sleep(3)

                            # 记录缺失的输出
                            if sure_point is None and vis_point is not None:
                                with open(miss_CAM, 'a', encoding='gbk') as f:
                                    f.write(level1 + '\n')
                            elif sure_point is not None and vis_point is None:
                                with open(miss_visual, 'a', encoding='gbk') as f:
                                    f.write(level1 + '\n')

                            # 删除订单
                            pyautogui.click(1125, 65)
                            time.sleep(6)
                            pyautogui.click(x=1347, y=137, clicks=1, button='right')
                            time.sleep(1)
                            pyautogui.hotkey("s")  # 删除
                            time.sleep(2)
                            pyautogui.hotkey("enter")
                            time.sleep(1)
                            pyautogui.click(1335, 757)  # 确认删除
                            time.sleep(2)

                            # 验证输出是否存在
                            if os.path.exists(os.path.join(va_path, xml_name)) and sure_point and vis_point:
                                if not os.path.exists(txt_path):
                                    os.makedirs(os.path.dirname(txt_path), exist_ok=True)
                                    with open(txt_path, 'w', encoding='gbk') as f:
                                        f.write(level1)
                            else:
                                # 输出缺失，移至错误文件夹
                                error_dest = os.path.join(error_filepath, level1)
                                if os.path.exists(error_dest):
                                    shutil.rmtree(error_dest)
                                shutil.copytree(level1_path, error_dest)
                                print(f"输出缺失，已移至错误文件夹: {level1}")
                                error_folders.add(level1)

            # 30分钟超时检查
            if time.time() - start_time >= 30 * 60:
                print("30分钟超时，重启软件")
                break

        # 关闭软件
        process.terminate()
        time.sleep(5)

        # 如果没有新文件夹需要处理，退出循环
        if not has_new_folder:
            print("所有文件夹已处理完毕，退出程序")
            break

def get_xmlfile():
    """判断是否有无法导入的提示窗口"""
    image1 = (875, 645, 810, 138)
    images_sure1 = pyautogui.screenshot(region=image1)
    array2 = np.array(images_sure1)
    sure_result1 = reader.readtext(array2)
    print(f"识别结果: {sure_result1}")
    # 检查是否有错误提示关键词
    error_keywords = {"确定", "无法", "导入", "错误", "订单","导苁"}
    for txt in sure_result1:
        if any(keyword in txt[1] for keyword in error_keywords):
            return True
    return False

if __name__ == '__main__':
    main()
