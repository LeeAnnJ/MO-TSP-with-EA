# --- 文件位置 ---
DATA_FOLDER = "../../Data/" # 数据文件夹
DATA_FILE = ["dantzig42.tsp"] # ["bayg29.tsp","bays29.tsp","dantzig42.tsp","gr120.tsp","pa561.tsp"]
RESULT_FOLDER = "../../result/SPEA2/" #结果文件夹

# ---基本参数设置----
FUNC_NUM = 2 # 目标函数个数
POP  = 100 # 种群数量
GEN  = 1000 # 迭代次数
SAVE_PIONT = 50 # 每隔多少次迭代记录一次结果
EVLN = 2 # 目标函数数量
P_CROSS = 0.9 # 交叉概率
P_MUT = 0.3 # 变异概率