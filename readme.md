# MO-TSP with Evolutionary Algorithm
## 简介
多目标旅行商问题（目前的目标函数还只是两个）的演化算法，python实现，包括NSGA-II和SPEA2，解集的评估指标包括IGD、HV和Spacing

文件结构：
- Code: 演化算法和评估的代码
- Data: 测试数据，来自[TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/index.html)，具体说明可见[官方文档](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/XML-TSPLIB/Description.pdf)
- result：算法的运行结果展示，具体内容见下文

## 配置&运行
### 环境需求
基本环境需求： python>3.8

python库需求: 见 [/Code/requirement](./Code/requirement.txt)

### 运行：

运行单个算法：在方法名对应的文件夹下运行`main.py`即可。以运行NSGA-II方法举例：
```sh
cd ./Code/NSGA-II
python main.py
```

调整算法参数：算法需要的参数都设置在`argument.py`中，在文件中调整即可。

对结果进行评估：运行`/Code/evaluate.py` 即可。

## 关于运行结果
结果文件夹中的文件结构如下：

```
result
|- 方法名称
| |- 数据文件名称
| | |- non_domitated_solution_{iter}.csv: 帕累托前沿的解的全排列表示和函数值，每10/50/100次迭代记录一次
| | |- 帕累托前沿绘图结果,每10/50/100次画一次
| | |- log文件
|- evaluate
| |- 数据文件名称
| | |- eval_HV_pic.png：HV指标随迭代变化的绘图结果
| | |- eval_IGD_pic.png：HV指标随迭代变化的绘图结果
| | |- eval_Spacing_pic.png：HV指标随迭代变化的绘图结果
| | |- eval_result_HSGA.csv：NSGA的各项指标在迭代中的记录
| | |- eval_result_SPEA.csv：SPEA的各项指标在迭代中的记录
```

目前项目中运行结果使用的参数设置为：

|数据名|迭代次数|种群数量|交叉概率|变异概率|
|:--:|:--:|:--:|:--:|:--:|
|bayg29|200|50|0.9|0.3|
|bays29|200|50|0.9|0.3|
|dantzig42|1000|100|0.9|0.5|
|gr120|2000|200|0.9|0.5|
|pa561|2000|200|0.9|0.5|


## Note
代码和结果仅供参考，希望能为入门演化算法的人们提供一点小小的帮助~