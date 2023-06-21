import numpy as np
import csv
import time
import matplotlib.pyplot as plt
import sys

a=np.array([1,2,3,4])
b=np.array([2,3,4,5])
# plt.title("a test pic")
# plt.plot(a,b,"o-")
# # plt.show()
# plt.draw()
plt.scatter(a,b)
plt.savefig("test.png")
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