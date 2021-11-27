from hhrl.problem import HyFlexDomain
from hhrl.solution import ListSolution


class TravelingSalesman(HyFlexDomain):
    def __init__(self, instance_id, seed):
        HyFlexDomain.__init__(self, 'TSP', instance_id, seed)

    def get_solution(self, idx=0):
        solution_str = self.problem.solutionToString(idx)
        solution_str = solution_str.split('\n')[1].strip()
        permutation = tuple((int(x) for x in solution_str.split(' ')))
        fitness = self.get_fitness(idx)
        id = next(self.solution_indexer)
        return ListSolution(id, permutation, fitness)
