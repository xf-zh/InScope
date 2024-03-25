import os
import numpy as np
from tqdm import tqdm

def npy_to_bin(input_folder, output_folder):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for file in tqdm(os.listdir(input_folder)):
        # 检查文件是否为npy格式
        if file.endswith('.npy'):
            print(os.path.join(input_folder, file))
            # 读取npy文件
            point_cloud = np.load(os.path.join(input_folder, file))
            # 转换为点云bin文件
            point_cloud_bin = point_cloud.astype(np.float32).tostring()

            # 保存bin文件到输出文件夹
            bin_file = os.path.join(output_folder, file.replace('.npy', '.bin'))
            with open(bin_file, 'wb') as f:
                f.write(point_cloud_bin)
            print(f'Converted {file} to {bin_file}')

if __name__ == '__main__':
    input_folder = 'path1'
    output_folder = 'path2'
    npy_to_bin(input_folder, output_folder)
