# --- 文件位置 ----
DATA_FOLDER = "../../Data/" # 数据文件夹
DATA_FILE = ["bayg29.tsp"] # ["bayg29.tsp","bays29.tsp","dantzig42.tsp","gr120.tsp","pa561.tsp"]
RESULT_FOLDER = "../../result/MOEA_D-fail/" #结果文件夹

# ---基本参数设置----
POP = 200 # 种群数量
EVAL_TIME = 50 # 迭代次数
NEIGHBOR = 5 # 邻居个数
M = 2 # 目标函数个数
P_CROSS = 0.9 # 交叉概率
P_MUT = 0.1 # 变异概率

# --- 结果保存设置 ---
REWRITE_WEIGHT = True # 重写权重文件
SAVE_PIONT = 50 # 每隔多少次迭代记录一次结果