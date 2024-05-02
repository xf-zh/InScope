# InCo: A New 3D Infrastructure-side Collaborative Perception Dataset based on Interscetion Scenes

[![paper](https://img.shields.io/badge/arXiv-Paper-green)](https://arxiv.org/abs/2403.10145)
[![ckpts](https://img.shields.io/badge/ckpts-DOWNLOAD-blue)](https://www.alipan.com/s/ATLDUtM3xk1) [Extraction code: 29kp]

This is the official implementation of InCo dataset. "InCo: A New 3D Infrastructure-side Collaborative Perception Dataset based on Interscetion Scenes".
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
Due to project restrictions, the InCo dataset is made conditionally public. If you need to use the InCo dataset, please fill in the following [./img/InCo Dataset ReIease Agreement.docx](img/InCo_Datase_ReIease_Agreement.docx) file and email your full name and affiliation to the contact person. We ask for your information only to ensure the dataset is used for non-commercial purposes.

After downloading the data, please put the data in the following structure:
```
├── InCo_detect or InCo_secondary or InCo_principal
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
├── InCo_track
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
To facilitate researchers' use and understanding, we adapted the InCo dataset to the OpenPCDet framework and provided the corresponding dataset configuration file [./InCo.config](detection_code/openpcdet/tools/cfgs/InCo_dataset.yaml)


## Quick Start

For detection training & inference, you can find instructions in [detection_code/openpcdet](docs/corridor_scene) in detail. 

For Tracking, you can find instructions in [docs/tracking.md](docs/tracking.md) in detail.

All the checkpoints are released in link in the tabels below, you can save them in [codes/ckpts/](codes/ckpts/).

## Benchmark
### Results of 3D object detection based on the InCo_detect dataset

|     Methods       |Car AP@0.7 | Truck AP@0.7| Cyclist AP@0.5| Pedestrian AP@0.5| mAP40    |  FPS    |  Download Link    |
| ------------------|-----------|-------------|---------------|------------------|----------|---------|-------------------|
| Point-RCNN        |   71.75   |    94.50    |     62.91     |      68.13       |   74.32  | 4.58    |                   |
| 3DSSD             |   68.00   |    95.08    |     36.58     |      13.88       |   53.38  | 11.35   |                   |
| SECOND            |   72.82   |    95.98    |     59.91     |      47.95       |   69.17  | 20.58   |                   |
| Pointpillar       |   78.04   |    95.86    |     58.46     |      35.34       |   66.93  | 24.51   |                   |
| PV-RCNN           |   75.05   |    94.52    |     56.31     |      48.37       |   68.56  | 4.35    |                   |
| PV-RCNN++         |   80.55   |    95.92    |     70.92     |      53.31       |   75.18  | 14.66   |                   |
| CenterPoint       |   77.24   |    96.12    |     74.74     |      70.45       |   79.64  | 30.49   |                   |
| CenterPoint\_RCNN |   78.33   |    96.48    |     75.23     |      71.13       |   80.29  | 6.55    |                   |


### Results of 3D object detection based on the InCo_secondary, InCo_principal, and InCo_detect datasets

#### Detection result based on the Secondary LiDAR Only 


|    Methods       |Car AP@0.7 | Truck AP@0.7| Cyclist AP@0.5| Pedestrian AP@0.5|   mAP40  |  FPS    |Download Link      |
|------------------|-----------|-------------|---------------|------------------|----------|---------|-------------------|
|  Point-RCNN	     |   14.12   |    45.36    |     20.62     |      23.66       |  25.94   |  22.94  |                   |
|  Pointpillar	    |   44.77   |    82.52    |     31.42     |      33.18       |  47.97   |  87.72  |                   |
|  PV-RCNN++       |   43.49   |    76.04    |     39.94     |      34.60       |  48.52   |  16.67  |                   |
|  CenterPoint	    |   35.92   |    68.78    |     38.24     |      37.40       |  45.08   |  107.53 |                   |

#### Detection result based on the Principal LiDAR Only 

|    Methods       |Car AP@0.7 | Truck AP@0.7| Cyclist AP@0.5| Pedestrian AP@0.5|   mAP40  |  FPS    |Download Link      |
|------------------|-----------|-------------|---------------|------------------|----------|---------|-------------------|
|    Point-RCNN    | 61.14     |    48.96    |    61.99      |88.80             |   65.22  |  4.67   |                   |
|    Pointpillar   | 67.34     |    91.59    |    43.51      |23.82             |   56.57  |  25.25  |                   |
|    PV-RCNN++     | 72.59     |    91.02    |    61.21      |45.26             |   67.52  |  13.81  |                   |
|    CenterPoint   | 61.31     |    82.02    |    52.73      |49.62             |   61.42  |  33.90  |                   |

#### Detection result based on the Early Fusion	Mechanism

|    Methods       |Car AP@0.7 | Truck AP@0.7| Cyclist AP@0.5| Pedestrian AP@0.5|   mAP40  |  FPS    |Download Link      |
|------------------|-----------|-------------|---------------|------------------|----------|---------|-------------------|
|   Point-RCNN     |71.75      |94.50        |62.91          |68.13             |74.32     | 4.58    |                   |
|   Pointpillar    |78.04      |95.86        |58.46          |35.34             |66.93     |24.33    |                   |
|   PV-RCNN++      |80.55      |95.92        |70.92          |53.31             |75.18     |12.45    |                   |
|   CenterPoint    |77.24      |96.12        |74.74          |70.45             |79.64     |30.49    |                   |

#### Detection result based on the Late Fusion	Mechanism

|    Methods       |Car AP@0.7 | Truck AP@0.7| Cyclist AP@0.5| Pedestrian AP@0.5|   mAP40  |  FPS    |Download Link      |
|------------------|-----------|-------------|---------------|------------------|----------|---------|-------------------|
|Point-RCNN        |62.69      |90.93        |52.31          |61.31             |66.81     |1.32     |                   |
|Pointpillar       |68.65      |93.48        |49.92          |31.81             |60.96     |1.81     |                   |
|PV-RCNN++         |68.01      |92.65        |56.95          |53.47             |67.77     |1.21     |                   |
|CenterPoint       |58.13      |85.65        |56.01          |50.03             |62.45     |6.40     |                   |

#### Detection result based on the Middle Fusion	Mechanism

|    Methods       |Car AP@0.7 | Truck AP@0.7| Cyclist AP@0.5| Pedestrian AP@0.5|   mAP40  |  FPS    |Download Link      |
|------------------|-----------|-------------|---------------|------------------|----------|---------|-------------------|
|Point-RCNN        |    -      |    -        |    -          |    -             |    -     |    -    |                   |
|Pointpillar       |    -      |    -        |    -          |    -             |    -     |    -    |                   |
|PV-RCNN++         |73.78      |91.89        |62.06          |52.06             |69.95     |13.02    |                   |
|CenterPoint       |52.74      |81.73        |51.19          |38.95             |56.15     |15.85    |                   |

### Results of data domain transfer on the car class

 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |   &nbsp; &nbsp; &nbsp; InCo→KITTI &nbsp; &nbsp; &nbsp; &nbsp;| &nbsp; &nbsp; &nbsp;DAIR-V2X-I→KITTI &nbsp; &nbsp;| &nbsp;  &nbsp; &nbsp;  &nbsp;   &nbsp; ONCE→KITTI    &nbsp;  &nbsp; &nbsp;  &nbsp;    | &nbsp; InCo→DAIR-V2X-I &nbsp; | DAIR-V2X-I→InCo|

| Source→Target  |Moderate | mAP40 |Moderate| mAP40|   Moderate |  mAP40  |Moderate  |mAP40| AP40 |
| ---------------|---------|-------|--------|------|------------|---------|----------|-----|------|
| Source Domain  | 49.45   | 52.97 |36.47   | 37.98|  38.65     |   41.65 |  29.54   |31.05| 32.16|
|     SN         | 58.66   | 61.87 |44.76   | 44.80|  45.95     |   49.34 |  30.47   |31.81| 33.25|
|     ST3D       | 70.06   | 74.63 |62.04   | 65.35|  53.92     |   58.19 |  34.65   |48.98| 37.03|
| Target Domain  | 78.63   | 81.63 |78.63   | 81.63|  78.63     |   81.63 |  78.51   |81.41| 71.75|

### 3D Multiobject tracking results on the car, truck, cyclist, and pedestrian.

#### Tracking result of the PC3T on the car class (IoU threshold = 0.5/0.7)
** The usage of the PC3T method refers to [this repository](https://github.com/hailanyi/3D-Multi-Object-Tracker)

|Detector   |sAMOTA↑    |   MOTA    |IDSW↓ | FRAG↓   |
|-----------|-----------|-----------|------|---------|
|PointRCNN  |80.70/65.67|72.46/51.45|27/19 |1198/2912|
|Pointpillar|88.23/70.06|78.91/55.18|80/57 |602/2932 |
|PVRCNN++   |88.30/74.49|75.56/57.42|158/75|664/2358 |
|Centerpoint|89.33/69.28|78.98/54.05|83/58 |727/3040 |

#### Tracking result of the PC3T on the truck class (IoU threshold = 0.5/0.7)

|Detector   | sAMOTA↑   |MOTA↑      | IDSW↓|FRAG↓  |
|-----------|-----------|-----------|------|-------|
|PointRCNN  |95.71/93.09|90.91/88.46| 10/7 |291/395|
|Pointpillar|97.97/95.34|92.93/91.41| 11/13|138/284|
|PVRCNN++   |95.58/95.04|86.23/84.73| 34/21|145/226|
|Centerpoint|95.42/94.50|92.00/89.42| 12/11|172/336|

#### Tracking result of the PC3T on the cyclist class (IoU threshold = 0.25/0.5)

|Detector   |sAMOTA↑    |MOTA↑      | IDSW↓|FRAG↓  |
|-----------|-----------|-----------|------|-------|
|PointRCNN  |63.43/53.21|46.33/38.42|19/16 |488/777|
|Pointpillar|54.37/37.05|41.04/25.77|9/6   |182/648|
|PVRCNN++   |68.23/58.27|50.60/40.97|48/38 |187/546|
|Centerpoint|77.02/64.56|60.45/46.87|17/14 |188/638|

#### Tracking result of the PC3T on the pedestrian class (IoU threshold = 0.25/0.5)

|Detector   |sAMOTA↑    |MOTA↑      |IDSW↓ |FRAG↓|
|-----------|-----------|-----------|------|-----|
|PointRCNN  |66.65/63.62|54.25/49.98|1/1   |44/53|
|Pointpillar|33.13/27.88|21.37/19.45|1/1   |19/32|
|PVRCNN++   |38.21/34.33|31.55/27.28|3/1   |20/35|
|Centerpoint|79.83/75.26|76.16/70.29|1/1   |11/56|

#### Tracking result of the AD3DMOT on the car class (IoU threshold = 0.5/0.7)

|Detector   |sAMOTA↑    |MOTA       |IDSW↓ |FRAG↓  |
|-----------|-----------|-----------|------|-------|
|PointRCNN  |60.97/50.27|41.56/33.77|10/13 |99/272 |
|Pointpillar|49.96/33.75|33.82/22.33|3/13  |64/379 |
|PVRCNN++   |63.00/52.65|43.22/34.12|126/82|177/349|
|Centerpoint|68.78/57.50|45.42/37.58|6/16  |70/267 |

#### Tracking result of the AD3DMOT on the truck class (IoU threshold = 0.5/0.7)

|Detector   |sAMOTA↑    |   MOTA↑   |IDSW↓|FRAG↓|
|-----------|-----------|-----------|-----|-----|
|PointRCNN  |59.89/56.59|39.73/37.06|1/1  |6/22 |
|Pointpillar|32.09/27.42|27.79/25.36|0/0  |4/24 |
|PVRCNN++   |31.39/28.54|27.71/25.75|3/3  |10/20|
|Centerpoint|67.38/62.03|63.48/59.30|5/4  |8/35 |

#### Tracking result of the AD3DMOT on the cyclist class (IoU threshold = 0.25/0.5)

|Detector   |sAMOTA↑    |MOTA↑      |IDSW↓|  FRAG↓ |
|-----------|-----------|-----------|-----|--------|
|PointRCNN  |74.81/60.34|63.25/44.45|12/6 |595/1834|
|Pointpillar|82.23/64.98|68.85/46.82|56/44|391/2166|
|PVRCNN++   |81.63/68.71|67.56/50.72|83/39|386/1560|
|Centerpoint|78.76/61.25|61.02/40.98|27/15|367/1720|

#### Tracking result of the AD3DMOT on the pedestrian class (IoU threshold = 0.25/0.5)

|Detector   |  sAMOTA↑  |   MOTA↑   |IDSW↓|FRAG↓|
|-----------|-----------|-----------|------|----|
|PointRCNN  |82.53/78.67|73.34/68.20|3/2|124/181|
|Pointpillar|82.18/76.79|75.26/70.33|9/8|80/182 |
|PVRCNN++   |81.50/77.20|69.15/64.53|9/8|76/141 |
|Centerpoint|81.44/76.11|71.89/65.85|7/7|70/207 |
## Citation
If you find InCo useful in your research or applications, please consider giving us a star 🌟 and citing it by the following BibTeX entry.
```shell
<p hidden>@inproceedings{zhang2024InCo,
  title={InCo: A New 3D Infrastructure-side Collaborative Perception Dataset based on Multiple LiDAR System},
  author={Zhang, Xiaofei and Li, Yining and Wang, Jinping and Qin, Xiangyi and Shen, Ying and Fan, Zhengping and Tan, Xiaojun},
  booktitle={Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI)},
  year={2024}
}这个段落应该被隐藏。</p>
```

## Acknowledgment
- [DAIR-V2X](https://github.com/AIR-THU/DAIR-V2X)
- [AB3DMOT](https://github.com/xinshuoweng/AB3DMOT)
- [PC3T](https://github.com/hailanyi/3D-Multi-Object-Tracker)
- [ST3D](https://github.com/CVMI-Lab/ST3D)
