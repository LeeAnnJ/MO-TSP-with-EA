# --- 文件位置 ---
DATA_FOLDER = "../../Data/" # 数据文件夹
DATA_FILE = ["dantzig42.tsp"] # ["bayg29.tsp","bays29.tsp","dantzig42.tsp","gr120.tsp","pa561.tsp"]
RESULT_FOLDER = "../../result/MOEA_D/" #结果文件夹

# ---基本参数设置----
EVAL_TIME  = 50 # 迭代次数
POP = 400 # 种群数量
FUNC_NUM = 2 # 目标函数数量False
NEIGHBOR = 10 # 邻居个数
P_CROSS = 0.9 # 交叉概率
P_MUT = 0.5 # 变异概率

# --- 结果保存设置 ---
REWRITE_WEIGHT = True # 重写权重文件
SAVE_PIONT = 102 # 每隔多少次迭代记录一次结果
NEED_DYNAMIC = True  # 是否动态展示
DRAW_WEIGHT = False # 是否画出权重图