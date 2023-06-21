import numpy as np


## 对初始种群开始排序 快速非支配排序
# 使用非支配排序对种群进行排序。该函数返回每个个体对应的排序值和拥挤距离,是一个两列的矩阵。  
# 并将排序值和拥挤距离添加到染色体矩阵中
# M: 目标函数个数 V: 决策变量
def non_domination_sort(x, M, V):
    N,_ = x.shape # 种群的数量
    m = np.zeros((N,2))
    x = np.hstack((x,m))
    front = 0 # front = 1
    # F = {front: {'f': []}}
    F = [[]]
    individual = np.zeros(N, dtype=[('n', int), ('p', list)])

    for i in range(N):
        individual[i]['n'] = 0 # n:个体i被支配的个体数量
        individual[i]['p'] = [] # p:被个体i支配的个体集合
        for j in range(N):
            dom_less = 0
            dom_equal = 0
            dom_more = 0
            for k in range(M): #判断个体i和个体j的支配关系
                if x[i, V + k] < x[j, V + k]:
                    dom_less += 1
                elif x[i, V + k] == x[j, V + k]:
                    dom_equal += 1
                else:
                    dom_more += 1
            if dom_less == 0 and dom_equal != M: # 说明i受j支配,相应的n加1
                individual[i]['n'] += 1
            elif dom_more == 0 and dom_equal != M: # 说明i支配j,把j加入i的支配合集中
                individual[i]['p'].append(j)
        if individual[i]['n'] == 0: # 个体i非支配等级排序最高,属于当前最优解集,相应的染色体中携带代表排序数的信息
            x[i, M + V ] = 1
            F[front].append(i) # 等级为1的非支配解集
        
    # 上面的代码是为了找出等级最高的非支配解集
    # 下面的代码是为了给其他个体进行分级
    while len(F[front]) > 0:
        Q = [] #存放下一个front集合
        # for i in range(len(F[front])): 
        for i in F[front]: # 循环当前支配解集中的个体
            if len(individual[i]['p']) > 0: # 个体i有自己所支配的解集
                #for j in range(len(individual[F[front]['f'][i]]['p'])):
                for j in individual[i]['p']: # 循环个体i所支配解集中的个体
                    individual[j]['n'] -= 1 # 个体j的被支配个数减1
                    if individual[j]['n'] == 0: # 如果q是非支配解集,则放入集合Q中
                        x[j, M + V] = front + 2 #1 # 个体染色体中加入分级信息
                        Q.append(j)
        front += 1
        F.append(Q) # F[front] = {'f': Q}

    index_of_fronts = np.argsort(x[:, M + V]) # 对个体的代表排序等级的列向量进行升序排序 index_of_fronts表示排序后的值对应原来的索引
    sorted_based_on_front = x[index_of_fronts] # 将x矩阵按照排序等级升序排序后的矩阵

    ## Crowding distance 计算每个个体的拥挤度
    current_index = 0
    for front in range(0, len(F)-1): # 这里减1是因为代码55行这里,F的最后一个元素为空,这样才能跳出循环。所以一共有length-1个排序等级
        distance = 0
        y = np.zeros((len(F[front]), 2*M + V + 1))
        previous_index = current_index #+ 1
        for i in range(len(F[front])):
            y[i,0:M+V+2] = sorted_based_on_front[current_index + i] # y中存放的是排序等级为front的集合矩阵
        current_index += i+1
        sorted_based_on_objective = np.zeros((len(y), 2*M + V + 1)) # 基于拥挤距离排序的矩阵
        for i in range(M):
            index_of_objectives = np.argsort(y[:, V + i])
            sorted_based_on_objective = y[index_of_objectives] # 按照目标函数值排序后的x矩阵
            f_max = sorted_based_on_objective[-1, V + i] # 目标函数最大值
            f_min = sorted_based_on_objective[0, V + i] # 目标函数最小值
            y[index_of_objectives[-1], M + V + 1 + i] = np.inf # 对排序后的第一个个体和最后一个个体的距离设为无穷大
            y[index_of_objectives[0], M + V + 1 + i] = np.inf
            for j in range(1, len(index_of_objectives) - 1): # 循环集合中除了第一个和最后一个的个体
                next_obj = sorted_based_on_objective[j + 1, V + i]
                previous_obj = sorted_based_on_objective[j - 1, V + i]
                if f_max - f_min == 0:
                    y[index_of_objectives[j], M + V + 1 + i] = np.inf
                else:
                    y[index_of_objectives[j], M + V + 1 + i] = (next_obj - previous_obj) / (f_max - f_min)
        distance = np.zeros(len(F[front]))
        for i in range(M):
            distance += y[:, M + V + 1 + i]
        y[:, M + V + 1] = distance
        y = y[:, :M + V + 2]
        x[previous_index:current_index] = y # 得到的是已经包含等级和拥挤度的种群矩阵 并且已经按等级排序排序

    return x
