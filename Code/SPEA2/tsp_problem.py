import numpy as np
import random


class TspProblem(object):
    dimention = 0 # 决策变量个数 
    func_num = 2 # 目标函数个数
    distance = [] # 节点间距离
    edge_weight = [] # 边权重

    def __init__(self):
        pass 

    def __init__ (self, M, V, dis_matrix, edge_weight):
        self.dimention = V
        self.func_num = M
        if V>0:
            self.distance = dis_matrix # 节点距离
            self.edge_weight = edge_weight # 边权重
    
    def func(self, decision_vector):
        if not isinstance(decision_vector, np.ndarray):
            raise TypeError("The expected type of `decision_vector` is `np.ndarray`")
        
        dis = weight = 0
        for i in range(0,self.dimention-1):
            dis += self.distance[int(decision_vector[i])][int(decision_vector[i+1])] ## 路径长度
            weight += self.edge_weight[int(decision_vector[i])][int(decision_vector[i+1])] # 边权重
        dis += self.distance[int(decision_vector[self.dimention-1])][int(decision_vector[0])]
        weight += self.edge_weight[int(decision_vector[self.dimention-1])][int(decision_vector[0])]
        weight *= -1
        # print("[info]: decision vector in f: ",decision_vector,f"dis:{dis}, weight:{weight}")
        return [dis,weight]

    # 生成随机解
    def generate_random_solution(self):
        # res = np.zeros(self.dimention)
        res = list(range(1,self.dimention+1))
        random.shuffle(res)
        # print("[info]: res in generate_random_solution:",res)
        return np.array(res)
