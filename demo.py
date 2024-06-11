import os
import argparse
import data_loader
import numpy as np
from tqdm import tqdm
from iqa import IQA
from utils import expand, calculate_sp, normalize_Mssim, normalize_mos, folder_path, img_num

def main(config):
    print('Testing demo.')

    method = IQA(config.pretrained_dataset)
    dataLoader = data_loader.DataLoader(config.dataset, folder_path[config.dataset], img_num[config.dataset], config.patch_size, config.patch_num, istrain=False)
    data = dataLoader.get_data()

    Mssim = []

    mos = []
    for img, label in tqdm(data):
        layer_scores, _ = method.UIC_IQA(img)
        Mssim.append(np.array(layer_scores))
        mos.append(label.numpy())
    Mssim = np.array(Mssim)
    mos = np.array(mos)

    # 预处理
    Mssim = normalize_Mssim(Mssim, config.pretrained_dataset) # 归一化到0-1
    Mssim = expand(Mssim) # 用函数集扩充 Mssim
    mos = normalize_mos(mos, config.dataset) # 归一化到0-1
    mos = mos[:, np.newaxis]

    ########## Determined by CURD, Assert no = 7 ##########
    # ----index----   sw    -------beta-------    srcc   plcc     (srcc + plcc)/2
    # beta = [15969.875, 4326.625, 883.921875, 1.0262349247932434, -278.994140625, -30607.75, 9705.1875]
    # index = [1, 7, 19, 30, 31, 37, 43]

    beta = [3.324539993639519,13.125284559431748,0.8595986471534047,-12.530279544116638,-68.34548125360743,-8.317460779137036,28.50518866092898]
    index = [7,10,18,21,23,26,41]

    Mssim_s = Mssim[:, index]
    yhat = Mssim_s @ beta

    srcc, plcc = calculate_sp(mos.squeeze(), yhat.squeeze())
    print(f'Testing SRCC {srcc},\tPLCC {plcc}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', dest='dataset', type=str, default='csiq', help='Support datasets: koniq-10k|live|csiq|tid2013')
    parser.add_argument('--pretrained_dataset', dest='pretrained_dataset', type=str, default='koniq-10k', help='Support datasets: koniq-10k|live|csiq|tid2013')
    parser.add_argument('--patch_num', dest='patch_num', type=int, default=1, help='Number of sample patches from testing image')
    parser.add_argument('--patch_size', dest='patch_size', type=int, default=224, help='Crop size for training & testing image patches')
    config = parser.parse_args()

    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    main(config)