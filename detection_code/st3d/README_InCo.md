# InCo transfer learning Benchmark
This is a reproduced benchmark about transfer learning for 3D object detection on the [InCo](我们的链接) dataset.

The code is mainly based on [ST3D](https://github.com/CVMI-Lab/ST3D).
## Benchmark
插入一些迁移学习的表格
## Installation
Please follow the [ST3D](https://github.com/CVMI-Lab/ST3D/blob/master/docs/INSTALL.md) installation instruction. 

## Getting Started
The dataset configs are located within [tools/cfgs/dataset_configs](./tools/cfgs/dataset_configs), and the model configs are located within tools/cfgs for different datasets.

### Dataset Prepareation
#### InCo Dataset
+ Please download the official [InCo](我们的链接) dataset and organize the dataset format according to Openpcdet's requirements for [custom](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/CUSTOM_DATASET_TUTORIAL.md) datasets as the following folder structure:
```
├── InCo
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


#### DAIR-V2X-I Dataset
+ Please follow the [instructions](https://github.com/AIR-THU/DAIR-V2X) to download the DAIR-V2X-I dataset and convert it to KITTI format. 
+ Generate the data infos by running the following command:
```python
python -m pcdet.datasets.dair.dair_dataset create_dair_infos tools/cfgs/dataset_configs/dair_dataset.yaml
```

#### KITTI Dataset
+ Please follow the [instructions](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d) to download the KITTI dataset. 
+ Generate the data infos by running the following command:
```python
python -m pcdet.datasets.kitti.kitti_dataset create_kitti_infos tools/cfgs/dataset_configs/kitti_dataset.yaml
```

#### ONCE Dataset
+ Please follow the [instructions](https://once-for-auto-driving.github.io/index.html) to download the ONCE dataset and convert. 
+ Generate the data infos by running the following command:
```python
python -m pcdet.datasets.once.once_dataset --func create_once_infos --cfg_file tools/cfgs/dataset_configs/once_dataset.yaml
```

### Pretrained Models
The `checkpoints` directory is located in [./ckpt](./ckpt). The pretrained models for four types of experiments are all included in this folder.
```
openpcdet
├── ckpt
│   ├── transfer_model
├── data
├── pcdet
├── tools
```
### Quick Demo
Please Please follow the [OpenPCDet](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/DEMO.md) quick demo instruction.

### Training & Testing
### Test and evaluate the pretrained models
* Test with a pretrained model: 
```shell script
python test.py --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE} --ckpt ${CKPT}
```

* To test all the saved checkpoints of a specific training setting and draw the performance curve on the Tensorboard, add the `--eval_all` argument: 
```shell script
python test.py --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE} --eval_all
```

* Notice that if you want to test on the setting with KITTI  as **target domain**, 
  please add `--set DATA_CONFIG_TAR.FOV_POINTS_ONLY True` to enable front view
  point cloud only: 
```shell script
python test.py --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE} --eval_all --set DATA_CONFIG_TAR.FOV_POINTS_ONLY True
```

* To test with multiple GPUs:
```shell script
sh scripts/dist_test.sh ${NUM_GPUS} \
    --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE}

# or

sh scripts/slurm_test_mgpu.sh ${PARTITION} ${NUM_GPUS} \ 
    --cfg_file ${CONFIG_FILE} --batch_size ${BATCH_SIZE}
```


### Train a model
You could optionally add extra command line parameters `--batch_size ${BATCH_SIZE}` and `--epochs ${EPOCHS}` to specify your preferred parameters. 
  

* Train with multiple GPUs or multiple machines
```shell script
sh scripts/dist_train.sh ${NUM_GPUS} --cfg_file ${CONFIG_FILE}

# or 

sh scripts/slurm_train.sh ${PARTITION} ${JOB_NAME} ${NUM_GPUS} --cfg_file ${CONFIG_FILE}
```

* Train with a single GPU:
```shell script
python train.py --cfg_file ${CONFIG_FILE}
```

### Train the Pre-trained 
Take Source Only model with Pointrcnn-IoU on InCo -> KITTI  as an example:
```shell script
sh scripts/dist_train.sh ${NUM_GPUS} --cfg_file cfgs/da-inco-kitti_models/pointrcnniou_origin.yaml \
    --batch_size ${BATCH_SIZE}
```
Notice that you need to select the **best model** as your Pre-train model, 
because the performance of adapted model is really unstable when target domain is KITTI format.


### Self-training Process
You need to set the `--pretrained_model ${PRETRAINED_MODEL}` when finish the
following self-training process.
```shell script
sh scripts/dist_train.sh ${NUM_GPUS} --cfg_file cfgs/da-inco-kitti_models/pointrcnniou_st3d++.yaml \
    --batch_size ${BATCH_SIZE} --pretrained_model ${PRETRAINED_MODEL}
```
Notice that you also need to focus the performance of the **best model**.
And I follow this [issue](https://github.com/CVMI-Lab/ST3D/issues/35) to use ST3D for InCo dataset.