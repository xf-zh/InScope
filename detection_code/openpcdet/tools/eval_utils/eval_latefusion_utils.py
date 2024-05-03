import pickle
import time
import copy

import numpy as np
import torch
import tqdm

from pcdet.models import load_data_to_gpu
from pcdet.utils import common_utils


def statistics_info(cfg, ret_dict, metric, disp_dict):
    for cur_thresh in cfg.MODEL.POST_PROCESSING.RECALL_THRESH_LIST:
        metric['recall_roi_%s' % str(cur_thresh)] += ret_dict.get('roi_%s' % str(cur_thresh), 0)
        metric['recall_rcnn_%s' % str(cur_thresh)] += ret_dict.get('rcnn_%s' % str(cur_thresh), 0)
    metric['gt_num'] += ret_dict.get('gt', 0)
    min_thresh = cfg.MODEL.POST_PROCESSING.RECALL_THRESH_LIST[0]
    disp_dict['recall_%s' % str(min_thresh)] = \
        '(%d, %d) / %d' % (metric['recall_roi_%s' % str(min_thresh)], metric['recall_rcnn_%s' % str(min_thresh)], metric['gt_num'])

def iou_match(boxes, query_boxes, criterion, scores0, scores1):
    N = boxes.shape[0]
    K = query_boxes.shape[0]
    overlaps = np.zeros((K, N, 3))
    for k in range(K):
        qbox_area = ((query_boxes[k, 2] - query_boxes[k, 0]) *
                     (query_boxes[k, 3] - query_boxes[k, 1]))
        for n in range(N):
            iw = (min(boxes[n, 2], query_boxes[k, 2]) -
                  max(boxes[n, 0], query_boxes[k, 0]))
            ih = (min(boxes[n, 3], query_boxes[k, 3]) -
                  max(boxes[n, 1], query_boxes[k, 1]))
            if iw > 0 and ih > 0:
                if criterion == -1:
                    ua = (
                        (boxes[n, 2] - boxes[n, 0]) *
                        (boxes[n, 3] - boxes[n, 1]) + qbox_area - iw * ih)
                elif criterion == 0:
                    ua = ((boxes[n, 2] - boxes[n, 0]) *
                            (boxes[n, 3] - boxes[n, 1]))
                elif criterion == 1:
                    ua = qbox_area
                else:
                    ua = 1.0
                overlaps[k, n, 0] = iw * ih / ua
                overlaps[k, n, 1] = scores0[n]
                overlaps[k, n, 2] = scores1[k]
            else:
                overlaps[k, n, 0] = None
                overlaps[k, n, 1] = None
                overlaps[k, n, 2] = scores1[k]
    return overlaps

def translate_boxes_to_bev(boxes):
    '''
    input: N x 6, center + lwh
    return: N x 4, xyxy
    '''
    center, lwh = boxes[:, :3], boxes[:, 3:]
    bev_min = center[:, :2] - lwh[:, :2] / 2.0
    bev_max = center[:, :2] + lwh[:, :2] / 2.0
    bbox_bev = np.concatenate((bev_min, bev_max), axis=1)
    return bbox_bev

def eval_one_epoch(cfg, args, model, dataloader, epoch_id, logger, dist_test=False, result_dir=None):
    result_dir.mkdir(parents=True, exist_ok=True)

    final_output_dir = result_dir / 'final_result' / 'data'
    if args.save_to_file:
        final_output_dir.mkdir(parents=True, exist_ok=True)

    metric = {
        'gt_num': 0,
    }
    for cur_thresh in cfg.MODEL.POST_PROCESSING.RECALL_THRESH_LIST:
        metric['recall_roi_%s' % str(cur_thresh)] = 0
        metric['recall_rcnn_%s' % str(cur_thresh)] = 0

    dataset = dataloader.dataset
    class_names = dataset.class_names
    det_annos = []

    if getattr(args, 'infer_time', False):
        start_iter = int(len(dataloader) * 0.1)
        infer_time_meter = common_utils.AverageMeter()

    logger.info('*************** EPOCH %s EVALUATION *****************' % epoch_id)
    if dist_test:
        num_gpus = torch.cuda.device_count()
        local_rank = cfg.LOCAL_RANK % num_gpus
        model = torch.nn.parallel.DistributedDataParallel(
                model,
                device_ids=[local_rank],
                broadcast_buffers=False
        )
    model.eval()

    if cfg.LOCAL_RANK == 0:
        progress_bar = tqdm.tqdm(total=len(dataloader), leave=True, desc='eval', dynamic_ncols=True)
    start_time = time.time()
    for i, batch_dict in enumerate(dataloader):
        load_data_to_gpu(batch_dict)

        if getattr(args, 'infer_time', False):
            start_time = time.time()

        with torch.no_grad():
            pred_dicts, ret_dict = model(batch_dict)

        disp_dict = {}

        if getattr(args, 'infer_time', False):
            inference_time = time.time() - start_time
            infer_time_meter.update(inference_time * 1000)
            # use ms to measure inference time
            disp_dict['infer_time'] = f'{infer_time_meter.val:.2f}({infer_time_meter.avg:.2f})'

        statistics_info(cfg, ret_dict, metric, disp_dict)
        annos = dataset.generate_prediction_dicts(
            batch_dict, pred_dicts, class_names,
            output_path=final_output_dir if args.save_to_file else None
        )
        det_annos += annos
        if cfg.LOCAL_RANK == 0:
            progress_bar.set_postfix(disp_dict)
            progress_bar.update()

    if cfg.LOCAL_RANK == 0:
        progress_bar.close()

    if dist_test:
        rank, world_size = common_utils.get_dist_info()
        det_annos = common_utils.merge_results_dist(det_annos, len(dataset), tmpdir=result_dir / 'tmpdir')
        metric = common_utils.merge_results_dist([metric], world_size, tmpdir=result_dir / 'tmpdir')

    logger.info('*************** Performance of EPOCH %s *****************' % epoch_id)
    sec_per_example = (time.time() - start_time) / len(dataloader.dataset)
    logger.info('Generate label finished(sec_per_example: %.4f second).' % sec_per_example)

    if cfg.LOCAL_RANK != 0:
        return {}

    ret_dict = {}
    if dist_test:
        for key, val in metric[0].items():
            for k in range(1, world_size):
                metric[0][key] += metric[k][key]
        metric = metric[0]

    gt_num_cnt = metric['gt_num']
    for cur_thresh in cfg.MODEL.POST_PROCESSING.RECALL_THRESH_LIST:
        cur_roi_recall = metric['recall_roi_%s' % str(cur_thresh)] / max(gt_num_cnt, 1)
        cur_rcnn_recall = metric['recall_rcnn_%s' % str(cur_thresh)] / max(gt_num_cnt, 1)
        logger.info('recall_roi_%s: %f' % (cur_thresh, cur_roi_recall))
        logger.info('recall_rcnn_%s: %f' % (cur_thresh, cur_rcnn_recall))
        ret_dict['recall/roi_%s' % str(cur_thresh)] = cur_roi_recall
        ret_dict['recall/rcnn_%s' % str(cur_thresh)] = cur_rcnn_recall

    total_pred_objects = 0
    for anno in det_annos:
        total_pred_objects += anno['name'].__len__()
    logger.info('Average predicted number of objects(%d samples): %.3f'
                % (len(det_annos), total_pred_objects / max(1, len(det_annos))))

    with open(result_dir / 'result.pkl', 'wb') as f:
        pickle.dump(det_annos, f)

    result_str, result_dict = dataset.evaluation(
        det_annos, class_names,
        eval_metric=cfg.MODEL.POST_PROCESSING.EVAL_METRIC,
        output_path=final_output_dir
    )

    logger.info(result_str)
    ret_dict.update(result_dict)

    logger.info('Result is saved to %s' % result_dir)
    logger.info('****************Evaluation done.*****************')
    return ret_dict

def eval_one_epoch_lfus(cfg, args, model, dataloader, epoch_id, logger, dist_test=False, result_dir=None):
    result_dir.mkdir(parents=True, exist_ok=True)

    final_output_dir = result_dir / 'final_result' / 'data'
    if args.save_to_file:
        final_output_dir.mkdir(parents=True, exist_ok=True)

    metric = {
        'gt_num': 0,
    }
    for cur_thresh in cfg.MODEL.POST_PROCESSING.RECALL_THRESH_LIST:
        metric['recall_roi_%s' % str(cur_thresh)] = 0
        metric['recall_rcnn_%s' % str(cur_thresh)] = 0

    dataset, dataloader_iters = {}, {}
    for key in args.model_keys:
        dataset[key] = dataloader[key].dataset
        class_names = dataset[key].class_names
        dataloader_iters[key] = iter(dataloader[key])

        if getattr(args, 'infer_time', False):
            start_iter = int(len(dataloader[key]) * 0.1)
            infer_time_meter = common_utils.AverageMeter()

        logger.info('*************** EPOCH %s EVALUATION *****************' % epoch_id)
        model[key].eval()

        if cfg.LOCAL_RANK == 0:
            total_eval = len(dataloader[key])
            progress_bar = tqdm.tqdm(total=total_eval, leave=True, desc='eval', dynamic_ncols=True)
    
    start_time = time.time()

    det_annos = []
    # key = 'lidar0'
    # for i, batch_dict in enumerate(dataloader[key]):
    #     load_data_to_gpu(batch_dict)

    #     if getattr(args, 'infer_time', False):
    #         start_time = time.time()

    #     with torch.no_grad():
    #         pred_dicts, ret_dict = model[key](batch_dict)
    
    batch_dict = {}
    for s in range(total_eval):
        pred_fus = []
        for key in args.model_keys:
        # for key in ['lidar0']:
            batch_dict[key] = next(dataloader_iters[key])
            load_data_to_gpu(batch_dict[key])

            with torch.no_grad():
                pred_dicts, ret_dict = model[key](batch_dict[key])
                pred_fus.append(pred_dicts)
        
        # vote
        pred_fus_dict = copy.deepcopy(pred_fus[0])
        # pred_fus_dict = pred_fus[0]

        for b in range(args.batch_size):
            boxes_bev = {
                0: translate_boxes_to_bev(pred_fus[0][b]['pred_boxes'].cpu().numpy()),
                1: translate_boxes_to_bev(pred_fus[1][b]['pred_boxes'].cpu().numpy()),
            }
            overlaps = iou_match(
                boxes_bev[0],
                boxes_bev[1],
                -1,
                pred_fus[0][b]['pred_scores'].cpu().numpy(),
                pred_fus[1][b]['pred_scores'].cpu().numpy()
            )
            matched_ind = np.column_stack(np.where(overlaps[:, :, 0] > 0.7))    # k, n
            create = np.all(np.isnan(overlaps[:, :, 0]), axis=1)
            create = np.where(create)[0]

            for i in range(matched_ind.shape[0]):
                n = matched_ind[i][1]
                k = matched_ind[i][0]
                if pred_fus[0][b]['pred_scores'][n] < pred_fus[1][b]['pred_scores'][k]:
                    pred_fus_dict[b]['pred_boxes'][n, :] = pred_fus[1][b]['pred_boxes'][k, :]
                    pred_fus_dict[b]['pred_scores'][n] = pred_fus[1][b]['pred_scores'][k]
                    pred_fus_dict[b]['pred_labels'][n] = pred_fus[1][b]['pred_labels'][k]
            
            for i in range(create.shape[0]):
                k = create[i]
                pred_fus_dict[b]['pred_boxes'] = torch.cat((pred_fus_dict[b]['pred_boxes'], 
                                                            pred_fus[1][b]['pred_boxes'][k, :].view(1, -1)), dim=0)
                pred_fus_dict[b]['pred_scores'] = torch.cat((pred_fus_dict[b]['pred_scores'], 
                                                            pred_fus[1][b]['pred_scores'][k].view(1)), dim=0)
                pred_fus_dict[b]['pred_labels'] = torch.cat((pred_fus_dict[b]['pred_labels'], 
                                                            pred_fus[1][b]['pred_labels'][k].view(1)), dim=0)
        # end vote

        disp_dict = {}

        if getattr(args, 'infer_time', False):
            inference_time = time.time() - start_time
            infer_time_meter.update(inference_time * 1000)
            # use ms to measure inference time
            disp_dict['infer_time'] = f'{infer_time_meter.val:.2f}({infer_time_meter.avg:.2f})'

        statistics_info(cfg, ret_dict, metric, disp_dict)
        annos = dataset[args.model_keys[0]].generate_prediction_dicts(
            batch_dict[args.model_keys[0]], pred_fus_dict, class_names,
            output_path=final_output_dir if args.save_to_file else None
        )
        det_annos += annos
        if cfg.LOCAL_RANK == 0:
            progress_bar.set_postfix(disp_dict)
            progress_bar.update()

    if cfg.LOCAL_RANK == 0:
        progress_bar.close()

    if dist_test:
        rank, world_size = common_utils.get_dist_info()
        det_annos = common_utils.merge_results_dist(det_annos, len(dataset[args.model_keys[0]]), tmpdir=result_dir / 'tmpdir')
        metric = common_utils.merge_results_dist([metric], world_size, tmpdir=result_dir / 'tmpdir')

    logger.info('*************** Performance of EPOCH %s *****************' % epoch_id)
    sec_per_example = (time.time() - start_time) / len(dataloader[args.model_keys[0]].dataset)
    logger.info('Generate label finished(sec_per_example: %.4f second).' % sec_per_example)

    if cfg.LOCAL_RANK != 0:
        return {}

    ret_dict = {}
    if dist_test:
        for key, val in metric[0].items():
            for k in range(1, world_size):
                metric[0][key] += metric[k][key]
        metric = metric[0]

    gt_num_cnt = metric['gt_num']
    for cur_thresh in cfg.MODEL.POST_PROCESSING.RECALL_THRESH_LIST:
        cur_roi_recall = metric['recall_roi_%s' % str(cur_thresh)] / max(gt_num_cnt, 1)
        cur_rcnn_recall = metric['recall_rcnn_%s' % str(cur_thresh)] / max(gt_num_cnt, 1)
        logger.info('recall_roi_%s: %f' % (cur_thresh, cur_roi_recall))
        logger.info('recall_rcnn_%s: %f' % (cur_thresh, cur_rcnn_recall))
        ret_dict['recall/roi_%s' % str(cur_thresh)] = cur_roi_recall
        ret_dict['recall/rcnn_%s' % str(cur_thresh)] = cur_rcnn_recall

    total_pred_objects = 0
    for anno in det_annos:
        total_pred_objects += anno['name'].__len__()
    logger.info('Average predicted number of objects(%d samples): %.3f'
                % (len(det_annos), total_pred_objects / max(1, len(det_annos))))

    with open(result_dir / 'result.pkl', 'wb') as f:
        pickle.dump(det_annos, f)

    result_str, result_dict = dataset[args.model_keys[0]].evaluation(
        det_annos, class_names,
        eval_metric=cfg.MODEL.POST_PROCESSING.EVAL_METRIC,
        output_path=final_output_dir
    )

    logger.info(result_str)
    ret_dict.update(result_dict)

    logger.info('Result is saved to %s' % result_dir)
    logger.info('****************Evaluation done.*****************')
    return ret_dict

if __name__ == '__main__':
    pass
