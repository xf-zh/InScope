# The purpose of this py file is to merge txt files of different categories into one txt file
for i in range(87):
    merged_lines = []

    file_path = f'./centerpoint_Car_val_H1/data_0/{str(i).zfill(4)}.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()
        merged_lines.extend(lines)

    file_path = f'./centerpoint_Truck_val_H1/data_0/{str(i).zfill(4)}.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()
        merged_lines.extend(lines)

    file_path = f'./centerpoint_Pedestrian_val_H1/data_0/{str(i).zfill(4)}.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()
        merged_lines.extend(lines)

    file_path = f'./centerpoint_Cyclist_val_H1/data_0/{str(i).zfill(4)}.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()
        merged_lines.extend(lines)

    sorted_lines = sorted(merged_lines, key=lambda line: int(line.split()[0]))

    output_file_path = f'./merged_output/{str(i).zfill(4)}.txt'
    with open(output_file_path, 'w') as merged_file:
        merged_file.writelines(sorted_lines)