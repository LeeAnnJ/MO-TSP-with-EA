'''
对得出结果进行评估
'''
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances

DATA_FILE = ["bayg29","bays29","dantzig42","gr120","pa561"] # ["bayg29","bays29","dantzig42","gr120","pa561"]
MAX_ITER = [200,200,1000,2000,2000] # 结果文件中的最大评估次数
CHECK_POINT = [10,10,50,100,100]
SPEA_RESULT_FOLDER = "../result/SPEA2/" # SPEA2结果文件夹
NSGA_RESULT_FOLDER = "../result/NSGA-II/" # NSGA-II结果文件夹
EVAL_RESULT_FOLDER = "../result/evaluate/" # 性能评估结果文件夹
CSV_HEADER=["iter","IGD","HV","Spacing"] #csv数据文件头


# 计算反世代距离 IGD
def calculate_igd(reference_set, solution_set):
    # 计算每个解到参考集的最小距离
    distances = pairwise_distances(solution_set, reference_set).min(axis=0)
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
        hypervolume += (reference_point[0]-point[0]) * (last_point[1]-point[1])
        last_point = point
    return hypervolume

# 计算分散值 使用Spacing指标
def calculate_diversity(solution_set):
    num_solutions = len(solution_set)
    # 计算解集中解之间的平均距离
    distances = pairwise_distances(solution_set)
    np.fill_diagonal(distances, np.inf)
    min_distances = np.min(distances, axis=1)
    average_distance = np.mean(min_distances)
    # spacing指标
    spacing = np.sqrt(np.sum((min_distances-average_distance)**2) / (num_solutions-1))
    return spacing


# 获取单个csv文件中解集的函数值
def get_csv_result(result_file):
    data_frame = pd.read_csv(result_file,header=None,skiprows=[0])
    data = data_frame.values
    return data[:,0:2]


# 获取一个算法的 所有解集 和 理想点
def get_algorithm_result(result_folder,check_iter,max_eval):
    result_set = []
    dmin = np.inf
    pmin = dmax = 0
    pmax = -np.inf
    for i in range(check_iter,max_eval+1,check_iter):
        result_file = f"{result_folder}non_dominated_solution_{i}.csv"
        func = get_csv_result(result_file)
        result_set.append(func)
        [cur_dmin,cur_pmin] = np.min(func,axis=0)
        [cur_dmax,cur_pmax] = np.max(func,axis=0)
        dmin = min(cur_dmin,dmin)
        pmin = min(cur_pmin,pmin)
        dmax = max(cur_dmax,dmax)
        pmax = max(cur_pmax,pmax)
    igd_ref = [dmin,pmin]
    hv_ref = [dmax+1,pmax+1]
    return result_set, igd_ref, hv_ref


# 对一个算法的 一个数据集 的结果进行评估
# csv数据格式：[迭代次数, IGD数据, HV数据, spcaing数据]
def evaluate_single(result_set,igd_ref,hv_ref,iter,eval_folder,method):
    print("[info] method:",method)
    igd_set = []
    hv_set = []
    dv_set = []
    for result in result_set:
        igd = calculate_igd(result,np.array([igd_ref]))
        hv = calculate_hypervolume(result,hv_ref)
        dv = calculate_diversity(result)
        igd_set.append(igd)
        hv_set.append(hv)
        dv_set.append(dv)
    eval_set = np.array([iter,igd_set,hv_set,dv_set]).T
    #输出csv文件
    csv_name = f"{eval_folder}eval_result_{method}.csv"
    with open(csv_name,"w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(CSV_HEADER)
        writer.writerows(eval_set)
    return eval_set

# 将两个方法的评估数值画在一张图上
# y1为nsgaII数据，y2为spea2数据
def draw(x,y1,y2,yname,save_folder):
    plt.cla()
    plt.xlabel("iter")
    plt.ylabel(yname)
    plt.title(f"evaluate: {yname}")
    plt.plot(x,y1,"-o",label="NSGA-II",color="red")
    plt.plot(x,y2,"-o",label="SPEA2",color="blue")
    plt.legend(loc='upper right')
    plt.savefig(f"{save_folder}eval_{yname}_pic.png")

# 对两个方法进行比较
def evaluate_genereal(file_name,max_eval,check_iter):
    nsga_result_folder = f"{NSGA_RESULT_FOLDER}{file_name}/"
    spea_result_folder = f"{SPEA_RESULT_FOLDER}{file_name}/"
    eval_folder = f"{EVAL_RESULT_FOLDER}{file_name}/"
    if not os.path.exists(eval_folder):
        os.makedirs(eval_folder)

    iter = list(range(check_iter,max_eval+1,check_iter))
    nsga_result_set,n_igd_ref,n_hv_ref = get_algorithm_result(nsga_result_folder,check_iter,max_eval)
    spea_result_set,s_igd_ref,s_hv_ref = get_algorithm_result(spea_result_folder,check_iter,max_eval)
    igd_ref = np.min([n_igd_ref,s_igd_ref],axis=0)
    hv_ref = np.max([n_hv_ref,s_hv_ref],axis=0)
    nsga_eval = evaluate_single(nsga_result_set,igd_ref,hv_ref,iter,eval_folder,"NSGA")
    spea_eval = evaluate_single(spea_result_set,igd_ref,hv_ref,iter,eval_folder,"SPEA")
    iter = nsga_eval[:,0]
    # 开始画图
    draw(iter,nsga_eval[:,1],spea_eval[:,1],"IGD",eval_folder)
    draw(iter,nsga_eval[:,2],spea_eval[:,2],"HV",eval_folder)
    draw(iter,nsga_eval[:,3],spea_eval[:,3],"Spacing",eval_folder)
    pass


def test():
    func = get_csv_result("../result/NSGA-II/bayg29/non_dominated_solution_20.csv")
    print(func)
    print(type(func[0][0])," ",type(func[0][1]))
    print(func.shape)
    pass


if __name__ == '__main__':
    if not os.path.exists(EVAL_RESULT_FOLDER):
        os.makedirs(EVAL_RESULT_FOLDER)
    for i in range(len(DATA_FILE)):
        file_name = DATA_FILE[i]
        max_eval = MAX_ITER[i]
        check_point = CHECK_POINT[i]
        print("[info] procsccing dataset: ",file_name)
        evaluate_genereal(file_name,max_eval,check_point)
    pass