import os

# input_dir_list = ["D:/ManufacturingDir", "D:/Visualization output"]
# output_dir_list = ["E:/3shape-1-6+20#output/ManufacturingDir", "E:/3shape-1-6+20#output/Visualization output"]

input_dir_list = ["D:/Visualization output"]
output_dir_list = ["E:/3shape-1-6+20#output/Visualization output"]

for i in range(len(input_dir_list)):
    dirnames = os.listdir(input_dir_list[i])
    for dirname in dirnames:
        os.makedirs(os.path.join(output_dir_list[i], dirname), exist_ok=True)