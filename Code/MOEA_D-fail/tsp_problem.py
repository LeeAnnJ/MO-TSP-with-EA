import numpy as np
import random
from moead_framework.problem.problem import Problem


class TspProblem(Problem):
    # M:目标函数个数 V:决策变量个数
    def __init__(self):
        self.V = 0
        super().__init__(objective_number=2)

    def __init__ (self,M=2,V=0,weight_list=np.array([])):
        self.V = V
        self.weight_list = weight_list ## 权重向量
        super().__init__(objective_number=M)
    
    def f(self, function_id, decision_vector):
        if not isinstance(function_id,int):
            raise TypeError("The expected type of `function_id` is `int`")
        if not isinstance(decision_vector, np.ndarray):
            raise TypeError("The expected type of `decision_vector` is `np.ndarray`")
        
        fit = 0
        if function_id==0: ## 路径长度
            for i in range(0,self.V-1):
                # print("[info]: decision vector in f: ",decision_vector)
                line = int(self.V*(decision_vector[i]-1) + decision_vector[i+1]-1)
                fit += self.weight_list[line][0]
            line = int(self.V*(decision_vector[self.V-1]-1) + decision_vector[i+1]-1)
            fit += self.weight_list[line][0]
        elif function_id==1: ## 边权重
            for i in range(0,self.V-1):
                line = int(self.V*(decision_vector[i]-1) + decision_vector[i+1]-1)
                fit += self.weight_list[line][1]
            line = int(self.V*(decision_vector[self.V-1]-1) + decision_vector[i+1]-1)
            fit += self.weight_list[line][1]
            fit *= -1
        return fit


    def generate_random_solution(self):
        res = np.zeros(self.V)
        res = list(range(1,self.V+1))
        random.shuffle(res)
        # print("[info]: res in generate_random_solution:",res)
        ## return Solution
        return self.evaluate(x=res)
