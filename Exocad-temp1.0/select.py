import json
import os
import shutil
import numpy as np
import pyautogui



def main():
    source_txtpath = "D:/crowndata-xiaoyuan-2000-3_true"
    txt_path = "D:/crowndata-xiaoyuan-2000-3_true.txt"

    for file in os.listdir(source_txtpath):
        with open(txt_path, 'r', encoding='utf-8') as f:
            existing_contents_vis = f.read().splitlines()
        if file not in existing_contents_vis:
            with open(txt_path, 'a') as f:
                f.write(file + '\n')










if __name__ == '__main__':
    main()