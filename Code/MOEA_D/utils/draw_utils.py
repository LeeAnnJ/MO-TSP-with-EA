'''
动态展示和绘制图形相关方法
'''
from matplotlib import pyplot as plt
import numpy as np

fig = plt.figure()
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
ax = 0

def show():
    plt.show()

def savefig(file):
    plt.savefig(file)

def draw_MOEAD_pareto(moead, name):
    pareto_F_id = moead.EP_X_ID
    Pop_F_Data = np.array(moead.Pop_FV)

    plt.xlabel('distance', fontsize=10)
    plt.ylabel('profit(*-1)', fontsize=10)
    plt.title(name)

    xmin = np.min(Pop_F_Data[:,0])
    xmax = np.max(Pop_F_Data[:,0])
    ymin = np.min(Pop_F_Data[:,1])
    ymax = np.max(Pop_F_Data[:,1])
    plt.xlim(xmin-20, xmax+20)
    plt.ylim(ymin-20, ymax+20)
    # for pi, pp in enumerate(Pop_F_Data):
    #     plt.scatter(pp[0], pp[1], c='black', s=5)
    plt.scatter(Pop_F_Data[:,0], Pop_F_Data[:,1], c='black', s=5)
    # for pid in pareto_F_id:
    #     p = Pop_F_Data[pid]
    #     plt.scatter(p[0], p[1], c='r', s=20)
    p = Pop_F_Data[pareto_F_id]
    plt.scatter(p[:,0], p[:,1], c='r', s=20)
    pass


def draw_weight(moead):
    start_pts = moead.Z
    data = moead.W
    Pop_F_Data = moead.Pop_FV

    vec_start_x = start_pts[0]
    vec_start_y = start_pts[1]
    vec_end_x = data[:,0]
    vec_end_y = data[:,1]

    for i in range(vec_end_y.shape[0]):
        if i == moead.now_y:
            plt.plot([vec_end_x[i], Pop_F_Data[i][0]], [vec_end_y[i], Pop_F_Data[i][1]])
        plt.plot([vec_start_x, vec_end_x[i]], [vec_start_y, vec_end_y[i]])
    pass