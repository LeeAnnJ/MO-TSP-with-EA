'''
遗传算法的相关方法
'''
import numpy as np

import utils.moead_utils as Moead_U


def EO_optimition(moead, wi ,p1):
    return p1


def generate_next(moead, gen ,wi, p0, p1, p2):
    cbsv_p0 =  Moead_U.cpt_tchebyshev(moead,wi,p0)
    cbsv_p1 = Moead_U.cpt_tchebyshev(moead,wi,p1)
    cbsv_p2 = Moead_U.cpt_tchebyshev(moead,wi,p2)

    best = np.argmin(np.array([cbsv_p0,cbsv_p1,cbsv_p2]))
    y1 = [p0,p1,p2][best] # 切比雪夫距离最小的个体
    n_p0, n_p1, n_p2 = np.copy(p0),np.copy(p1),np.copy(p2)

    # 交叉
    n_p0,n_p1 = moead.GNO.cross_mutation(n_p0,n_p1)
    n_p1,n_p2 = moead.GNO.cross_mutation(n_p1,n_p2)

    cbsv_np0 = Moead_U.cpt_tchebyshev(moead, wi, n_p0)
    cbsv_np1 = Moead_U.cpt_tchebyshev(moead, wi, n_p1)
    cbsv_np2 = Moead_U.cpt_tchebyshev(moead, wi, n_p2)
    best = np.argmin(np.array([cbsv_p0,cbsv_p1,cbsv_p2,cbsv_np0,cbsv_np1,cbsv_np2]))
    y2 = [p0,p1,p2,n_p0,n_p1,n_p2][best]

    # 随机选中目标中的某一个目标进行判断，目标太多，不要贪心，随机选一个目标就好
    # fm = np.random.randint(0,moead.func_num)
    # if np.random.rand() < 0.3:
    #     Fy1 = moead.problem.func(y1)
    #     Fy2 = moead.problem.func(y2)
    #     if Fy2[fm]< Fy1[fm]:
    #         return y2
    #     else:
    #         return y1
    return y2