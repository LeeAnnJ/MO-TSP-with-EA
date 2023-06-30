# Multi-objective Travelling Salesman Problem：

## 参考文献：

- Multi-objective traveling salesman problem: an ABC approach：
https://link.springer.com/article/10.1007/s10489-020-01713-4

- TSPLIB：http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/index.html

- An Evolutionary Algorithm Applied to the Bi-Objective Travelling Salesman Problem：https://link.springer.com/chapter/10.1007/978-3-031-26504-4_42

## 多目标优化主要算法

- MOEA/D:A Multiobjective Evolutionary Algorithm Based on Decomposition
https://ieeexplore.ieee.org/document/4358754  
github 框架 python实现： https://github.com/moead-framework/framework  
Pruvost, Geoffrey, Bilel Derbel, and Arnaud Liefooghe. "Moead-framework: a modular MOEA/D python framework." Journal of Open Source Software 7.78 (2022): 2974.: https://inria.hal.science/hal-03818749/document
具体问题实现：https://github.com/OnlySekai/mo-tsp-by-moead
参考代码：https://github.com/425776024/MOEAD/tree/master


- NSGA-Ⅲ：K. Deb and H. Jain, “An Evolutionary Many-Objective Optimization Algorithm Using Reference-Point-Based Nondominated Sorting Approach, Part I: Solving Problems With Box Constraints,” IEEE Transactions on Evolutionary Computation, vol. 18, no. 4, pp. 577–601, Aug. 2014, doi: 10.1109/TEVC.2013.2281535.  
NSGA-Ⅱ实现：https://github.com/tsoernes/multiobjective-tsp  
An effective method for solving multiple travelling salesman problem based on NSGA-II： https://www.tandfonline.com/doi/full/10.1080/21642583.2019.1674220?scroll=top&needAccess=true&role=tab&aria-labelledby=full-article  
算法讲解：https://zhuanlan.zhihu.com/p/144807879

- spea:[Zitzler et. al., 2001] Zitzler, Eckart, Marco Laumanns, and Lothar Thiele. “SPEA2: Improving the Strength Pareto Evolutionary Algorithm.” Zurich, Switzerland: ETH Zurich, 2001. https://doi.org/10.3929/ethz-a-004284029.


## chatgpt:

在多目标优化演化算法中，以下是一些目前常用的算法：

- [x] 非支配排序遗传算法（Non-dominated Sorting Genetic Algorithm，NSGA）及其改进版本（如NSGA-II、NSGA-III）：NSGA是多目标优化领域最经典的算法之一，通过将个体按照非支配关系进行排序，实现多个目标之间的均衡优化

- [x] 多目标进化策略（Multi-objective Evolutionary Strategy，MOEA）：MOEA是另一种常用的多目标优化算法，通过使用进化策略的思想，结合变异、交叉等操作来搜索多目标空间中的解。

- [ ] 多目标遗传规划（Multi-objective Genetic Programming，MOGP）：MOGP使用遗传规划的思想，通过进化生成和优化程序来解决多目标优化问题。

- [ ] 题外求助算法（Pareto Archived Evolution Strategy，PAES）：PAES基于进化策略思想，使用网格搜索策略来寻找Pareto前沿上的解。

- [ ] 压缩遗传算法（Indicator-Based Evolutionary Algorithm，IBEA）：IBEA通过使用指标来评估个体的优劣，并使用压缩技术来快速搜索Pareto前沿。

- [ ] 引导多目标优化算法（Preference-Inspired Coevolutionary Algorithm，PICEA）：PICEA使用偏好信息来引导搜索过程，提高算法在多目标优化中的性能。

以上只是多目标优化演化算法的一些常见例子，实际上还有很多其他的算法和改进版本，因此选择适合具体问题的算法需要结合问题特点和需求进行综合考虑。

## 记一下预计产出的内容
- 对每个方法文件夹：
  - 数据文件名称
    - 每50/100次迭代的解集/函数评估结果
    - 帕累托前沿绘图结果(如果可以，每50/100次画一次)
    - 最终的一个解决方案的绘图结果
    - log文件
  - 时间统计结果 
- 解集评估结果


## 目前的参数设置
### MOEA/D
|文件|迭代次数|种群数量|交叉概率|变异概率|
|:--:|:--:|:--:|:--:|:--:|
|bayg29|100|0.9|0.5|
|bays29|200|0.9|0.5|
|dantzig42|500|0.9|0.5|
|gr120|1000|0.9|0.5|
|pa561|1000|||

### MOEA/D
|文件|迭代次数|种群数量|交叉概率|变异概率|
|:--:|:--:|:--:|:--:|:--:|
|bayg29|100|50|0.9|0.5|
|bays29|200|50|0.9|0.3|
|dantzig42|500|100|0.9|0.5|
|gr120|1000|100|0.9|0.5|
|pa561|2000|200|0.9|0.5|