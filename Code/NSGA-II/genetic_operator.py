import numpy as np

import argument as ARG
from function_evaluate import TSPEvaluator as Evaluator

# 对种群的交叉变异操作
# 采用全排列算子的交叉变异方式
class Permutation_GeneOperator(object):
    # 交叉变异参数设置
    def set_constant(self):
        self.P_cross = ARG.P_CROSS # 交叉概率
        self.P_mut = ARG.P_MUT # 变异概率
    
    def __init__(self):
        self.M = 0 # 目标函数个数
        self.V = 0 # 决策变量个数

    def __init__(self, M, V, eval:Evaluator):
        self.M = M # 目标函数个数
        self.V = V # 决策变量个数
        self.eval = eval
        self.set_constant()
        
    # 对父代解进行交叉操作
    def crossover_option(self, parent_chromosome):
        N, _ = parent_chromosome.shape  # N是交配池中的个体数量
        child = np.zeros((2 * N, self.M+self.V))
        # 进行交叉工作
        for i in range(N):
            child_1 = np.zeros(self.V+self.M)
            child_2 = np.zeros(self.V+self.M)
            parent_1 = np.random.randint(N)
            parent_2 = np.random.randint(N)
            count = 0
            while np.array_equal(parent_chromosome[parent_1], parent_chromosome[parent_2]):
                parent_2 = np.random.randint(0, N)
                count+=1
                if count>=50:
                    print("[warn] too much iteration for select parent in crossover option, quit.")
                    parent_2 = min(N-1,parent_1+1)
                    break
            parent_1 = parent_chromosome[parent_1,0:self.V+self.M]
            parent_2 = parent_chromosome[parent_2,0:self.V+self.M]
           
            if np.random.rand() < self.P_cross:
                child_1[0:self.V+self.M],child_2[0:self.V+self.M] = self.order_crossover(parent_1[0:self.V+self.M],parent_2[0:self.V+self.M])
                child_1[self.V:self.M + self.V] = self.eval.evaluate_objective(child_1)
                child_2[self.V:self.M + self.V] = self.eval.evaluate_objective(child_2)
            else:
                child_1 = parent_1[0:self.M+self.V].copy()
                child_2 = parent_2[0:self.M+self.V].copy()
            child[2*i] = child_1
            child[2*i+1] = child_2
        # print("[info] child in crossover opition's shape:",child.shape)
        return child
    
    
    # 序交叉
    def order_crossover(self,parent1,parent2):
        var = len(parent1)
        child1 = np.zeros(var) # self.M + self.V)
        child2 = np.zeros(var)
        start = np.random.randint(self.V)
        end = np.random.randint(start+1,self.V+1)
        # print("[info] :start:",start,"end:",end)
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
    
    # 对交叉后的数组的每个个体根据概率进行变异操作
    def mutate_option(self, chromosome):
        N, m = chromosome.shape
        # print("[info] in mutate_option, chromosome'shape: ",(N,m))
        for i in range(N):
            if np.random.rand() < self.P_mut:
                chromosome[i,:self.V] = self.displacement_mutation(chromosome[i,:self.V])
                chromosome[i,self.V:] = self.eval.evaluate_objective(chromosome[i])
        return chromosome
    

    # 位移变异
    def displacement_mutation(self,gene):
        start = np.random.randint(self.V)
        end = np.random.randint(start+1,self.V+1)
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
