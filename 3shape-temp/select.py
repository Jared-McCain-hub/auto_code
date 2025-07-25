import json
import os
import shutil
import numpy as np
import pyautogui



def main():
    source_txtpath = "F:/3shape-1-6"
    source_dir= "F:/datas-2025-04-14-4T-3shape"
    de_dir = "F:/3shape-4T-1-6+20#input"
    error_path= "F:/3shape-4T-1-6+20#output-error"
    for txtfile in os.listdir(source_txtpath):
        txtfilepath = os.path.join(source_txtpath,txtfile)
        with open(txtfilepath, 'r', encoding='utf-8')as f:
            contents = f.read().splitlines()
        for conten in contents:
            re_filepath = os.path.join(source_dir, conten)
            de_filepath = os.path.join(de_dir, conten)
            if not os.path.exists(de_filepath):
                shutil.copytree(re_filepath,de_filepath)

    #1.删除文件中重复文件名的数据
    # source_dir = "E:/3shape-2T-7-8#input"
    # path = "D:/1"
    # filenames = []
    # for file in os.listdir(source_dir):
    #     # filename = file.split('#')[0]
    #     filepath =os.path.join(source_dir, file)
    #     for xmlfile in os.listdir(filepath):
    #         if xmlfile.endswith('.xml') and xmlfile != "Materials.xml":
    #             if xmlfile not in filenames:
    #                 filenames.append(xmlfile)
    #             else:
    #                 repath = os.path.join(source_dir, file)
    #                 if os.path.exists(repath):
    #                     shutil.rmtree(repath)

    #2.筛选出已经导出的数据
    # source_dir = "F:/datas-2025-04-14-2T-3shape"
    # de_filepath = "F:/3shape-data-4T-1-6+20#2"
    # CAM_path = "F:/3shape-data-4T-1-6+20#2/ManufacturingDir"
    # vis_path = "F:/3shape-data-4T-1-6+20#2/Visualization output"
    # txt_path = "D:/3shape-4T-16-20.txt"
    # camtxtpath = "D:/upload_3shape-4T-16-20-2-output-cam.txt"
    # error_txtpath = "D:/upload_3shape-4T-16-20-2-error.txt"
    # with open(txt_path, 'r', encoding='utf-8') as f:
    #     existing_contents = f.read().splitlines()
    #
    # with open(camtxtpath, 'r', encoding='utf-8') as fi:
    #     existing_content_cam = fi.read().splitlines()
    #
    # with open(error_txtpath, 'r', encoding='utf-8') as fil:
    #     existing_content_error = fil.read().splitlines()
    #
    # files = os.listdir(vis_path)
    # for visfile in files:
    #     if visfile in existing_contents:
    #         visfilepath = os.path.join(vis_path, visfile)
    #         camfilepath = os.path.join(CAM_path, visfile)
    #         shutil.rmtree(visfilepath)
    #         if os.path.exists(camfilepath):
    #             shutil.rmtree(camfilepath)
    #     elif visfile in existing_content_cam:
    #         visfilepath = os.path.join(vis_path, visfile)
    #         camfilepath = os.path.join(CAM_path,visfile)
    #         shutil.rmtree(visfilepath)
    #         if os.path.exists(camfilepath):
    #             shutil.rmtree(camfilepath)
    #     else:
    #         origintxtfilename = os.path.join(vis_path,visfile)
    #         for txtfile in os.listdir(origintxtfilename):
    #             if txtfile.endswith('.txt'):
    #                 filename = txtfile[0:-4]
    #                 if filename in existing_content_error:
    #                     visfilepath = os.path.join(vis_path, visfile)
    #                     camfilepath = os.path.join(CAM_path, visfile)
    #                     shutil.rmtree(visfilepath)
    #                     if os.path.exists(camfilepath):
    #                         shutil.rmtree(camfilepath)
    #                 break
            # re_vispath = os.path.join(vis_path,visfile)
            # de_vispath = os.path.join(de_filepath,os.path.basename(vis_path), visfile)
            # re_campath = os.path.join(CAM_path, visfile)
            # de_campath = os.path.join(de_filepath, os.path.basename(CAM_path), visfile)
            # shutil.copytree(re_vispath,de_vispath)
            # if os.path.exists(re_campath):
            #     shutil.copytree(re_campath,de_campath)






    # #使用脚本对数据已经拆分文件夹存储
    # source_dir = "F:/3shape-datas/6"
    # target_dir = "D:/3shape-datas-2-3"
    # batch_size = 2000

    # files = os.listdir(source_dir)
    # files.sort()
    # batch_count = 1
    # file_count = 0
    # for file in files:
    #     source_file=os.path.join(source_dir,file)
    #     target_subdir = os.path.join(target_dir,file)
    #     if not os.path.exists(target_subdir):
    #         shutil.copytree(source_file,target_subdir)

        # file_count += 1
        # if file_count == batch_size:
        #     batch_count += 1
        #     file_count = 0


    # 字典映射,创建txt存储在VisualizationS output文件夹
    # source_dir = "D:/3shape-datas-1-6"
    # target_dir = "D:/Visualization output"
    # xml_files = {}
    # for file in os.listdir(source_dir):
    #     for xmlfile in os.listdir(os.path.join(source_dir, file)):
    #         if xmlfile.endswith('.xml') and xmlfile != "Materials.xml":
    #             filename = xmlfile[0:-4]
    #             xml_files[filename] = file
    #             break
    # for visfile in os.listdir(target_dir):
    #     subfolder_path = os.path.join(target_dir, visfile)
    #     if visfile in xml_files:
    #         value = xml_files[visfile]
    #         txt_filepath = os.path.join(subfolder_path,f"{value}.txt")
    #         if not os.path.exists(txt_filepath):
    #             print(txt_filepath)
    #             with open(txt_filepath, 'w') as txt_file:
    #                 txt_file.write(value)

    #记录已跑数据的文件名
    # source_dir = "D:/ManufacturingDir"
    # target_dir = "D:/Visualization output"
    # outputtxt_filepath = "E:/3shape-1-6+20#output/3shape-1-6+20#output_vis.txt"
    # txt_filepath = "E:/3shape-1-6+20#output/3shape-1-6+20#output_man.txt"
    # for file in os.listdir(target_dir):
    #     filename = os.path.basename(file)
    #     with open(outputtxt_filepath, 'a') as f:
    #         f.write(filename+ '\n')
    #
    # for man_file in os.listdir(source_dir):
    #     man_filename = os.path.basename(man_file)
    #     with open(txt_filepath, 'a') as f:
    #         f.write(man_filename+ '\n')


    #将无txt的数据区分开
    # source_manpath= "D:/ManufacturingDir"
    # source_path ="D:/Visualization output"
    # vis_path= "E:/3shape-1-6+20#output/exists/Visualization output"
    # man_path = "E:/3shape-1-6+20#output/exists/ManufacturingDir"
    # not_txt_vispath = "E:/3shape-1-6+20#output/exists/txt-visulization"
    # for visfile in os.listdir(source_path):
    #     if not os.path.exists(os.path.join(vis_path, visfile)):
    #         if os.path.exists(os.path.join(source_manpath,visfile)):
    #             re_vispath = os.path.join(source_path, visfile)
    #             de_vispath = os.path.join(vis_path, visfile)
    #             # if not os.path.exists(de_vispath):
    #             #     os.makedirs(de_vispath)
    #             if not os.path.exists(de_vispath):
    #                 shutil.copytree(re_vispath,de_vispath)
    #             re_manpath = os.path.join(source_manpath,visfile)
    #             de_manpath = os.path.join(man_path, visfile)
    #             # if not os.path.exists(de_manpath):
    #             #     os.makedirs(de_manpath)
    #             if not os.path.exists(de_manpath):
    #                 shutil.copytree(re_manpath,de_manpath)

    # vispath = "E:/3shape-1-6+20#output/exists/Visualization output"
    # select_txtpath = os.path.join(os.path.dirname(vispath), "select_over.txt")
    # for file in os.listdir(vispath):
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