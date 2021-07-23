from hhrl.problem import HyFlexDomain
from hhrl.solution import BooleanSolution


class MAXSAT(HyFlexDomain):
    def __init__(self, instance_id, seed):
        HyFlexDomain.__init__(self, 'SAT', instance_id, seed)

    def str_to_bool(self, s):
        if s == 'true':
            return True
        else:
            return False

    def get_solution(self, idx=0):
        solution_str = self.problem.solutionToString(idx)
        solution_list = solution_str.strip().split()
        bool_list = [self.str_to_bool(x.split(':')[1]) for x in solution_list]
        return BooleanSolution(bool_list)
