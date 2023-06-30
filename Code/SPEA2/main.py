import os
import sys
import numpy as np

import argument as ARG
import data_reader as Reader
from tsp_problem import TspProblem
from tsp_spea2 import SPEA2

## 为什么权重向量都是一条线捏？
if __name__ == '__main__':
    files = ARG.DATA_FILE
    original_stdout = sys.stdout

    for file in files:
        print("[info] processing file: ",file)

        data_file = f"{ARG.DATA_FOLDER}{file}" # 原始数据位置
        file_name = file.split('.')[0] # 数据文件名
        result_folder = f"{ARG.RESULT_FOLDER}{file_name}/" # 设置结果保存位置
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        with open(f"{result_folder}{file_name}.log","w") as log_file:
            sys.stdout = log_file
            # 读取数据文件
            dim,_,dis_matrix,edge_weight_matrix = Reader.read_tsp_file(data_file)
            print(f"[info] pop:{ARG.POP}, dim:{dim}")
            
            problem = TspProblem(ARG.FUNC_NUM,dim,dis_matrix,edge_weight_matrix)
            spea2 = SPEA2(dim,problem,result_folder)
            spea2.run()
            sys.stdout = original_stdout
        spea2.save_result(text="final_result")
    print("[info] finish!")
    pass