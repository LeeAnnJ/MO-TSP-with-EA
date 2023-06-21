import numpy as np
import random


class TspProblem(object):
    dimention = 0 # 决策变量个数 
    func_num = 2 # 目标函数个数
    weight_list = None # 权重向量
    bound = [0,np.inf]

    def __init__ (self,M=2,V=0,weight_list=np.array([])):
        self.dimention = V
        self.func_num = M
        self.weight_list = weight_list ## 权重向量

    def calc_vec(self, x,y):
        if x==y:
            return [0,0]
        if x<y:
            x,y = y,x
        line = int( (x-1)*(x-2)/2+y-1 )
        return self.weight_list[line]
    
    def func(self, decision_vector):
        if not isinstance(decision_vector, np.ndarray):
            raise TypeError("The expected type of `decision_vector` is `np.ndarray`")
        
        dis = weight = 0
       
        for i in range(0,self.dimention-1):
            vec = self.calc_vec(decision_vector[i], decision_vector[i+1])
            dis += vec[0] ## 路径长度
            weight += vec[1] ## 边权重
        vec = self.calc_vec(decision_vector[self.dimention-1], decision_vector[0])
        dis += vec[0]
        weight += vec[1]
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
