import os
import shutil

input_root = "F:/3shape-datas"
done_dir_root = "D:/Visualization output"
output_root = "E:/3shape-1-6+20#input-wo"
input_split_list = ["1", "2", "3", "4", "5", "6", "20"]
os.makedirs(output_root, exist_ok=True)
# get done list
done_list_fname = set()
dirnames = os.listdir(done_dir_root)
for dirname in dirnames:
    fnames = os.listdir(os.path.join(done_dir_root, dirname))
    for fname in fnames:
        if fname.endswith(".txt"):
            done_list_fname.add(fname[:-4])

for input_split in input_split_list:
    for dirname in os.listdir(os.path.join(input_root, input_split)):
        if (dirname in done_list_fname):
            print("found done:", input_split, dirname)
        else:
            if not os.path.exists(os.path.join(output_root, dirname)):
                shutil.copytree(os.path.join(input_root, input_split, dirname), os.path.join(output_root, dirname))
                print("copied:", input_split, dirname)
            else:
                print("already exits:", input_split, dirname)
