import numpy as np
from hhrl.util.fifo_list import FIFOList


class FitnessDistanceCorrelation:
    def __init__(self, config, **kwargs):
        self.sample_size = config['FDC'].getint('sample_size', 10)
        self.solution_list = FIFOList(self.sample_size)
        self.dist_list = FIFOList(self.sample_size)
        self.optima_list = []
        self.fdc = 0

    def update_optima_list(self, solution):
        if len(self.optima_list) == 0:
            self.optima_list.append(solution)
            return True
        if solution.fitness < self.optima_list[0].fitness:
            self.optima_list = [solution]
            return True
        if solution.fitness == self.optima_list[0].fitness:
            for optimum in self.optima_list:
                if solution.compare(optimum):
                    break
            else:
                self.optima_list.append(solution)
                return True
        return False

    def update_dist_list(self):
        for idx, solution in enumerate(self.solution_list):
            # compare with the last appended optimum
            dist = solution.distance(self.optima_list[-1])
            if len(self.optima_list) == 1 or dist < self.dist_list[idx]:
                self.dist_list[idx] = dist

    def distance_to_closest_optimum(self, solution):
        dist = float('inf')
        for optimum in self.optima_list:
            aux_dist = solution.distance(optimum)
            if aux_dist < dist:
                dist = aux_dist
        return dist

    def compute_fdc(self):
        cost_list = [sol.fitness for sol in self.solution_list]
        avg_cost, avg_dist = np.mean(cost_list), np.mean(self.dist_list)
        product_sum = sum([
            (c - avg_cost) * (d - avg_dist) for c, d in zip(cost_list, self.dist_list)
            ])
        if product_sum == 0:
            self.fdc = 1
        else:
            std_cost, std_dist = np.std(cost_list), np.std(self.dist_list)
            self.fdc = (product_sum / self.sample_size) / (std_cost * std_dist)

    def reset(self):
        self.solution_list.clear()
        self.dist_list.clear()
        self.optima_list= []
        self.fdc = 0

    def get_state(self):
        return [self.fdc]

    def update(self, solution, **kwargs):
        if self.update_optima_list(solution):
            self.update_dist_list()
        self.solution_list.push(solution)
        self.dist_list.push(self.distance_to_closest_optimum(solution))
        self.compute_fdc()
