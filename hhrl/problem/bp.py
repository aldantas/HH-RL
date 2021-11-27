import re
from hhrl.problem import HyFlexDomain
from hhrl.solution import ListSolution


class BinPacking(HyFlexDomain):

    re_bin_items = re.compile(r'(\d+\.0, )')

    def __init__(self, instance_id, seed):
        HyFlexDomain.__init__(self, 'BP', instance_id, seed)

    def get_solution(self, idx=0):
        solution_str = self.problem.solutionToString(idx)
        sorted_bins = []
        for bin in solution_str.split('\n')[:-2]:
            items = [float(it.strip('[, ]')) for it in re.findall(self.re_bin_items, bin)]
            sorted_bins.append(sorted(items))
        sorted_bins.sort()
        fitness = self.get_fitness(idx)
        id = next(self.solution_indexer)
        return ListSolution(id, sorted_bins, fitness)
