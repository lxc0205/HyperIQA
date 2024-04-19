import numpy as np
from scipy.stats import spearmanr, pearsonr
# Expand函数的Python实现
def expand_old(Mssim):
    Mssim_expand = np.hstack((
        Mssim, 
        Mssim**2, 
        np.sqrt(Mssim), 
        Mssim**3, 
        Mssim**(1/3), 
        np.log(Mssim), 
        np.power(2, Mssim), 
        np.exp(Mssim)
    ))
    return Mssim_expand

# x in [0, 1], y in [0, 1]
def expand(Mssim):
    Mssim_expand = np.hstack((
        Mssim, 
        Mssim**2, 
        np.sqrt(Mssim), 
        Mssim**3, 
        Mssim**(1/3), 
        np.log(Mssim+1) / np.log(2), 
        np.power(2, Mssim) - 1, 
        (np.exp(Mssim)-1) / (np.exp(1)-1)
    ))
    return Mssim_expand
def normalize_Mssim(Mssim, datasets):
    if datasets == 'csiq':
        limit = 1
    elif datasets == 'live':
        limit = 100
    elif datasets == 'tid2013':
        limit = 9
    elif datasets == 'koniq-10k':
        limit = 100
    else:
        print('wrong dataset name!')
    
    Mssim = Mssim / limit
    Mssim = np.where(Mssim < 0, 1e-4, Mssim)
    Mssim = np.where(Mssim > 1, 1, Mssim)
    return Mssim

def normalize_mos(scores, datasets, new_min=0, new_max=1):
    if datasets == 'csiq':
        old_min = 0 
        old_max = 1
        dmos = True
    elif datasets == 'live':
        old_min = 0
        old_max = 100
        dmos = True
    elif datasets == 'tid2013':
        old_min = 0
        old_max = 9
        dmos = False
    elif datasets == 'koniq-10k':
        old_min = 0
        old_max = 100
        dmos = False
    else:
        print('wrong dataset name!')
        return 0

    # 计算归一化后的分数
    if dmos:
        output_scores = [(1-((new_max - new_min) * (score - old_min) / (old_max - old_min) + new_min)) for score in scores]    # 如果是 Dmos，则将分数取反
    else:
        output_scores = [((new_max - new_min) * (score - old_min) / (old_max - old_min) + new_min) for score in scores]
    return output_scores

def calculate_sp(y, yhat):
    SROCC, _ = spearmanr(y, yhat)
    PLCC, _ = pearsonr(y, yhat)
    return SROCC, PLCC

def loadtxt(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines:
        fields = line.split('\t')[:-1]
        float_fields = [float(field) for field in fields]
        data.append(float_fields)
    data = np.array(data)
    return data
def loaddata(file_path, dataset, pretrained_dataset):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines:
        fields = line.split('\t')[:-1]
        float_fields = [float(field) for field in fields]
        data.append(float_fields)
    data = np.array(data)
    
    mos = data[:, -1]
    Mssim = data[:, :-1]

    # 预处理
    Mssim = normalize_Mssim(Mssim, pretrained_dataset) # 归一化到0-1
    Mssim = expand(Mssim) # 用函数集扩充 Mssim
    mos = normalize_mos(mos, dataset) # 归一化到0-1
    mos = np.array(mos)
    mos = mos[:, np.newaxis]

    return Mssim, mos

def savedata(file, vector, label):
    for i in range(len(vector)):
        file.write(str(vector[i]))
        file.write('\t')
    file.write(str(label))
    file.write('\t')
    file.write('\n')

def sort(data, order, row):
    if order:
        sorted_indices = np.argsort(data[:, row], axis=0, kind='mergesort')
    else:
        sorted_indices = np.argsort(data[:, row], axis=0, kind='mergesort')[::-1]
    sorted_indices = sorted_indices.reshape(-1, 1)
    sorted_indices = np.tile(sorted_indices, (1, data.shape[1]))
    sorted_matrix = np.take_along_axis(data, sorted_indices, axis=0)
    return sorted_matrix

folder_path = {
    'live': './Database/LIVE/',
    'csiq': './Database/CSIQ/',
    'tid2013': './Database/TID2013/',
    'livec': './Database/ChallengeDB_release/ChallengeDB_release/',
    'koniq-10k': './Database/koniq-10k/',
    'bid': './Database/BID/',
}

img_num = {
    'live': list(range(0, 29)),
    'csiq': list(range(0, 30)),
    'tid2013': list(range(0, 25)),
    'livec': list(range(0, 1162)),
    'koniq-10k': list(range(0, 10073)),
    'bid': list(range(0, 586)),
}



