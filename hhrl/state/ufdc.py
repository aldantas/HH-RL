import numpy as np
from .fdc import FitnessDistanceCorrelation


class UnitaryFitnessDistanceCorrelation(FitnessDistanceCorrelation):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

    def compute_fdc(self):
        cost_list = [sol.fitness for sol in self.solution_list]
        avg_cost, avg_dist = np.mean(cost_list), np.mean(self.dist_list)
        c = cost_list[-1]
        d = self.dist_list[-1]
        product = (c - avg_cost) * (d - avg_dist)
        if product == 0:
            self.fdc = 1
        else:
            std_cost, std_dist = np.std(cost_list), np.std(self.dist_list)
            self.fdc = product / (std_cost * std_dist)
