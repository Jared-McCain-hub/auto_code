import os
import shutil
import numpy as np
import pyautogui
import xml.etree.ElementTree as ET


'''3shape 导入牙冠步骤：
    1. 自动化脚本（export-stl）导出牙冠数据;
    2. 脚本初筛掉只有单一输出的数据;
    3. 读取ox文件：
                (1)找到只有单冠的复制单冠和上下颌到新的文件夹存放并重命名,若全是连续冠就不复制;
                (2)在可视化输出文件夹中创建json文件，存放原始牙冠名和对应牙位号, 存放牙颌名称和对应上下颌;
    4. 将可视化输出的文件夹对应的CAM输出的文件夹复制到可视化输出的文件夹下;
'''

def main():
    # 第二步：初筛掉只有单一输出的数据
    source_dir = "F:/datas-2025-04-14-2T-3shape"
    de_filepath = "E:/3shape-2T-7-8#input"
    txt_path = "D:/3shape-2T-txt/8.txt"
    with open(txt_path, 'r', encoding='utf-8') as f:
        existing_contents = f.read().splitlines()
    for content in existing_contents:
        re_path = os.path.join(source_dir, content)
        de_path = os.path.join(de_filepath, content)
        shutil.copytree(re_path, de_path)
    # Manufacturing_dir = "E:/ManufacturingDir"
    # Visualization_dir = "E:/Visualization output"
    # for visfile in os.listdir(Visualization_dir):
    #     if not os.path.exists(os.path.join(Manufacturing_dir, visfile)):
    #         shutil.rmtree(os.path.join(Visualization_dir,visfile))
    #     else:
    #         re_path = os.path.join(Manufacturing_dir,visfile)
    #         de_path = os.path.join(Visualization_dir,visfile,visfile)
    #         shutil.copytree(re_path,de_path)


    # 将错误的数据保存出来
    # sourece_dir = "F:/3shape-1-6+20#output/exists/3shape-2025-04-14-4T-1-6_1-select-over.txt"
    # vispath ="D:/Visualization output"
    # cam_path = "D:/ManufacturingDir"
    # de_vispath = "E:/Visualization output"
    # de_campath = "E:/ManufacturingDir"
    # with open(sourece_dir, 'r', encoding='utf-8') as f:
    #     existing_contents= f.read().splitlines()
    # for file in os.listdir(vispath):
    #     if file not in existing_contents:
    #         re_vispath = os.path.join(vispath,file)
    #         de_visfilepath = os.path.join(de_vispath, file)
    #
    #         shutil.copytree(re_vispath,de_visfilepath)
    #         re_campath = os.path.join(cam_path,file)
    #         de_camfilepath = os.path.join(de_campath,file)
    #         if os.path.exists(re_campath):
    #             shutil.copytree(re_campath,de_camfilepath)


    #将提出处理的数据记录txt
    # vispath = "D:/Visualization output"
    # for file in os.listdir(vispath):
    #     select_txtpath = os.path.join(os.path.dirname(vispath), "select_over.txt")
    #     if os.path.exists(select_txtpath):
    #         with open(select_txtpath, 'r') as f:
    #             existing_lines = f.read()
    #             if file not in existing_lines:
    #                 with open(select_txtpath, 'a', encoding='utf-8') as f:
    #                     f.write(file + '\n')
    #     else:
    #         with open(select_txtpath, 'w') as txt_file:
    #             txt_file.write(file+ '\n')



if __name__ == '__main__':
    main()