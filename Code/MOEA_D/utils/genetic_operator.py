import numpy as np

import argument as ARG

'''
对种群的交叉变异操作
采用全排列算子的交叉变异方式
'''
class Permutation_GeneOperator(object):
    M = 0 # 目标函数个数
    V = 0 # 决策变量个数
    P_cross = ARG.P_CROSS # 交叉概率
    P_mut = ARG.P_MUT # 变异概率

    def __init__(self):
        pass

    def set(self, M, V):
        self.M = M # 目标函数个数
        self.V = V # 决策变量个数
    
    # 交叉变异操作
    def cross_mutation(self, p1, p2):
        y1 = np.copy(p1)
        y2 = np.copy(p2)
        if np.random.rand() < self.P_cross:
            y1,y2 = self.order_crossover(y1,y2)
        if np.random.rand() < self.P_mut:
            y1 = self.displacement_mutation(y1)
            y2 = self.displacement_mutation(y2)
        return y1,y2
    
    # 序交叉
    def order_crossover(self,parent1,parent2):
        var = len(parent1)
        child1 = np.zeros(var) # self.M + self.V)
        child2 = np.zeros(var)
        start = np.random.randint(self.V)
        end = np.random.randint(start+1,self.V+1)
        child1[start:end] = parent1[start:end]
        child2[start:end] = parent2[start:end]

        point_1 = point_2 = end%self.V
        for i in range(end,self.V):
            while np.any(child1[:]==parent2[point_1]):
                point_1 = (point_1+1)%self.V
            while np.any(child2[:]==parent1[point_2]):
                point_2 = (point_2+1)%self.V
            child1[i] = parent2[point_1]
            child2[i] = parent1[point_2]
        for i in range(0,start):
            while np.any(child1[:]==parent2[point_1]):
                point_1 = (point_1+1)%self.V
            while np.any(child2[:]==parent1[point_2]):
                point_2 = (point_2+1)%self.V
            child1[i] = parent2[point_1]
            child2[i] = parent1[point_2]
        return child1,child2

    # 位移变异
    def displacement_mutation(self,gene):
        start = np.random.randint(self.V)
        if start>0:
            end = np.random.randint(start+1,self.V+1)
        else:
            end = np.random.randint(self.V-1)
        part = gene[start:end]
        mutated_gene = np.concatenate([gene[:start],gene[end:self.V]])
        insert_pos = np.random.randint(len(mutated_gene))
        mutated_gene = np.insert(mutated_gene,insert_pos,part)
        
        return mutated_gene
    



if __name__ == '__main__':
    parent1 = np.array([1,2,3,4,5,6,7])
    parent2 = np.array([7,6,5,4,3,2,1])
    operator = Permutation_GeneOperator(2,7)
    for i in range(5):
        print(i,": \n")
        child1 = operator.displacement_mutation(parent1)
        print(child1)
        # child1,child2 = operator.order_crossover(parent1,parent2)
        # print(child1)
        # print(child2)
