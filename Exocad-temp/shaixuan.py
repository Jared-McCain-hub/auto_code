import os
import shutil
import numpy as np
import pyautogui
from PIL import Image, ImageGrab, ImageEnhance
import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
# from charset_normalizer import detect
from datetime import datetime

from numpy.ma.core import mask_or
from pytesseract import Output
from torch.ao.nn.quantized.functional import threshold

#from crown_detect import CrownDetect
import pytesseract as tess
import easyocr




def main():
    source_dir = "D:/ExoCad"
    path = "D:/ExoCad_true"
    for file in os.listdir(source_dir):
        if len(os.listdir(os.path.join(source_dir,file)))>3:
            oldfilePath = os.path.join(source_dir,file)
            newfilePath = os.path.join(path,file)
            shutil.copytree(oldfilePath,newfilePath)
            shutil.rmtree(oldfilePath)


    # images_path = "D:/TEST_images"
    # for file in os.listdir(source_dir):
    #     if file + "-Upper.png"  in os.listdir(images_path):
    #         re_filepath = os.path.join(source_dir, file)
    #         de_filepath = os.path.join(os.path.dirname(source_dir), "1", file)
    #         shutil.copytree(re_filepath, de_filepath)
    #         shutil.rmtree(re_filepath)
    # pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    # screenshot_path = "D:/temp/screenshot.png"
    # image_upp = cv2.imread(screenshot_path)
    # target_color = (109,58,71)


# # 截图找到Auto hide的坐标位置
#     screenshot_path = "D:/temp/2.png"
#     screenshot_mesh = cv2.imread(screenshot_path)
    # x,y=1150,665
    # b,g,r = screenshot_mesh[y,x]
    # print(f'RGB值：R={r},G={g},B={b}')
    # image = cv2.cvtColor(np.array(screenshot_mesh), cv2.COLOR_RGB2BGR)  # 将截图转为Opencv支持的格式
    # # 创建二值图像
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    #
    # # 使用阈值化方法来分割背景
    # _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # # binary2 = cv2.erode(binary, (110, 110), iterations=50)
    # binary2 = cv2.erode(binary, (120, 120), iterations=50)
    # for y in range(binary2.shape[0]):
    #     for x in range(binary2.shape[1]):
    #         if binary2[y, x] == 255:
    #             con_point = (x, y)
    #             print("白色像素点坐标：", con_point)
    #             break
    #     else:
    #         continue
    #     break
    # else:
    #     print("未找到白色像素的点")

    # 定义黄色范围
    # lower_yellow = np.array([150, 130, 100])
    # upper_yellow = np.array([255, 215, 162])
    # # # 创建二值图像
    # mask = cv2.inRange(image, lower_yellow, upper_yellow)
    # _, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # binary2 = cv2.erode(binary, (110, 110), iterations=30)
    # cv2.imwrite("D:/temp/mask.png", mask)
    # cv2.imwrite("D:/temp/binary.png", binary2)
    # white_coords = np.where(binary2 == 255)
    # if white_coords[0].size > 0:
    #     num_white_points = len(white_coords[0])
    #     print(num_white_points)
    #     start_index = num_white_points // 3
    #     print(start_index)
    #     for idx in range(start_index, num_white_points):
    #         y, x = white_coords[0][idx], white_coords[1][idx]
    #         con_point = (x, y)
    #         print("白色像素点坐标：", con_point)
    #         break
    #
    # else:
    #     print("未找到白色像素的点")
    # for y in range(binary2.shape[0]):
    #     for x in range(binary2.shape[1]):
    #         if binary2[y, x] == 255:
    #             print("白色像素点坐标：", x,y)
    #             return (x,y)
    #     else:
    #         continue
    # return -1

    # cv2.imshow("mask", mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()




    # a = np.where(screenshot_mesh == np.array([109, 48, 71]))[:2]
    # screenshot_mesh[a] = 0D:\2\-lejiaxiang\-lejiaxiang.dentalProject

    # cv2.imwrite("a.png", screenshot_mesh)
    # print(a)
    # image = cv2.cvtColor(np.array(screenshot_mesh), cv2.COLOR_RGB2BGR)  # 将截图转为Opencv支持的格式
    # gray = cv2.cvtColor(screenshot_mesh, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    # cv2.imwrite("gray.png", gray)

    # 使用阈值化方法来分割背景
    # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # binary2= cv2.dilate(binary, (120,120), iterations=130)
    # cv2.imwrite("output2.png", binary2)
    # binary1 = cv2.erode(binary2, (150,150), iterations=100)
    # contours_low, hierarchy_low = cv2.findContours(binary_low, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imwrite("output1.png", binary1)
    # cv2.imwrite("output.png", binary)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # # 截图保存
    # # D:\2\-lejiaxiang\-lejiaxiang.dentalProject

    #D:\2\-lejiaxiang\-lejiaxiang.dentalProject




if __name__ == '__main__':
    main()