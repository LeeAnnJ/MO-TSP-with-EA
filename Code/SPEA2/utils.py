'''
常用方法工具包
'''
import math


# 判断 func1的值是否支配func2
def is_dominate(func1:list,func2:list):
    dom_less = 0
    if len(func1)!=len(func2):
        raise ValueError("func1's length not equal with func2.")
    for i in range(len(func1)):
        if func1[i]>func2[i]:
            return False
        if func1[i]<func2[i]:
            dom_less+=1
    if dom_less!=0:
        return True
    return False


# 计算距离
def cal_distance(func1:list, func2:list):
    dis = 0
    for i in range(len(func1)):
        dis += (func1[i]-func2[i])*(func1[i]-func2[i])
    return math.sqrt(dis)