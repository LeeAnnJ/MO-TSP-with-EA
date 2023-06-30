'''
对得出结果进行评估
'''
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances

DATA_FILE = ["gr120.tsp","pa561.tsp"] # ["bayg29.tsp","bays29.tsp","dantzig42.tsp","gr120.tsp","pa561.tsp"]
SPEA_RESULT_FOLDER = "../result/SPEA/" # SPEA2结果文件夹
NSGA_RESULT_FOLDER = "../result/NSGA-II/" # NSGA-II结果文件夹
EVAL_RESULT_FOLDER = "../result/evaluate/" # 性能评估结果文件夹
max_iter = [100,100,500,1000,1000]
check_point = [10,10,50,100,100]


# 计算反世代距离 IGD
def calculate_igd(reference_set, solution_set):
    # 计算每个解到参考集的最小距离
    distances = pairwise_distances(solution_set, reference_set).min(axis=1)
    # 计算IGD值
    igd = distances.mean()
    return igd

# 计算超体积 HV
def calculate_hypervolume(solution_set, reference_point):
    # 按照第一个目标函数值进行排序
    sorted_set = sorted(solution_set, key=lambda x: x[0])
    # 计算超体积
    hypervolume = 0.0
    last_point = reference_point
    for point in sorted_set:
        hypervolume += (point[0] - last_point[0]) * (point[1] - reference_point[1])
        last_point = point
    return hypervolume

# 计算分散值
def calculate_diversity(solution_set):
    # 计算解集中解之间的平均距离
    distances = pairwise_distances(solution_set)
    diversity = distances.mean()
    return diversity

# 获取单个csv文件中解集的函数值
def get_csv_result(result_file):
    data_frame = pd.read_csv(result_file,header=None,skiprows=[0])
    data = data_frame.values
    return data[:,0:2]

if __name__ == '__main__':
    func = get_csv_result("../result/NSGA-II/bayg29/non_dominated_solution_10.csv")
    print(func[0][1])
    pass