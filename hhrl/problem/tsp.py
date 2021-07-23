from hhrl.problem import HyFlexDomain
from hhrl.solution import PermutationSolution


class TSP(HyFlexDomain):
    def __init__(self, instance_id, seed):
        HyFlexDomain.__init__(self, 'TSP', instance_id, seed)

    def get_solution(self, idx=0):
        solution_str = self.problem.solutionToString(idx)
        solution_str = solution_str.split('\n')[1].strip()
        permutation = [int(x) for x in solution_str.split(' ')]
        solution = PermutationSolution(permutation)
        return solution
