# --- 文件位置 ---
DATA_FOLDER = "../../Data/" # 数据文件夹
DATA_FILE = ["bayg29_copy.tsp"] # ["bayg29.tsp","bays29.tsp","dantzig42.tsp","gr120.tsp","pa561.tsp"]
RESULT_FOLDER = "../../result/NSGA-II/" #结果文件夹

# ---基本参数设置----
POP  = 50 # 种群数量
GEN  = 200 # 迭代次数
SAVE_PIONT = 50 # 每隔多少次迭代记录一次结果
EVLN = 2 # 目标函数数量
P_CROSS = 0.9 # 交叉概率
P_MUT = 0.5 # 变异概率
TOUR = 2 # 锦标赛参赛选手个数
