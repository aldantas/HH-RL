from hhrl.problem import HyFlexDomain
from hhrl.solution import Solution


class BinPacking(HyFlexDomain):
    def __init__(self, instance_id, seed):
        HyFlexDomain.__init__(self, 'BP', instance_id, seed)

    def get_solution(self, idx=0):
        return Solution()
