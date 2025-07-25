import json
import os
import shutil
import numpy as np
import pyautogui



def main():
    source_txtpath = "F:/3shape-1-6"
    source_dir= "F:/3shape-4T-1-6+20#input"
    output_vis = "E:/3shape-1-6/Visualization output"
    output_cam = "E:/3shape-1-6/ManufacturingDir"
    error_path= "F:/3shape-4T-1-6+20#output-error"
    vistxt_path = "D:/upload_3shape-4T-16-20-2-output-vis.txt"
    camtxtpath = "D:/upload_3shape-4T-16-20-2-output-cam.txt"
    error_txtpath = "D:/upload_3shape-4T-16-20-2-error.txt"

    output_file = []
    for visfile in os.listdir(output_vis):
        output_file.append(visfile)
    for camfile in os.listdir(output_cam):
        if camfile not in output_file:
            output_file.append(camfile)

    with open(vistxt_path, 'r', encoding='utf-8') as f:
        existing_contents_vis = f.read().splitlines()

    with open(camtxtpath, 'r', encoding='utf-8') as fi:
        existing_content_cam = fi.read().splitlines()

    with open(error_txtpath, 'r', encoding='utf-8') as fil:
        existing_content_error = fil.read().splitlines()

    for file in os.listdir(source_dir):
        filepath = os.path.join(source_dir,file)
        for xmlfile in os.listdir(filepath):
            if xmlfile.endswith('.xml') and xmlfile != "Materials.xml":
                filename = xmlfile[0:-4]
                if filename not in output_file and filename not in existing_contents_vis and filename not in existing_content_cam:
                    if file not in existing_content_error:
                        re_path = os.path.join(source_dir, file)
                        de_path = os.path.join(error_path, file)
                        shutil.copytree(re_path,de_path)
                break








if __name__ == '__main__':
    main()