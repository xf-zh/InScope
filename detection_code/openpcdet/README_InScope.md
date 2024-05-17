# InScope Benchmark
This is a reproduced benchmark for 3D object detection on the [InScope](我们的链接) dataset.

The code is mainly based on [OpenPCDet](https://github.com/open-mmlab/OpenPCDet).


## Installation
Please follow the [OpenPCDet](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/INSTALL.md) installation instruction.

## Getting Started
The dataset configs are located within [tools/cfgs/dataset_configs](./tools/cfgs/dataset_configs), and the model configs are located within tools/cfgs for different datasets.

### Dataset Prepareation
#### InScope Dataset
+ Please download the official [InScope](我们的链接) dataset and organize the dataset format according to Openpcdet's requirements for [custom](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/CUSTOM_DATASET_TUTORIAL.md) datasets as the following folder structure:
```
├── InScope
│   │── ImageSets
│   │   │── train.txt
│   │   │── val.txt
|   |   |—— test.txt
│   │── points
│   │   │── 000000.npy
│   │   │── 021416.npy
│   │── labels
│   │   │── 000000.txt
│   │   │── 021416.txt
```

+ Generate the data infos by running the following command:
```python
python -m pcdet.datasets.inscope.inscope_dataset create_inscope_infos tools/cfgs/dataset_configs/inscope_dataset.yaml
```
#### InScope_80 Dataset
Please download the official [InScope_80](我们的链接) dataset and organize the dataset format according to Openpcdet's requirements for [custom](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/CUSTOM_DATASET_TUTORIAL.md) datasets as the following folder structure:
```
├── InScope_80
│   │── ImageSets
│   │   │── train.txt
│   │   │── val.txt
|   |   |—— test.txt
│   │── points
│   │   │── 000000.npy
│   │   │── 021416.npy
│   │── labels
│   │   │── 000000.txt
│   │   │── 021416.txt
```
+ Generate the data infos by running the following command:
```python
python -m pcdet.datasets.inscope80.inscope80_dataset create_inscopr80_infos tools/cfgs/dataset_configs/inscope80_dataset.yaml
```
#### InScope_32 Dataset
Please download the official [InScope_32](我们的链接) dataset and organize the dataset format according to Openpcdet's requirements for [custom](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/CUSTOM_DATASET_TUTORIAL.md) datasets as the following folder structure:
```
├── InScope_32
│   │── ImageSets
│   │   │── train.txt
│   │   │── val.txt
|   |   |—— test.txt
│   │── points
│   │   │── 000000.npy
│   │   │── 021416.npy
│   │── labels
│   │   │── 000000.txt
│   │   │── 021416.txt
```
+ Generate the data infos by running the following command:
```python
python -m pcdet.datasets.inscope32.mlsy32_dataset create_inscope32_infos tools/cfgs/dataset_configs/inscope32_dataset.yaml
```
#### DAIR-V2X-I Dataset
+ Please follow the [instructions](https://github.com/AIR-THU/DAIR-V2X) to download the DAIR-V2X-I dataset and convert it to KITTI format. 
+ Generate the data infos by running the following command:
```python
python -m pcdet.datasets.dair.dair_dataset create_dair_infos tools/cfgs/dataset_configs/dair_dataset.yaml
```
### Pretrained Models
The `checkpoints` directory is located in [./ckpt](./ckpt). The pretrained models for four types of experiments are all included in this folder.
```
openpcdet
├── ckpt
│   ├── early_fusion
|   ├── lidar_32
|   ├── lidar_80
|   ├── middle_fusion
├── data
├── pcdet
├── tools
```
### Quick Demo
Please Please follow the [OpenPCDet](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/DEMO.md) quick demo instruction.

### Training & Testing
**1 Early Fusion**
***
The early fusion model configuration config file path is located at [./tools/cfgs/inscope_models](./tools/cfgs/inscope_models)

(1) Test and evaluate the pretrained models with early fusion
+ Test with a pretrained model:
```python
python test.py --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE} --ckpt ${CKPT} --save_to_file
```
+ To test all the saved checkpoints of a specific training setting and draw the performance curve on the Tensorboard, add the --eval_all argument:
```python
python test.py --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE} --eval_all --save_to_file
```

+ To test with multiple GPUs:
```shell script
sh scripts/dist_test.sh ${NUM_GPUS} --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE}
# or 
CUDA_VISIBLE_DEVICES=0,1 python -m torch.distributed.launch --nproc_per_node=2 test.py\
--cfg_file ${CONFIG_FILE} --launcher pytorch
```
(2) Train a model with early fusion

+ Train with a single GPU:
```python
python train.py --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE} --save_to_file
```
+ Train with multiple GPUs or multiple machines
```shell script
sh scripts/dist_train.sh ${NUM_GPUS} --cfg_file ${CONFIG_FILE}
# or 
CUDA_VISIBLE_DEVICES=0,1 python -m torch.distributed.launch --nproc_per_node=2 train.py\
--cfg_file ${CONFIG_FILE} --launcher pytorch
```
**2 Lidar 80**
***
The Lidar 80 model configuration config file path is located at [./tools/cfgs/inscope80_models](./tools/cfgs/inscope80_models).

***Tips:The training and testing instructions are similar to the early fusion commands***

**3 Lidar 32**
***
The Lidar 80 model configuration config file path is located at [./tools/cfgs/inscope32_models](./tools/cfgs/inscope32_models).

***Tips:The training and testing instructions are similar to the early fusion commands***

**4 Middle Fusion**
***
The middle fusion model configuration config file path is located at [./tools/cfgs/inscope_middlefusion_models](./tools/cfgs/inscope_middlefusion_models).

(1) Test and evaluate the pretrained models with middle fusion
+ Test with a pretrained model:
```python
python test_middle_fusion.py --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE} --ckpt ${CKPT} --save_to_file
```
+ To test all the saved checkpoints of a specific training setting and draw the performance curve on the Tensorboard, add the --eval_all argument:
```python
python test_middle_fusion.py --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE} --eval_all --save_to_file
```
(2) Train a model with middle fusion

+ Train with a single GPU:
```python
python train_middle_fusion.py --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE} --save_to_file
```

**5 Late Fusion**
***

+ Test with pretrained models:

```python
python test_late_fusion.py \
    --cfg_file_lidar0 ${CONFIG_FILE0} \
    --cfg_file_lidar1 ${CONFIG_FILE1} \
    --batch_size ${BATCH_SIZE} \
    --ckpt0 ${CKPT0} \
    --ckpt1 ${CKPT1}
```
