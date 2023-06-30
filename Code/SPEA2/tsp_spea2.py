import csv
import time
import random
import numpy as np
import matplotlib.pyplot as plt

import argument as ARG
import utils as Utils
from tsp_problem import TspProblem
from genetic_operator import Permutation_GeneOperator as GNO


class SPEA2():
    max_iter = ARG.GEN     # 最大迭代次数
    V = 0                  # 维度
    pop = ARG.POP          # 种群数量
    problem = TspProblem() # TSP问题的目标值计算和随机解生成
    gene_op = None         # 个体基因的交叉变异操作
    result_folder= ""      # 结果保存的位置
    population = []        # 父代种群
    archive = []           # 存档集合
    popu_arch = []         # 合并后的父代与存档集合种群
    fronts = []            # Pareto前沿面
    KNN = []               # 最近领域距离，K-th
    rank = []              # 非支配排序等级 
    S = []                 # 个体 i的 Strength Value
    D = []                 # density，距离度量
    R = []                 # 支配关系度量
    F = []                 # 适应度
    objectives = []        # 目标函数值       
    np = []                # 该个体支配的其它个体数目
    set = []               # 被支配的个体集


    def __init__(self, V, problem:TspProblem, result_folder):
        self.V = V 
        self.K = int(np.sqrt(self.pop + self.pop)) #距离排序，第k个距离值
        self.problem = problem
        self.gene_op = GNO(V)
        self.result_folder = result_folder
        self.clear_old()
    
    def clear_old(self):
        self.population = []
        self.archive = []
        self.popu_arch = []
        self.fronts = []
        self.KNN = []
        self.rank = []
        self.S = []
        self.D = []
        self.R = []
        self.F = []
        self.objectives = []
        self.np = []
        self.set = []


    # 保存当前结果画图 支配前沿     
    def save_result(self, text, iter=-1):
        print("[info] start saving current solution in result file.")
        if iter!=-1:
            csv_name = f"{self.result_folder}non_dominated_solutons_{iter}.csv"
            pic_text = f"Pareto Front, iter: {iter}"
            pic_file = f"{self.result_folder}pic_iter_{iter}.png"
        else:
            csv_name = f"{self.result_folder}{text}.csv"
            pic_text = f"Pareto Front, {text}"
            pic_file = f"{self.result_folder}{text}_pic.png"
            pass

        cal_fitness(self,self.pop)
        front = []
        front_obj = [] 
        count = 0
        # 寻找非支配个体
        for i in range(self.pop):
            if self.F[i] < 1:                   
                count += 1
                position = self.archive[i]
                front.append(position)
                front_obj.append(self.problem.func(position))

        front_obj = np.array(front_obj)
        obj = np.array(self.objectives)
        front = np.array(front)
        
        # 保存csv文件
        result = np.hstack([front_obj,front])
        header = ["distance","profit","solution"]
        with open(csv_name,"w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(result)

        # 画图保存
        best_x,best_y = front_obj[:,0], front_obj[:,1]
        x,y = obj[:,0], obj[:,1]
        plt.cla()
        plt.xlabel('distance')
        plt.ylabel('profit(*-1)')
        plt.title(pic_text)
        plt.scatter(x, y, c='black', s=5)
        plt.scatter(best_x, best_y, c='r',s=20)
        #plt.plot(,'--',label='')
        # plt.show()
        plt.savefig(pic_file)


    # 演化算法主要流程
    def run(self):
        start = time.time()
        # 初始化种群，选择交叉变异，生成子代种群
        init_Population(self)  
        popu_archive(self)
        cal_fitness(self,2*self.pop)
        update(self)
        for i in range(1,self.max_iter+1):
            # print(f"[info] iteration {i}.")
            selection(self)
            self.population = self.gene_op.crossover_option(self.population)
            self.population = self.gene_op.mutate_option(self.population)
            popu_archive(self)
            cal_fitness(self,2*self.pop)
            update(self)

            if i%ARG.SAVE_PIONT==0:
                print(f"[info] iteration {i} finish.")
                self.save_result(text="",iter=i)
        end = time.time()
        print("[info] experinced time: ",end-start," s.")
    pass


#初始化种群
def init_Population(spea:SPEA2): 
    for i in range(spea.pop):
        idv = spea.problem.generate_random_solution()
        spea.population.append(idv)
        spea.archive.append(idv)


# Population和 Archive合并,pop*2
def popu_archive(spea:SPEA2):                     
    spea.popu_arch = np.zeros((2*spea.pop,spea.V))
    # print("[info] population's length",len(spea.population))
    
    for i in range(spea.pop):
        spea.popu_arch[i][:] = spea.population[i]
        spea.popu_arch[i+spea.pop] = spea.archive[i]


#计算 Pt和 Et 适应度, F(i) = R(i) + D(i)
# pop_num:需要计算的个体个数
# note: cal_fitness: 2*self.pop cal_fitness2: self.pop
def cal_fitness(spea:SPEA2, pop_num):
        spea.objectives = []
        spea.set = []
        spea.S = np.zeros(pop_num)
        spea.D = np.zeros(pop_num)
        spea.R = np.zeros(pop_num)
        spea.F = np.zeros(pop_num)
        spea.KNN = np.zeros(pop_num)

        if pop_num==2*spea.pop:
            for i in range(pop_num):
                position = spea.popu_arch[i]
                spea.objectives.append(spea.problem.func(position))
        elif pop_num==spea.pop:
            for i in range(pop_num):
                position = spea.archive[i]
                spea.objectives.append(spea.problem.func(position))

        # 计算 S 值
        for i in range(pop_num):
            temp = []
            for j in range(pop_num):
                if j != i:
                    # i支配 j，np+1
                    ob_i = spea.objectives[i]
                    ob_j = spea.objectives[j]
                    if Utils.is_dominate(ob_i,ob_j):
                        spea.S[i] += 1
                    # j支配 i
                    if Utils.is_dominate(ob_j,ob_i):
                        temp.append(j)
            spea.set.append(temp)   

        # 计算 R 值
        for i in range(pop_num):
            for j in range(len(spea.set[i])):
                spea.R[i] += spea.S[spea.set[i][j]]

        # 计算 D 值        
        for i in range(pop_num):
            distance = []
            for j in range(pop_num):
                if j != i:
                    distance.append(Utils.cal_distance(spea.objectives[i],spea.objectives[j]))
            distance = sorted(distance)        
            spea.KNN[i] = distance[spea.K-1] # 其它个体与个体i的距离,升序排序,取第 K 个距离值     
            spea.D[i] = 1/(spea.KNN[i]+2)

        # 计算 F 值
        for i in range(pop_num):
            spea.F[i] = spea.D[i] + spea.R[i] #适应度越小越好


# 更新下一代 Archive
def update(spea:SPEA2):    
    #spea.archive = []
    distance = []
    fitness = []
    count = 0
    for i in range(2*spea.pop):
        if spea.F[i] < 1:
            distance.append([spea.D[i],i])
            count = count+1
        else:
            fitness.append([spea.F[i],i])

    #判断是否超出范围
    if count > spea.pop: # 截断策略
        distance = sorted(distance)
        for i in range(spea.pop):
            spea.archive[i] = spea.popu_arch[distance[i][1]]
    if count == spea.pop: # 刚好填充
        for i in range(spea.pop):
            spea.archive[i] = spea.popu_arch[distance[i][1]]            
    if count < spea.pop: # 适应值筛选
        fitness = sorted(fitness)
        for i in range(count):
            spea.archive[i] = spea.popu_arch[distance[i][1]]
        for i in range(spea.pop - count):
            spea.archive[i+count] = spea.popu_arch[fitness[i][1]]


# 轮盘赌选择
def selection(spea:SPEA2):                               
    pi = np.zeros(spea.pop)  # 个体的概率
    qi = np.zeros(spea.pop+1) # 个体的累积概率
    P = 0
    cal_fitness(spea,2*spea.pop) # 计算Archive的适应值

    for i in range(spea.pop):
        P += 1/spea.F[i] # 取倒数，求累积适应度
    for i in range(spea.pop):
        pi[i] =  (1/spea.F[i])/P # 个体遗传到下一代的概率                
    for i in range(spea.pop):
        qi[0] = 0
        qi[i+1] = np.sum(pi[0:i+1]) # 累积概率

    # 生成新的 population
    spea.population = np.zeros((spea.pop,spea.V))
    for i in range(spea.pop):
        r = random.random() # 生成随机数，
        for j in range(spea.pop):
            if r > qi[j] and r < qi[j+1]:
                spea.population[i] = spea.archive[j]
            j += 1
    # print("[info] in selection, population's length:",len(spea.population))