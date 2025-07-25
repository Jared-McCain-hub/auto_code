import os

input_split_list = [str(i) for i in range(1,21)]
input_root = "F:/3shape-datas"

for input_split in input_split_list:
    dirnames = os.listdir(os.path.join(input_root, input_split))
    output_names = [name + "\n" for name in dirnames]
    with open(os.path.join(input_root, f"{input_split}.txt"), 'w') as f:
        f.writelines(output_names)
