import jnius_config
jnius_config.set_classpath('.', 'hyflex/*')
from jnius import autoclass
from itertools import count
import json
from hhrl.solution import Solution


class HyFlexDomain:

    solution_indexer = count(1)

    def __init__(self, problem_str, instance_id, seed):
        with open(f'hyflex/problems_json/{problem_str}.json', 'r') as json_file:
            self.problem_dict = json.load(json_file)
        ProblemClass = autoclass(self.problem_dict['class'])
        self.problem = ProblemClass(seed)
        self.problem.loadInstance(instance_id)
        try:
            self.instance_name = self.problem_dict['instances'][str(instance_id)]
        except KeyError:
            self.instance_name = f'id_{instance_id}'
        self.actions = self.problem_dict['actions']

    def initialise_solution(self, idx=0):
        self.problem.initialiseSolution(idx)

    def get_fitness(self, idx=0):
        return self.problem.getFunctionValue(idx)

    def apply_heuristic(self, llh, src_idx=0, dest_idx=1):
        return self.problem.applyHeuristic(llh, src_idx, dest_idx)

    def accept_solution(self, src_idx=1, dest_idx=0):
        self.problem.copySolution(src_idx, dest_idx)

    def get_best_fitness(self):
        return self.problem.getBestSolutionValue()

    def get_solution(self, idx=0):
        solution_str = self.problem.solutionToString(idx)
        id = next(self.solution_indexer)
        return Solution(id, solution_str, self.get_fitness(idx))
