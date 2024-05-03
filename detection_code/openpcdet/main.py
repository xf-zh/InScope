import pickle
import numpy as np
from matplotlib import pyplot as plt
import mayavi.mlab as mlab

# 加载.pkl文件
with open('./second/data_dict_000001.pkl', 'rb') as f:
    pred_dicts = pickle.load(f)

# 可视化点云
points = pred_dicts['points']
fig = mlab.figure(bgcolor=(0, 0, 0))
mlab.points3d(points[:, 0], points[:, 1], points[:, 2], color=(1, 1, 1), mode='point')

# 可视化预测框
pred_boxes = pred_dicts['pred_boxes']
for box in pred_boxes:
    x = [box[0], box[1], box[1], box[0], box[0]]
    y = [box[2], box[2], box[3], box[3], box[2]]
    z = [box[4], box[4], box[4], box[4], box[4]]
    mlab.plot3d(x, y, z, color=(1, 0, 0), tube_radius=None, line_width=2)

mlab.show()

# 可视化点云和预测框
fig, ax = plt.subplots()
ax.scatter(points[:, 0], points[:, 1], c='white', s=1)
for box in pred_boxes:
    rect = plt.Rectangle((box[0], box[2]), box[1] - box[0], box[3] - box[2], fill=False, edgecolor='r')
    ax.add_patch(rect)

plt.show()