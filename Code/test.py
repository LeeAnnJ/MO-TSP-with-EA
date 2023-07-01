import numpy as np
import csv
import time
import matplotlib.pyplot as plt
import sys
import os

# 设置目录路径
directory = "../result/SPEA2/pa561/"

# 遍历目录下的文件
for filename in os.listdir(directory):
    # 检查文件名是否以 "non_dominated_solutons" 开头
    if filename.startswith("non_dominated_solutons"):
        # 构建新的文件名
        new_filename = filename.replace("non_dominated_solutons", "non_dominated_solution")
        
        # 构建原文件的完整路径
        old_filepath = os.path.join(directory, filename)
        
        # 构建新文件的完整路径
        new_filepath = os.path.join(directory, new_filename)
        
        # 重命名文件
        os.rename(old_filepath, new_filepath)
        
        print(f"已将文件 {filename} 重命名为 {new_filename}")
# a=np.array([1,2,3,4])
# b=np.array([2,3,4,5])
# # plt.title("a test pic")
# plt.plot(a,b,"o-",c='r')
# plt.show()
# plt.draw()
# plt.scatter(a,b)
# plt.savefig("test.png")
# plt.xlabel('Distance')
# plt.ylabel('Profit(*-1)')

# time_start = time.time()
# for i in range(10000000):
#     i+=1

# time_end = time.time()
# print('程序执行时间: ',time_end - time_start)

# 保存原始的 sys.stdout
# original_stdout = sys.stdout

# 打开文件作为新的 sys.stdout
# with open('output.txt', 'w') as f:
#     f.write("132")
#     f.write("323")
#     sys.stdout = f
    # 现在所有的打印语句都会写入文件
    # print('Hello, world!')

# 恢复原始的 sys.stdout
# sys.stdout = original_stdout