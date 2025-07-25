import json
import os
import shutil
import numpy as np
import pyautogui



def main():
    source_dir= "D:/exocad-data/crowndata-xiaoyuan-2000-3"
    output_cam = "D:/exocad-data/crowndata-xiaoyuan-2000-3_false"
    vistxt_path = "D:/exocad-data/crowndata-xiaoyuan-2000-3_false.txt"


    with open(vistxt_path, 'r', encoding='utf-8') as f:
        existing_contents_vis = f.read().splitlines()

    for file in existing_contents_vis:
        filepath = os.path.join(source_dir, file)
        de_path = os.path.join(output_cam,file)
        if not os.path.exists(de_path):
            shutil.copytree(filepath, de_path)











if __name__ == '__main__':
    main()