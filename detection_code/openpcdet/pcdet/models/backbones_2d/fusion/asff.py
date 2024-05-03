import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

class Asff(nn.Module):
    def __init__(self, model_cfg) -> None:
        super().__init__()
        self.model_cfg = model_cfg
        channel = self.model_cfg.IN_CHANNEL
        self.weight_level_0 = nn.Sequential(
            nn.Conv2d(channel, channel, 1, 1, 0, bias=False),
            nn.Sigmoid()
        )
        self.weight_level_1 = nn.Sequential(
            nn.Conv2d(channel, channel, 1, 1, 0, bias=False),
            nn.Sigmoid()
        )
        self.after_bev = self.model_cfg.AFTER_BEV

    def forward(self, batch_dict1, batch_dict2):
        if self.after_bev:
            lidar_80_bev = batch_dict1['spatial_features']
            lidar_32_bev = batch_dict2['spatial_features']
        else:
            lidar_80_bev = batch_dict1['spatial_features_2d']
            lidar_32_bev = batch_dict2['spatial_features_2d']

        weight_level_0 = self.weight_level_0(lidar_80_bev)
        weight_level_1 = self.weight_level_1(lidar_32_bev)

        # Fuse
        #fuse = weight_level_0 * lidar_80_bev + weight_level_1 * lidar_32_bev
        fuse = weight_level_0 * lidar_32_bev + weight_level_1 * lidar_80_bev
        # # 可视化调试
        # spatial_features1 = lidar_80_bev[0, 0, :, :]
        # spatial_features2 = lidar_32_bev[0, 0, :, :]
        # concat_feature = fuse[0, 0, :, :]
        # # 将张量转换为numpy数组
        # spatial_features1 = spatial_features1.detach().cpu().numpy()
        # spatial_features2 = spatial_features2.detach().cpu().numpy()
        # concat_feature = concat_feature.detach().cpu().numpy()
        # # 使用matplotlib进行可视化
        #
        # plt.imshow(spatial_features1, cmap='hot')
        # # 保存图像
        # plt.savefig("/ai/data/lyn_code/OpenPCDet-master/output/image_pvrcnnplus/lidar_80_bev.png")
        # plt.imshow(spatial_features2, cmap='hot')
        # # 保存图像
        # plt.savefig("/ai/data/lyn_code/OpenPCDet-master/output/image_pvrcnnplus/lidar_32_bev.png")
        # plt.imshow(concat_feature, cmap='hot')
        # # 保存图像
        # plt.savefig("/ai/data/lyn_code/OpenPCDet-master/output/image_pvrcnnplus/spatial_features.png")

        if self.after_bev:
            batch_dict1['spatial_features'] = fuse
        else:
            batch_dict1['spatial_features_2d'] = fuse

        return batch_dict1