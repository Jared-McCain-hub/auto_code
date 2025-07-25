import os
import shutil
import glob
import pypinyin
from pathlib import Path
import zipfile

from torch.utils.flop_counter import suffixes

source_dir = "D:/20250317-beb"

def main():

    #解压压缩包
    for bebfile in os.listdir(source_dir):
        for file in os.listdir(os.path.join(source_dir, bebfile)):
            if file.endswith('.zip'):
                with zipfile.ZipFile(os.path.join(source_dir,bebfile,file),'r') as zf:
                    zf.extractall(os.path.join(source_dir,bebfile))
    #             os.remove(os.path.join(source_dir, bebfile, file))

    #第一步：将后缀不是beb的数据删除
    # for bebfile in os.listdir(source_dir):
    #     bebpath = os.path.join(source_dir, bebfile)
    #     for txtfile in os.listdir(os.path.join(source_dir, bebfile)):
    #         path = os.path.join(source_dir, bebfile, txtfile)
            # for f in os.listdir(path):
            #     if f.endswith('-LowerJaw.beb') or f.endswith('-UpperJaw.beb'):
            #         txtpath = os.path.join(bebpath, txtfile,f)
            #         new_path = os.path.join(bebpath,f)
            #         if not os.path.exists(new_path):
            #             shutil.copy(txtpath, new_path)

            # if os.path.isdir(path):
            #     shutil.rmtree(path)



    #第二步：将beb文件名根据文件夹重命名
    # for bebfile in os.listdir(source_dir):
    #     bebpath = os.path.join(source_dir, bebfile)
    #     for txtfile in os.listdir(os.path.join(source_dir, bebfile)):
    #         name = txtfile[-13:]
    #         old_name_path = os.path.join(bebpath, txtfile)
    #         new_name_path = os.path.join(bebpath, bebfile+name)
    #         if not(os.path.exists(new_name_path)):
    #             os.rename(old_name_path, new_name_path)
    #
    #
    # #第三步：
    # for bebfile in os.listdir(source_dir):
    #     bebpath = os.path.join(source_dir, bebfile)
        # if len(os.listdir(bebpath))>3:
        #     print(bebpath)
    #
    # input_path = Path(source_dir)
    # suffixes = ['.downloading', 'txt']
    # for file in input_path.rglob('*'):
    #     if any(file.name.endswith(suffix) for suffix in suffixes):
    #         os.remove(file)


if __name__ == '__main__':
    main()