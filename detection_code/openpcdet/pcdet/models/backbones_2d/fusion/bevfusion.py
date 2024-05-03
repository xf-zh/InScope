import torch
from torch import nn


class Bevfusion(nn.Module):
    def __init__(self, model_cfg) -> None:
        super().__init__()
        self.model_cfg = model_cfg
        in_channel = self.model_cfg.IN_CHANNEL
        out_channel = self.model_cfg.OUT_CHANNEL
        self.conv = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_channel),
            nn.ReLU(True)
        )

    def forward(self, batch_dict1, batch_dict2):
        """
        Args:
            batch_dict:
                spatial_features_lidar (tensor): Bev features from lidar32 modality
                spatial_features (tensor): Bev features from lidar80 modality

        Returns:
            batch_dict:
                spatial_features (tensor): Bev features after muli-modal fusion
        """
        lidar_80_bev = batch_dict1['spatial_features']
        lidar_32_bev = batch_dict2['spatial_features']
        cat_bev = torch.cat([lidar_32_bev, lidar_80_bev], dim=1)
        mm_bev = self.conv(cat_bev)

        batch_dict1['spatial_features'] = mm_bev
        return batch_dict1
