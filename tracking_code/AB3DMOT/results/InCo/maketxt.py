# Because some classes are not present in a certain dataset sequence, it is necessary to create an empty txt file to make 87 txt files complete, otherwise an error will be reported during evaluation
import os

folder_path = './pointrcnn_Pedestrian_val_H1/data_0'  # 替换为实际的文件夹路径

for i in range(87):  # 从0000.txt到0086.txt一共87个文件
    file_name = f'{i:04d}.txt'  # 格式化文件名为四位数，例如0000.txt
    file_path = os.path.join(folder_path, file_name)  # 构建文件的完整路径

    if os.path.exists(file_path):  # 检查文件是否已存在
        print(f'{file_name} already exists. Skipping...')
    else:
        with open(file_path, 'w') as file:  # 创建空txt文件
            pass
        print(f'{file_name} created successfully.')