import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import time
import sys
import os

import argument as ARG
import data_reader as Reader
import non_domination_sort_mod as Sort
import selection as Select
from function_evaluate import TSPEvaluator
from genetic_operator import Permutation_GeneOperator as GeneOperator

# ---常用变量---
POP  = ARG.POP # 种群数量
GEN  = ARG.GEN # 迭代次数
EVLN = ARG.EVLN # 目标函数数量
NAME = "" # 数据文件名称

# 初始化种群
# num: 种群数量 dim: 维度
def initialize_variables(num, dim, eval:TSPEvaluator):
    k = EVLN + dim; #K是数组的总元素个数。为了便于计算，决策变量和目标函数串在一起形成一个数组。  
    res = np.zeros((num,k))
    # 对于交叉和变异，利用目标变量对决策变量进行选择
    for i in range(0,num):
        # 为每个个体的所有决策变量在约束条件内随机取值
        # res[i][j]表示的是种群中第i个个体中的第j个决策变量
        res[i][0:dim] = list(range(1,dim+1))
        random.shuffle(res[i][0:dim])
        # 为了简化计算将对应的目标函数值储存在染色体的V + 1 到 K的位置。
        # print("[info]: res[i][dim+1:k]:",res[i][dim+1:k])
        res[i][dim:k] = eval.evaluate_objective(res[i])
    return res


## 保存当前结果
def save_checkpoint(iter,chromosome,result_folder,text=None):
    # 保存解集
    if text is None:
        csv_file = f"{result_folder}non_dominated_solution_{iter}.csv"
        pic_text = f"{NAME}, iter: {iter}"
        pic_file = f"{result_folder}pic_iter_{iter}.png"
    else:
        csv_file = f"{result_folder}{text}.csv"
        pic_text = f"{NAME}, {text}"
        pic_file = f"{result_folder}{text}_pic.png"

    best = chromosome[np.where(chromosome[:,-2]==1)]
    best_value = best[:,-4:-2]
    solution = np.hstack((best_value[:,:],best[:,0:-4]))
    csv_header = ["distance","profit","solution"]
    with open(csv_file,"w") as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerows(solution)
    # 画图
    plt.cla()
    plt.xlabel('Distance')
    plt.ylabel('Profit(*-1)')
    plt.title(pic_text)
    dis = chromosome[:,-4]
    pro = chromosome[:,-3]
    plt.plot(dis,pro,"o",c='black')
    dis = best[:,-4]
    pro = best[:,-3]
    plt.plot(dis,pro,"o",c='r')
    plt.draw()
    plt.savefig(pic_file)
    pass


# NSGA-II 优化主要流程
def nsga_ii_optimization(tsp_file, result_folder) :
    DIM,node_position,dis_matrix,edge_weight_matrix = Reader.read_tsp_file(f"{ARG.DATA_FOLDER}{tsp_file}")
    TSP_eval = TSPEvaluator(DIM,node_position,dis_matrix,edge_weight_matrix)

    TSP_GNO = GeneOperator(EVLN, DIM, TSP_eval)

    #用于计时
    time_start = time.time()
    chromosome = initialize_variables(POP, DIM, TSP_eval) #初始化种群
    chromosome = Sort.non_domination_sort(chromosome, EVLN, DIM) # 对初始化种群进行非支配快速排序和拥挤度计算
    
    for i in range(0,GEN+1):
        pool = round(POP/2) #round() 四舍五入取整 交配池大小
        parent_chromosome = Select.tournament_selection(chromosome, pool, ARG.TOUR) #竞标赛选择适合繁殖的父代


        offspring_chromosome = TSP_GNO.crossover_option(parent_chromosome)
        offspring_chromosome = TSP_GNO.mutate_option(offspring_chromosome)
        
        # 合并父代种群和子代种群
        intermediate_chromosome = np.vstack([parent_chromosome[:,0:DIM+EVLN],offspring_chromosome])

        intermediate_chromosome = Sort.non_domination_sort(intermediate_chromosome, EVLN, DIM) # 对新的种群进行快速非支配排序
        chromosome = Select.replace_chromosome(intermediate_chromosome, EVLN, DIM, POP) # 选择合并种群中前N个优先的个体组成新种群
        if i%10==0 and i>0:
            print(f'[info] {i} generations completed.')
            if i%ARG.SAVE_PIONT==0:
                save_checkpoint(i,chromosome,result_folder)

    time_end = time.time()
    print("experinced time: ",time_end-time_start," s.")
    # 输出最终解集
    save_checkpoint(0,chromosome,result_folder,"final_result")
    # with open(f"{result_folder}final_solution_set.csv","w") as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["number","solution","distance","weight"])
    #     for i in range(len(chromosome)):
    #         writer.writerow((i,chromosome[i][0:DIM],chromosome[i][DIM],chromosome[i][DIM+1]*-1))


if __name__ == '__main__':
    files = ARG.DATA_FILE
    original_stdout = sys.stdout

    for file in files:
        print("[info] processing file: ",file)
        file_name = file.split('.')[0]
        NAME = file_name
        result_folder = f"{ARG.RESULT_FOLDER}{file_name}/"
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        with open(f"{result_folder}{file_name}_log.txt","w") as log_file:
            sys.stdout = log_file
            nsga_ii_optimization(file, result_folder)
            sys.stdout = original_stdout

    print("finish!")
