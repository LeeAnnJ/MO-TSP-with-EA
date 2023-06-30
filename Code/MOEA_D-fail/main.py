from moead_framework.aggregation.tchebycheff import Tchebycheff
from moead_framework.tool.result import save_population_full
from matplotlib import pyplot as plt
import numpy as np
import csv
import time
import sys
import os

from tsp_gene_operate import TspGeneOperator
import argument as ARG
import data_reader as Reader
from tsp_problem import TspProblem
from tsp_moead import TspMoead

## 保存迭代过程的数据
def checkpoint(algorithm:TspMoead):
    if algorithm.current_eval%10==0:
        print(f"[info]: {algorithm.current_eval} iteration finished")
        if algorithm.current_eval%ARG.SAVE_PIONT==0: 
            filename = f"{algorithm.result_folder}non_dominated_solutions_{algorithm.current_eval}.txt"
            save_population_full(file_name=filename,population=algorithm.ep)

if __name__ == '__main__':
    files = ARG.DATA_FILE
    original_stdout = sys.stdout

    for file in files:
        print("[info] processing file: ",file)
        
        data_file = f"{ARG.DATA_FOLDER}{file}"
        file_name = file.split('.')[0]
        weight_file = f"{ARG.DATA_FOLDER}{file_name}_weight.txt"
        result_folder = f"{ARG.RESULT_FOLDER}{file_name}/"
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        with open(f"{result_folder}{file_name}_log.txt","w") as log_file:
            sys.stdout = log_file
            dim,node_position,dis_matrix,edge_weight_matrix = Reader.read_tsp_file(data_file)
            if ARG.REWRITE_WEIGHT:
                weight_list = Reader.write_weight_file(ARG.POP,ARG.M,weight_file)
            else:
                weight_list = np.loadtxt(fname=weight_file)
            # problem = TspProblem(ARG.M,dim,weight_list)
            problem = TspProblem(ARG.M,dim,dis_matrix,edge_weight_matrix)
            moead = TspMoead(problem=problem,
                            result_folder=result_folder,
                            max_evaluation=ARG.EVAL_TIME,
                            number_of_weight_neighborhood=ARG.NEIGHBOR,
                            aggregation_function=Tchebycheff,
                            weight_file=weight_file,
                            genetic_operator=TspGeneOperator)
            
            # 开始进行优化并计时
            time_start = time.time()
            list_of_solutions =  moead.run(checkpoint=checkpoint)
            time_end = time.time()
            print("[info] exprinced time: ",time_end-time_start," s")
            sys.stdout = original_stdout
        
        pareto_front = []
        pareto_set = []
        for solution_object in list_of_solutions:
            pareto_front.append(solution_object.F)
            pareto_set.append(solution_object.decision_vector)
        # 记录最终解集
        with open(f"{result_folder}final_solution_set.csv","w") as sol_file:
            writer = csv.writer(sol_file)
            writer.writerows(pareto_set)
        # 绘制帕累托前沿
        data = np.array([pareto_front])
        x,y = data.T
        plt.xlabel('Distance')
        plt.ylabel('Profit(*-1)')
        plt.scatter(x,y)
        plt.draw()
        plt.savefig(f"{result_folder}pareto_front.png")
    
    print("[info] finish!")