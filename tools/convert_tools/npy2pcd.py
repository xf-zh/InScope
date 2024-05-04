import os
import numpy as np

def npy_to_pcd_ascii(npy_file, pcd_file):
    # 读取npy文件
    point_cloud = np.load(npy_file)

    # 获取点云的尺寸信息
    num_points = point_cloud.shape[0]

    # 生成pcd文件的头部信息
    header = f'''\
# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z intensity
SIZE 4 4 4 4
TYPE F F F F
COUNT 1 1 1 1
WIDTH {num_points}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {num_points}
DATA ascii
'''

    # 保存pcd文件
    with open(pcd_file, 'w') as f:
        f.write(header)
        np.savetxt(f, point_cloud, fmt='%.6f')

def batch_convert_npy_to_pcd(input_folder, output_folder):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for file in os.listdir(input_folder):
        # 检查文件是否为npy格式
        if file.endswith('.npy'):
            npy_file = os.path.join(input_folder, file)
            pcd_file = os.path.join(output_folder, file.replace('.npy', '.pcd'))
            npy_to_pcd_ascii(npy_file, pcd_file)
            print(f'Converted {file} to {os.path.basename(pcd_file)}')

if __name__ == '__main__':
    input_folder = 'path1'
    output_folder = 'path2'
    batch_convert_npy_to_pcd(input_folder, output_folder)

