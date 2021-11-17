import numpy as np
import bisect
from hhrl.util import SolutionSpace


class DispersionMetric:
    def __init__(self, config, **kwargs):
        self.sample_size = config['Dispersion'].getint('sample_size', 100)
        self.elite_sample_size = config['Dispersion'].getint('elite_sample_size', 10)
        self.sample_space = SolutionSpace(self.sample_size)
        self.solution_sorted_list = []
        self.elite_dispersion = 0
        self.dispersion = 0

    def update_elite_dispersion(self):
        idx_list = []
        for elite in self.solution_sorted_list[:self.elite_sample_size]:
            # get the sample space index of the elite solution
            elite_idx = self.sample_space.sample.index(elite)
            idx_list.append(elite_idx)
        self.elite_dispersion = self.sample_space.get_sample_dispersion(idx_list)

    def reset(self):
        self.sample_space.clear()
        self.solution_sorted_list.clear()
        self.elite_dispersion = 0
        self.dispersion = 0

    def get_state(self):
        return [self.dispersion]

    def update(self, action, reward, solution):
        popped = self.sample_space.update(solution)
        if popped:
            popped_sorted_idx = self.solution_sorted_list.index(popped)
            self.solution_sorted_list.remove(popped)
        else:
            # just to be used in the conditional for updating the elite dispersion
            popped_sorted_idx = float('inf')

        # index to insert the new solution in the sorted list
        insertion_idx = bisect.bisect(self.solution_sorted_list, solution)
        self.solution_sorted_list.insert(insertion_idx, solution)

        if popped_sorted_idx < self.elite_sample_size or insertion_idx < self.elite_sample_size:
            self.update_elite_dispersion()
        sample_dispersion = self.sample_space.get_sample_dispersion()
        self.dispersion = sample_dispersion - self.elite_dispersion
