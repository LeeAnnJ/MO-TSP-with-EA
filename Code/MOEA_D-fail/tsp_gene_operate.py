from moead_framework.core.genetic_operator.abstract_operator import GeneticOperator
import numpy as np
import argument as ARG

class TspCrossover(GeneticOperator):
    def __init__(self, solutions, V, cross):
        if len(solutions[0])<V:
            msg = f"The number of variable in solution (V={len(self.solutions[0])}) must be strictly equal V ={V}"
            raise ValueError(msg)
        self.V = V
        self.P_cross = cross
        super().__init__(solutions)

    def run(self):
        self.number_of_solution_is_correct(n=2)
        parent1 = self.solutions[0]
        parent2 = self.solutions[1]
        if np.random.rand() < self.P_cross:
            child = self.order_crossover(parent1,parent2)
        elif np.random.rand()< 0.5:
            child = parent1
        else:
            child = parent2
        return child
    
    # 序交叉
    def order_crossover(self,parent1,parent2):
        child1 = np.zeros(self.V) 
        start = np.random.randint(self.V)
        end = np.random.randint(start+1,self.V+1)
        child1[start:end] = parent1[start:end]

        point_1 = end%self.V
        for i in range(end,self.V):
            while np.any(child1[:]==parent2[point_1]):
                point_1 = (point_1+1)%self.V
            child1[i] = parent2[point_1]
        for i in range(0,start):
            while np.any(child1[:]==parent2[point_1]):
                point_1 = (point_1+1)%self.V
            child1[i] = parent2[point_1]
        return child1


class TspMutation(GeneticOperator):
    def __init__(self, solutions, V, mut):
        if len(solutions[0])<V:
            msg = f"The number of variable in solution (V={len(self.solutions[0])}) must be strictly equal V ={V}"
            raise ValueError(msg)
        self.V = V
        self.P_mut = mut
        super().__init__(solutions)

    def run(self):
        self.number_of_solution_is_correct(n=1)
        if np.random.rand() < self.P_mut:
            child = self.displacement_mutation(self.solutions[0])
        else: 
            child = self.solutions[0]
        return child
    
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


class TspGeneOperator(GeneticOperator):
    def __init__(self, solutions:np.ndarray):
        self.V = len(solutions[0])
        self.P_cross = ARG.P_CROSS
        self.P_mut = ARG.P_MUT
        super().__init__(solutions)
    
    def run(self):
        cross = TspCrossover(solutions=self.solutions,V=self.V,cross=self.P_cross)
        child = cross.run()
        mutate = TspMutation(solutions=[child],V=self.V,mut=self.P_mut)
        child = mutate.run()
        return child
