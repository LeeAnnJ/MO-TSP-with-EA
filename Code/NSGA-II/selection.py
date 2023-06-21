import numpy as np

# 竞标赛选择法，每次随机选择两个个体，优先选择排序等级高的个体，如果排序等级一样，则优选选择拥挤度大的个体
# pop:交配池大小 tour_size:参赛选手个数
def tournament_selection(chromosome, pool_size, tour_size):
    pop, variables = chromosome.shape  # 获取种群的个体数量和决策变量数量
    rank = variables - 2  # 个体向量中排序值所在位置
    distance = variables - 1  # 个体向量中拥挤度所在位置
    res = np.zeros((pool_size, variables))  # 存储选中的个体

    for i in range(pool_size):
        candidate = np.zeros(tour_size, dtype=int)
        for j in range(tour_size):
            candidate[j] = np.random.randint(pop)  # 随机选择参赛个体
            while np.any(candidate[:j] == candidate[j]):  # 防止两个参赛个体是同一个
                candidate[j] = np.random.randint(pop)

        c_obj_rank = chromosome[candidate, rank]  # 记录每个参赛者的排序等级
        c_obj_distance = chromosome[candidate, distance]  # 记录每个参赛者的拥挤度

        min_candidate = np.where(c_obj_rank == np.min(c_obj_rank))[0]  # 选择排序等级较小的参赛者
        if len(min_candidate) != 1:  # 如果两个参赛者的排序等级相等，则继续比较拥挤度，优先选择拥挤度大的个体
            max_candidate = np.where(c_obj_distance[min_candidate] == np.max(c_obj_distance[min_candidate]))[0]
            max_candidate = max_candidate[0]
            res[i, :] = chromosome[candidate[min_candidate[max_candidate]], :]
        else:
            res[i, :] = chromosome[candidate[min_candidate[0]], :]

    return res


# 精英选择策略
def replace_chromosome(intermediate_chromosome, M, V, pop):
    N, m = intermediate_chromosome.shape
    index = np.argsort(intermediate_chromosome[:, M + V])
    sorted_chromosome = intermediate_chromosome[index]

    max_rank = np.max(intermediate_chromosome[:, M + V])
    # print("[info]: max_rank:",max_rank)
    selected_chromosome = np.zeros((pop,M+V+2))
    previous_index = 0
    for i in range(1, int(max_rank) + 1):
        current_index = np.max(np.where(sorted_chromosome[:, M + V] == i)[0])
        if current_index > pop:
            remaining = pop - previous_index
            temp_pop = sorted_chromosome[previous_index:current_index, :]
            temp_sort_index = np.argsort(temp_pop[:, M + V + 1])[::-1]
            temp_sort_pop = temp_pop[temp_sort_index]
            selected_chromosome[previous_index:previous_index+remaining,:] = temp_sort_pop[0:remaining,:]
            return selected_chromosome
        elif current_index < pop:
            selected_chromosome[previous_index:current_index, :] = sorted_chromosome[previous_index:current_index, :]
        else:
            selected_chromosome[previous_index:current_index, :] = sorted_chromosome[previous_index:current_index, :]
            return selected_chromosome
        previous_index = current_index