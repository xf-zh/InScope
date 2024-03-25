# MuLSys: A New 3D Infrastructure-side Collaborative Perception Dataset based on Multiple LiDAR System

[![paper](https://img.shields.io/badge/arXiv-Paper-green)](https://arxiv.org/abs/2403.10145)
[![ckpts](https://img.shields.io/badge/ckpts-DOWNLOAD-blue)](https://www.alipan.com/s/ATLDUtM3xk1) [Extraction code: 29kp]

This is the official implementation of IJCAI2024 paper. "MuLSys: A New 3D Infrastructure-side Collaborative Perception Dataset based on Multiple LiDAR System".
[Xiaofei Zhang](https://github.com/xf-zh), [Yining Li](https://leofansq.github.io/), [Jinping Wang](https://dblp.org/pid/350/9258.html), [Xiangyi Qin](https://www.linkedin.com/in/zhenlinzhangtim/), [Ying Shen](),  [Zhengping Fan](), [Xiaojun Tan<sup>†</sup>]()

<div style="text-align:center">
<img src="img/dataset.png" width="800" alt="" class="img-responsive">
</div>
<div style="text-align:center">
<img src="img/dataset_introduction.png" width="800" alt="" class="img-responsive">
</div>


## Overview
- [Data Download](#data-download)
- [Data Loading](#data-loading)
- [Quick Start](#quick-start)
- [Benchmark](#benchmark)
- [Citation](#citation)
- [Acknowledgment](#acknowledgment)

## Data Download
Due to project restrictions, the MuLSys dataset is made conditionally public. If you need to use the MuLSys dataset, please fill in the following [MuLSYS Dataset ReIease Agreement.docx](img/MuLSYS Dataset ReIease Agreement.docx) file and email your full name and affiliation to the contact person. We ask for your information only to ensure the dataset is used for non-commercial purposes.

After downloading the data, please put the data in the following structure:
```
├── MuLSys_detect or MuLSys_secondary or MuLSys_principal
│   ├── ImageSets
|      |── train.txt
|      |── test.txt
|      |── val.txt
│   ├── labels
|      |── 000000.txt
|      |── 000001.txt
|      |── 000002.txt
|      |── ...
│   ├── points
|      |── 000000.npy
|      |── 000001.npy
|      |── 000002.npy
|      |── ...
```

```
├── MuLSys_track
│   ├── label_02
|      |── 0000.txt
|      |── 0001.txt
|      |── 0002.txt
|      |── ...
│   ├── points
|      |── 0000
|          |── 000000.bin
|          |── 000001.bin
|          |── 000002.bin
|          |── ...
|      |── 0001
|      |── 0002
|      |── ...
│   ├── evaluate_tracking.seqmap
│   ├── evaluate_tracking.seqmap.test
│   ├── evaluate_tracking.seqmap.training
│   ├── evaluate_tracking.seqmap.val
```

## Data Loading
To facilitate researchers' use and understanding, we adapted the MuLSys dataset to the OpenPCDet framework and provided the corresponding dataset configuration file mulsys.config


## Quick Start
For detection training & inference, you can find instructions in [docs/corridor_scene](docs/corridor_scene) or [docs/intersection_scene](docs/intersection_scene) in detail. (<b>Notes</b>: you may need to set PYTHONPATH to call modified codes other than the pip-installed ones.)

For Tracking, you can find instructions in [docs/tracking.md](docs/tracking.md) in detail.

All the checkpoints are released in link in the tabels below, you can save them in [codes/ckpts/](codes/ckpts/).

## Benchmark
### Results of Cooperative 3D object detection for corridor scenes
|                      Method                    |  AP@0.3  |  AP@0.5  |  AP@0.7  |                                      Download Link                                             |
| ---------------------------------------------- | -------- | -------- | -------- | ---------------------------------------------------------------------------------------------- |
| No Fusion                                      | 40.0     | 29.2     | 11.1     | [url](https://drive.google.com/drive/folders/1mmnIf0HDjS_vL1abptXM91pJHE3BLdqT?usp=drive_link) |
| Late Fusion                                    | 44.5     | 29.9     | 10.8     | [url](https://drive.google.com/drive/folders/1mKt7zKoS6KKzEqKWilHuQtpb36PSztxP?usp=drive_link) |
| Early Fusion                                   | **69.8** | 54.7     | 30.3     | [url](https://drive.google.com/drive/folders/1Ox0Vdh_LPShyK5uGX9s1FHI8USpITy_l?usp=drive_link) |
| [AttFuse](https://arxiv.org/abs/2109.07644)    | 62.7     | 51.6     | 32.1     | [url](https://drive.google.com/drive/folders/1uBTfVMWhbslPzF4f44q36pDHTwEPhoV_?usp=drive_link) |
| [F-Cooper](https://arxiv.org/abs/1909.06459)   | 65.9     | 55.8     | 36.1     | [url](https://drive.google.com/drive/folders/1k677v_DTHXf5lMC9DMBeOLHWdEtd3H-e?usp=drive_link) |
| [Where2Comm](https://arxiv.org/abs/2209.12836) | 67.1     | 55.6     | 34.3     | [url](https://drive.google.com/drive/folders/1aKj5A5wTuy2xJQSiErr0qJ6UWOKxJQFX?usp=drive_link) |
| [CoBEVT](https://arxiv.org/abs/2207.02202)     | 67.6     | **57.2** | **36.2** | [url](https://drive.google.com/drive/folders/1E8CBXLQmBVnShF2TeyTCkPJN_HBGSyzk?usp=drive_link) |




## Citation
If you find MuLSys useful in your research or applications, please consider giving us a star 🌟 and citing it by the following BibTeX entry.
```shell
@inproceedings{zhang2024mulsys,
  title={MuLSys: A New 3D Infrastructure-side Collaborative Perception Dataset based on Multiple LiDAR System},
  author={Zhang, Xiaofei and Li, Yining and Wang, Jinping and Qin, Xiangyi and Shen, Ying and Fan, Zhengping and Tan, Xiaojun},
  booktitle={Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI)},
  year={2024}
}
```

## Acknowledgment
- [DAIR-V2X](https://github.com/AIR-THU/DAIR-V2X)
- [AB3DMOT](https://github.com/xinshuoweng/AB3DMOT)
- [PC3T](https://github.com/hailanyi/3D-Multi-Object-Tracker)
- [ST3D](https://github.com/CVMI-Lab/ST3D)
