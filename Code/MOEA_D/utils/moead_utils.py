'''
MOEA/D的相关方法
'''
import numpy as np


# 判断Fx是否支配Fy
def is_dominate(Fx:list,Fy:list):
    i = 0
    for xv, yv in zip(Fx, Fy):
        if xv < yv:
            i = i + 1
        if xv > yv:
            return False
    if i != 0:
        return True
    return False


# 计算切比雪夫距离
def Tchebyshev_dist(w,f,z):
    return w*abs(f-z)

# 计算X与理想点Z的切比雪夫距离
# idx: X在种群中的位置
def cpt_tchebyshev(moead, idx, x):
    max = moead.Z[0]
    ri = moead.W[idx]
    Fx = moead.problem.func(x)
    for i in range (moead.problem.func_num):
        fi = Tchebyshev_dist(ri[i],Fx[i],moead.Z[i])
        if fi>max:
            max = fi
    return max


# 如果id存在，则更新其对应函数集合的值
def update_EP_by_id(moead,id,Fy):
    if id in moead.EP_X_ID:
        pos_pi = moead.EP_X_ID.index(id) # 拿到所在位置
        moead.EP_X_FV[pos_pi][:] = Fy[:] # 更新函数值
    pass


# 根据Y更新Z坐标
def update_Z(moead,y):
    dz = np.random.rand()
    Fy = moead.problem.func(y)
    for i in range(moead.func_num):
        if moead.Z[i]> Fy[i]:
            moead.Z[i] = Fy[i]-dz
    pass


# 根据Y更新前沿
# 根据Y更新EP
def update_EP_by_Y(moead, id_y):
    i = 0
    Fy = moead.Pop_FV[id_y]
    delete_set = [] # 需要被删除的集合
    ep_len = len(moead.EP_X_FV) # 支配前沿集合的数量
    for pi in range(ep_len):
        if is_dominate(Fy,moead.EP_X_FV[pi]):
            delete_set.append(pi)
            break
        if i!=0:
            break
        if is_dominate(moead.EP_X_FV[pi],Fy):
            i += 1
    
    new_EP_X_ID = [] # 新的支配前沿的ID集合，种群个体ID，
    new_EP_X_FV = [] # 新的支配前沿集合的函数值
    for id in range(ep_len):
        if id not in delete_set:
            new_EP_X_ID.append(moead.EP_X_ID[id])
            new_EP_X_FV.append(moead.EP_X_FV[id])
    moead.EP_X_ID = new_EP_X_ID
    moead.EP_X_FV = new_EP_X_FV
    # i==0 意味着没人支配id_y 则y加进支配前沿
    if i==0:
        if id_y not in moead.EP_X_ID:
            moead.EP_X_ID.append(id_y)
            moead.EP_X_FV.append(Fy)
        else: # 本来就在里面的，更新它
            idy = moead.EP_X_ID.index(id_y)
            moead.EP_X_FV[idy] = Fy[:]
    pass


# 根据Y更新P_B集内邻居
def update_BT_X(moead, pb, y):
    for i in pb:
        xi = moead.Pop[i]
        dx = cpt_tchebyshev(moead,i,xi)
        dy = cpt_tchebyshev(moead,i,y)
        if dy<=dx:
            moead.Pop[i] = y[:]
            Fy = moead.problem.func(y)
            moead.Pop_FV[i] = Fy
            update_EP_by_id(moead,i,Fy)
    pass
