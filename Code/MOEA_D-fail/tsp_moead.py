from moead_framework.algorithm.abstract_moead import AbstractMoead
from moead_framework.core.parent_selector.two_random_parent_selector import TwoRandomParentSelector
from moead_framework.core.termination_criteria.max_evaluation import MaxEvaluation


"""
Constructor of the algorithm.

:param problem: {:class:`~moead_framework.problem.Problem`} 待优化的问题
:param max_evaluation: {integer} 迭代次数
:param number_of_weight_neighborhood: {integer} 邻居个数
:param aggregation_function: {:class:`~moead_framework.aggregation.functions.AggregationFunction`} 聚合函数
:param weight_file: {string} 权重文件的路径。每一行代表一个权重向量, 每一列代表一个坐标。
:param termination_criteria: Optional 终止标准 -- {:class:`~moead_framework.core.termination_criteria.abstract_termination_criteria.TerminationCriteria`} The default component is {:class:`~moead_framework.core.termination_criteria.max_evaluation.MaxEvaluation`}
:param genetic_operator: Optional -- {:class:`~moead_framework.core.genetic_operator.abstract_operator.GeneticOperator` 交叉变异算子
:param parent_selector: Optional -- {:class:`~moead_framework.core.parent_selector.abstract_parent_selector.ParentSelector`} 取决于交叉变异算子需要的解的数量
:param mating_pool_selector: Optional -- {:class:`~moead_framework.core.selector.abstract_selector.MatingPoolSelector`} The default selector is {:class:`~moead_framework.core.selector.closest_neighbors_selector.ClosestNeighborsSelector`}
:param sps_strategy: Optional -- {:class:`~moead_framework.core.sps_strategy.abstract_sps.SpsStrategy`} The default strategy is {:class:`~moead_framework.core.sps_strategy.sps_all.SpsAllSubproblems`}
:param offspring_generator: Optional -- {:class:`~moead_framework.core.offspring_generator.abstract_mating.OffspringGenerator`} The default generator is {:class:`~moead_framework.core.offspring_generator.offspring_generator.OffspringGeneratorGeneric`}
:param number_of_weight: Deprecated
:param number_of_objective: Deprecated
"""

class TspMoead(AbstractMoead):
    def __init__(self, problem, max_evaluation,number_of_weight_neighborhood, result_folder,
                 aggregation_function, weight_file, 
                 termination_criteria = None,
                 genetic_operator=None,
                 parent_selector=TwoRandomParentSelector,
                 mating_pool_selector=None,
                 sps_strategy=None,
                 offspring_generator=None,
                 number_of_weight=None,
                 number_of_objective=None):
        self.result_folder = result_folder # 保存结果的文件
        super().__init__(problem=problem, 
                         max_evaluation = max_evaluation, 
                         number_of_weight_neighborhood = number_of_weight_neighborhood, 
                         aggregation_function = aggregation_function,
                         weight_file = weight_file,
                         # termination_criteria= termination_criteria, 
                         genetic_operator = genetic_operator, 
                         parent_selector = parent_selector, 
                         mating_pool_selector = mating_pool_selector,
                         sps_strategy = sps_strategy,
                         offspring_generator = offspring_generator, 
                         number_of_weight= number_of_weight, 
                         number_of_objective = number_of_objective)