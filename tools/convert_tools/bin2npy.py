import os
import numpy as np
from tqdm import tqdm

# 输入文件夹包含所有的.bin文件
input_folder = 'path1'

# 输出文件夹用于存储所有的.npy文件
output_folder = 'path2'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取所有的.bin文件列表
bin_files = [f for f in os.listdir(input_folder) if f.endswith('.bin')]
bin_files.sort()
# 定义起始编号
start_number = 16694

# 遍历每个.bin文件并进行转换
for idx, bin_file in tqdm(enumerate(bin_files), desc="Converting"):
    # 构建输入和输出文件的完整路径
    input_path = os.path.join(input_folder, bin_file)
    output_path = os.path.join(output_folder, f"{start_number + idx:06d}.npy")
    print(input_path)
    print(output_path)
    # 从.bin文件读取数据并保存为.npy文件
    with open(input_path, 'rb') as f:
        data = np.fromfile(f, dtype=np.float32)  # 根据实际数据类型进行修改
        # 将数据重塑为n*4的形式
        data = data.reshape(-1, 4)
        np.save(output_path, data)

print("Conversion completed.")
