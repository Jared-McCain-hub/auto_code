import os

base_dir = "D:\CBCT\导出数据"
output_txt = "D:\\CBCT\\result.txt"

output_file = []
for file in os.listdir(base_dir):
    folder_dir = os.path.join(base_dir,file)
    for f in os.listdir(folder_dir):
        if f in ["STL（无下颌神经）", "stl-output", "stl", "STL"]:
            file_dir = os.path.join(folder_dir,f)
            for stl_file in os.listdir(file_dir):
                if stl_file in ["Nerve_0.stl", "Nerve_1.stl"]:
                    output_file.append(file)
                    break
new_file = list(set(os.listdir(base_dir)) - set(output_file))

output_dir = os.path.dirname(output_txt)
os.makedirs(output_dir, exist_ok=True) 

with open(output_txt, 'w', encoding='utf-8') as f:
       
    f.write("\n不包含特定STL文件的文件夹:\n")
    for item in new_file:
        f.write(f"- {item}\n")
                    


