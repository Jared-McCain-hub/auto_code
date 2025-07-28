import os
import pyvista as pv

input_root = "D:/袖口数据"
output_dir = "D:/output-images"

for root, dirs, files in os.walk(input_root):
    for file_name in files:
        if file_name.endswith("LowerJaw.beb") or file_name.endswith("UpperJaw.beb"):
            beb_path = os.path.join(root, file_name)
            mesh = pv.read(beb_path)
            plotter = pv.Plotter(off_screen=True)
            plotter.add_mesh(mesh)
            plotter.background_color = "white"
            plotter.show(auto_close=False)
            base_name = os.path.splitext(file_name)[0]
            output_path = os.path.join(output_dir,f"{base_name}.png")
            plotter.screenshot(output_path)
            plotter.close()
            print(f"save:{output_path}")

print("OKOK")