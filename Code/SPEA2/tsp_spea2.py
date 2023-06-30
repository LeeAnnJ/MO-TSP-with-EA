import random
import numpy as np
from matplotlib.ticker import  MultipleLocator
import matplotlib.pyplot as plt

import argument as ARG
from tsp_problem import TspProblem


class SPEA2():
    max_iter = ARG.GEN
    p_cross = ARG.P_CROSS # 交叉概率
    p_mut = ARG.P_MUT # 变异概率
    V = 0 # 维度
    pop = 0 # 种群数量
    problem = TspProblem()
    population = []                    #父代种群
    archive = []                       #存档集合
    popu_arch = []                     #合并后的父代与存档集合种群
    fronts = []                        #Pareto前沿面
    KNN = []                           #最近领域距离，K-th
    rank = []#np.zeros(self.pop)       #非支配排序等级 
    S = []                             # 个体 i的 Strength Value
    D = []                             # density，距离度量
    R = []                             # 支配关系度量
    F = []                             # 适应度
    objectives = []                    #目标函数值       
    np = []                            #该个体支配的其它个体数目
    set = []                           # 被支配的个体集


    def __init__(self, V, problem:TspProblem):
        self.V = V                          
        self.K = int(np.sqrt(self.pop + self.pop)) #距离排序，第k个距离值
        self.problem = problem

                
    def cal_obj(self,position):                 #计算一个个体的多目标函数值 f1,f2 最小值
        f1 = position[0]
        f = 0
        for i in range(self.V-1):
            f += 9*(position[i+1]/(self.V - 1))
        g = 1+f
        f2 = g*(1- np.square(f1/g))
        return [f1,f2]
    
            
    def update(self):    #下一代 Archive
        #self.archive = []
        juli = []
        shiyingzhi = []
        a = 0
        for i in range(2*self.pop):
            if self.F[i] < 1:
                juli.append([self.D[i],i])
                a = a+1
            else:
                shiyingzhi.append([self.F[i],i])
        #判断是否超出范围
        if a > self.pop:              #截断策略
            juli = sorted(juli)
            for i in range(self.pop):
                self.archive[i] = self.popu_arch[juli[i][1]]
        if a == self.pop:              #刚好填充
            for i in range(self.pop):
                self.archive[i] = self.popu_arch[juli[i][1]]            
        if a < self.pop:              #适应值筛选
            shiyingzhi = sorted(shiyingzhi)
            for i in range(a):
                self.archive[i] = self.popu_arch[juli[i][1]]
            for i in range(self.pop - a):
                self.archive[i+a] = self.popu_arch[shiyingzhi[i][1]]

    def cal_fitness2(self):                      #计算 Pt和 Et 适应度, F(i) = R(i) + D(i)
        self.objectives = []
        self.set = []
        self.S = np.zeros(self.pop)
        self.D = np.zeros(self.pop)
        self.R = np.zeros(self.pop)
        self.F = np.zeros(self.pop)
        self.KNN = np.zeros(self.pop)
        position = []
        for i in range(self.pop):
            position = self.archive[i]
            self.objectives.append(self.cal_obj(position))
        #计算 S 值
        for i in range(self.pop):
            temp = []
            for j in range(self.pop):
                if j != i:
                    if self.objectives[i][0] <= self.objectives[j][0] and self.objectives[i][1] <= self.objectives[j][1]:
                        self.S[i] += 1         # i支配 j，np+1
                    if self.objectives[j][0] <= self.objectives[i][0] and self.objectives[j][1] <= self.objectives[i][1]: 
                        temp.append(j)         # j支配 i
            self.set.append(temp)   
        #计算 R 值
        for i in range(self.pop):
            for j in range(len(self.set[i])):
                self.R[i] += self.S[self.set[i][j]]
        #计算 D 值        
        for i in range(self.pop):
            distance = []
            for j in range(self.pop):
                if j != i:
                    distance.append(np.sqrt(np.square(self.objectives[i][0] - self.objectives[j][0]) + np.square(self.objectives[i][1] - self.objectives[j][1])))
            distance = sorted(distance)        
            self.KNN[i] = distance[self.K - 1]   #其它个体与个体 i 的距离，升序排序，取第 K 个距离值     
            self.D[i] = 1/(self.KNN[i] + 2)
        #计算 F 值
        for i in range(self.pop):
            self.F[i] = self.D[i] + self.R[i]   #适应度越小越好
        
    def selection(self):                               #轮盘赌选择
        pi = np.zeros(self.pop)                        #个体的概率
        qi = np.zeros(self.pop+1)                      #个体的累积概率
        P = 0
        self.cal_fitness2()                            #计算Archive的适应值     
        for i in range(self.pop):
            P += 1/self.F[i]                           #取倒数，求累积适应度
        for i in range(self.pop):
            pi[i] =  (1/self.F[i])/P               #个体遗传到下一代的概率                
        for i in range(self.pop):
            qi[0] = 0
            qi[i+1] = np.sum(pi[0:i+1])                #累积概率
        #生成新的 population
        self.population = np.zeros((self.pop,self.V))
        for i in range(self.pop):
            r = random.random()                        #生成随机数，
            for j in range(self.pop):
                if r > qi[j] and r < qi[j+1]:
                    self.population[i] = self.archive[j]
                j += 1                
                
    def crossover(self):                               #交叉,SBX交叉
        for i in range(self.pop-1):
            #temp1 = []
            #temp2 = []
            if random.random() < self.p_cross:
                #pc_point = random.randint(0,self.V-1)        #生成交叉点
                #temp1.append(self.population[i][pc_point:self.V])
                #temp2.append(self.population[i+1][pc_point:self.V])
                #self.population[i][pc_point:self.V] = temp2
                #self.population[i+1][pc_point:self.V] = temp1
                a = random.random()
                for j in range(self.V):
                    self.population[i][j] = a*self.population[i][j] + (1-a)*self.population[i+1][j]
                    self.population[i+1][j] = a*self.population[i+1][j] + (1-a)*self.population[i][j]
            i += 2       
        
    def mutation(self):                         #变异
        for i in range(self.pop):
            for j in range(self.V):
                if random.random() < self.p_mut:
                    self.population[i][j] = self.population[i][j] - 0.1 + np.random.random()*0.2               
                    if self.population[i][j] < 0:
                        self.population[i][j] = 0  #最小值0
                    if self.population[i][j] >1:
                        self.population[i][j] = 1  #最大值1                
                        
    def draw(self):                             #画图 
        self.cal_fitness2()
        self.objectives = [] 
        a = 0
        for i in range(self.pop):
            if self.F[i] < 1:                   #非支配个体  
                a += 1
                position = self.archive[i]
                self.objectives.append(self.cal_obj(position))
        x=[]
        y=[]
        for i in range(a):
            x.append(self.objectives[i][0])
            y.append(self.objectives[i][1])             
        ax=plt.subplot(111)
        plt.scatter(x,y)#,marker='+')#self.objectives[:][0],self.objectives[:][1]) #?
        #plt.plot(,'--',label='')        
        plt.axis([0.0,1.0,0.0,1.1])
        xmajorLocator = MultipleLocator(0.1)
        ymajorLocator = MultipleLocator(0.1)  
        ax.xaxis.set_major_locator(xmajorLocator) 
        ax.yaxis.set_major_locator(ymajorLocator) 
        plt.xlabel('f1')
        plt.ylabel('f2')
        plt.title('ZDT2 Pareto Front')
        plt.grid()
        #plt.show()
        # plt.savefig('SPEA ZDT2 Pareto Front 2.png')
        
    
    def run(self):
        init_Population()  #初始化种群，选择交叉变异，生成子代种群
        popu_archive()
        self.cal_fitness()
        self.update()
        for i in range(self.max_iter - 1):
            self.selection()
            self.crossover()
            self.mutation()
            popu_archive()
            self.cal_fitness()
            self.update()
            #self.selection()
            #self.crossover()
            #self.mutation()
        self.draw()


#初始化种群
def init_Population(spea:SPEA2): 
    #     for j in range(self.V):
    #         self.population[i][j] = random.random()
    #         self.archive[i][j] = random.random()
    for i in range(spea.pop):
        idv = spea.problem.generate_random_solution()
        spea.population.append(idv)
        spea.archive.append(idv)


# Population和 Archive合并,pop*2
def popu_archive(spea:SPEA2):                     
    spea.popu_arch = np.zeros((2*spea.pop,spea.V))
    for i in range(spea.pop):
        spea.popu_arch[i][:spea.V] = spea.population[i][:spea.V]
        spea.popu_arch[i+spea.pop][:spea.V] = spea.archive[i][:spea.V]

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

        for i in range(pop_num):
            position = spea.popu_arch[i]
            spea.objectives.append(spea.cal_obj(position))
        #计算 S 值
        for i in range(pop_num):
            temp = []
            for j in range(pop_num):
                if j != i:
                    if spea.objectives[i][0] <= spea.objectives[j][0] and spea.objectives[i][1] <= spea.objectives[j][1]:
                        spea.S[i] += 1         # i支配 j，np+1
                    if spea.objectives[j][0] <= spea.objectives[i][0] and spea.objectives[j][1] <= spea.objectives[i][1]: 
                        temp.append(j)         # j支配 i
            spea.set.append(temp)   
        #计算 R 值
        for i in range(pop_num):
            for j in range(len(spea.set[i])):
                spea.R[i] += spea.S[spea.set[i][j]]
        #计算 D 值        
        for i in range(pop_num):
            distance = []
            for j in range(pop_num):
                if j != i:
                    distance.append(np.sqrt(np.square(spea.objectives[i][0] - spea.objectives[j][0]) + np.square(spea.objectives[i][1] - spea.objectives[j][1])))
            distance = sorted(distance)        
            spea.KNN[i] = distance[spea.K - 1]   #其它个体与个体 i 的距离，升序排序，取第 K 个距离值     
            spea.D[i] = 1/(spea.KNN[i] + 2)
        #计算 F 值
        for i in range(pop_num):
            spea.F[i] = spea.D[i] + spea.R[i]