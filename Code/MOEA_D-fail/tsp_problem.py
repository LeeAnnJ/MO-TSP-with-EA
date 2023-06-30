import numpy as np
import random
from moead_framework.problem.problem import Problem


class TspProblem(Problem):
    dimention = 0 # 决策变量个数 
    func_num = 2 # 目标函数个数
    distance = [] # 节点间距离
    edge_weight = [] # 边权重

    def __init__(self):
        self.V = 0
        super().__init__(objective_number=2)

    def __init__ (self,M=2,V=0, dis_matrix=np.array([]), edge_weight=np.array([])):
        self.dimention = V
        self.func_num = M
        self.distance = dis_matrix # 节点距离
        self.edge_weight = edge_weight # 边权重
        super().__init__(objective_number=M)
    
    def f(self, function_id, decision_vector):
        if not isinstance(function_id,int):
            raise TypeError("The expected type of `function_id` is `int`")
        if not isinstance(decision_vector, np.ndarray):
            raise TypeError("The expected type of `decision_vector` is `np.ndarray`")
        
        fit = 0
        # print("[info]: decision vector in f: ",decision_vector)
        if function_id==0: ## 路径长度
            for i in range(0,self.V-1):
                fit += self.distance[int(decision_vector[i])][int(decision_vector[i+1])]
            fit += self.distance[int(decision_vector[self.dimention-1])][int(decision_vector[0])]
        elif function_id==1: ## 边权重
            for i in range(0,self.V-1):
                fit += self.edge_weight[int(decision_vector[i])][int(decision_vector[i+1])]
            fit += self.edge_weight[int(decision_vector[self.dimention-1])][int(decision_vector[0])]
            fit *= -1
        return fit


    def generate_random_solution(self):
        res = np.zeros(self.V)
        res = list(range(1,self.V+1))
        random.shuffle(res)
        # print("[info]: res in generate_random_solution:",res)
        ## return Solution
        return self.evaluate(x=res)
