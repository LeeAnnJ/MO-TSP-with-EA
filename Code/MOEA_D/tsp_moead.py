import csv
import time
import numpy as np

import argument as ARG
from tsp_problem import TspProblem
from utils import Utils


class MOEAD(object):
    problem = None
    name = '' # 数据文件名称
    dim = 0 # 决策变量个数
    func_num = 0 # 目标函数个数
    GNO = Utils.GENE_OP() # 交叉变异算子
    pop_size = -1 # 种群大小，取决于权重文件
    max_eval = ARG.EVAL_TIME # 最大迭代次数
    neighbour_size = ARG.NEIGHBOR # 邻居设定
    EP_X_ID = [] # 支配前沿的ID
    EP_X_FV = [] # 支配前沿的函数值
    Pop = [] # 种群
    Pop_FV = [] # 种群计算出的函数值
    W = [] # 权重
    W_Bi_T = [] # 权重的T个邻居。比如：T=2，(0.1,0.9)的邻居：(0,1)、(0.2,0.8)。永远固定不变
    Z = [] # 理想点。（比如最小化，理想点是趋于0）
    weight_file_path = '' # 权重向量存储位置
    result_folder = '' # 结果保存位置
    cur_eval = 0 # 当前迭代代数
    need_dynamic = ARG.NEED_DYNAMIC  # 是否动态展示
    draw_weight = ARG.DRAW_WEIGHT # 是否画出权重图
    save_point = ARG.SAVE_PIONT # 每过多少次迭代记录一次结果
    now_y = []

    # 数据初始化
    def __init__(self, problem:TspProblem, data_name:str, weight_list:np.ndarray, result_folder:str):
        self.problem = problem
        self.dim = problem.dimention
        self.func_num = problem.func_num
        self.GNO.set(self.func_num,self.dim)
        self.name = data_name
        self.weight_file_path = f"{ARG.DATA_FOLDER}{data_name}_weight.txt"
        self.W = weight_list
        self.pop_size = self.W.shape[0]
        self.result_folder = result_folder

    # 保存结果
    def save_result(self,text=None):
        print("[info] start saving current solution in result file.")
        # 记录最终解集
        solution = np.array(self.Pop)
        value = np.array(self.Pop_FV)
        best_sol = solution[self.EP_X_ID]
        best_value = value[self.EP_X_ID]
        result = np.hstack((best_value,best_sol))
        header = ["distance","profit","solution"]
        if text is not None:
            csv_name = f"{self.result_folder}{text}.csv"
            pic_text = f"{self.name},{text}"
            pic_file = f"{self.result_folder}{text}_pic.png"
        else:
            csv_name = f"{self.result_folder}non_dominated_solutons_{self.cur_eval}.csv"
            pic_text = f"{self.name},iter: {self.cur_eval}"
            pic_file = f"{self.result_folder}pic_iter_{self.cur_eval}.png"

        with open(csv_name,"w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(result)
        # 保存图像
        if self.need_dynamic is not True:
            Utils.Draw.plt.cla()
            Utils.Draw.draw_MOEAD_pareto(self,pic_text)
        Utils.Draw.savefig(pic_file)
        pass

    # 执行演化算法
    def run(self):
        start = time.time()
        evolution(self)
        end = time.time()
        print("[info] experinced time: ",end-start," s.")


# 生成初始解
def create_pop(moead:MOEAD):
    pop = []
    pop_fv = []
    if moead.pop_size < 1:
        raise ValueError("moead's pop size small than 1.")
    for i in range(moead.pop_size):
        x = moead.problem.generate_random_solution()
        pop.append(x)
        pop_fv.append(moead.problem.func(x))

    moead.Pop = pop
    moead.Pop_FV = pop_fv
    pass

# 计算T个邻居
def cpt_W_Bi_T(moead:MOEAD):
    if moead.neighbour_size<1:
        return -1
    for bi in range(moead.W.shape[0]):
        Bi = moead.W[bi]
        dis = np.sum((moead.W-Bi)**2, axis=1)
        B_t = np.argsort(dis)
        B_t = B_t[1:moead.neighbour_size+1] # 第0个是自己（距离永远最小）
        moead.W_Bi_T.append(B_t)
    pass


# 另一种初始化Z集的方法
def init_z2(moead:MOEAD):
    Z = moead.Pop_FV[0][:]
    dz = np.random.rand()
    for fi in range(moead.func_num):
        for Fpi in moead.Pop_FV:
            if Fpi[fi] < Z[fi]:
                Z[fi] = Fpi[fi] - dz
    moead.Z = Z
    pass


# 计算初始化前沿
def init_EP(moead:MOEAD):
    for pi in range(moead.pop_size):
        np = 0
        F_V_P = moead.Pop_FV[pi]
        for ppi in range(moead.pop_size):
            F_V_PP = moead.Pop_FV[ppi]
            if pi != ppi:
                if Utils.is_dominate(F_V_PP, F_V_P):
                    np += 1
        if np == 0:
            moead.EP_X_ID.append(pi)
            moead.EP_X_FV.append(F_V_P[:])


# 演化算法的主要流程
def evolution(moead:MOEAD):
    cpt_W_Bi_T(moead)
    create_pop(moead)
    init_z2(moead)
    init_EP(moead)
    # 开始迭代进化
    for gen in range(0,moead.max_eval+1):
        moead.cur_eval = gen
        # 个体序号pi, 个体p
        for pi,p in enumerate(moead.Pop):
            Bi = moead.W_Bi_T[pi] # 第pi个个体的邻居集
            # 从邻居被随机选两个个体
            index_k = Bi[np.random.randint(moead.neighbour_size)]
            index_l = Bi[np.random.randint(moead.neighbour_size)]
            Xi = moead.Pop[pi]
            Xk = moead.Pop[index_k]
            Xl = moead.Pop[index_l]
            # 进化下一代个体
            y = Utils.generate_next(moead,gen,pi,Xi,Xk,Xl)
            cbsv_i = Utils.cpt_tchebyshev(moead,pi,Xi) # Xi不进化前的切比雪夫距离
            cbsv_y = Utils.cpt_tchebyshev(moead,pi,y) # 计算进化后的切比雪夫距离
            dis = 0.001 #超过这个距离才更新
            if cbsv_y<cbsv_i:
                moead.now_y = pi
                Fy = moead.problem.func(y)[:]
                Utils.update_EP_by_id(moead,pi,Fy)
                Utils.update_Z(moead,y)
                if cbsv_i-cbsv_y>dis:
                    Utils.update_EP_by_Y(moead,pi)
            Utils.update_BT_X(moead,Bi,y)
        
        # 动态展示
        if moead.need_dynamic:
            Utils.Draw.plt.cla()
            if moead.draw_weight:
                Utils.Draw.draw_weight(moead)
            Utils.Draw.draw_MOEAD_pareto(moead,f"{moead.name},iter: {gen}")
            Utils.Draw.plt.pause(0.001)
            # Utils.Draw.plt.show()
        
        # 检查点
        if gen%10==0:
            print(f"[info] iteration {gen}, number in pareto front(moead.EP_X_ID's length): {len(moead.EP_X_ID)}, moead.Z: {moead.Z}")
            if gen%moead.save_point==0:
                moead.save_result()
