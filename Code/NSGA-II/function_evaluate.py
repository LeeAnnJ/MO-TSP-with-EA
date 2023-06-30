import numpy as np

# 目标函数评价类
class TSPEvaluator(object):
    M = 2 # 目标函数个数

    def __init__(self):
        self.V = 0

    def __init__(self, V,dis_matrix,edge_weight_matrix):
        self.V = V # 变量维度
        if V>0:
            self.distance = dis_matrix # 节点间的距离
            self.edge_weight = edge_weight_matrix # 边权重
    
       
    # 计算每个个体的M个目标函数值
    # x[0:V]: 个体决策变量
    def evaluate_objective(self, x):
        dis = 0 # 路径距离
        weight = 0 # 路径权重
        for i in range(0,self.V-1):
            dis += self.distance[int(x[i])][int(x[i+1])]
            weight += self.edge_weight[int(x[i])][int(x[i+1])]
        dis += self.distance[int(x[self.V-1])][int(x[0])]
        weight += self.edge_weight[int(x[self.V-1])][int(x[0])]
        weight *= -1

        eval = np.array([dis,weight])
        return eval
