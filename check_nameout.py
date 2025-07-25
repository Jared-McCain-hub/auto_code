import os

origin_dir = "D:\CBCT\源文件"
out_dir = "D:\CBCT\导出数据"

out_file = []
for file in os.listdir(out_dir):
    file = file + ".nii.gz"
    out_file.append(file)

orgin_file = []
for file in os.listdir(origin_dir):
    orgin_file.append(file)

for f in orgin_file:
    if f not in out_file:
        print(f)