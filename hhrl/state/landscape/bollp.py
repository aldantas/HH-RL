from hhrl.util import SolutionSpace


class BoLLP():
    def __init__(self, config, **kwargs):
        self.sample_size = config['BoLLP'].getint('sample_size', 100)
        self.neighborhood_size = config['BoLLP'].getint('neighborhood_size', 3)
        self.sample_space = SolutionSpace(self.sample_size)
        self.histogram = [0] * (2**self.neighborhood_size)

    def compute_llp(self, solution_idx):
        solution = self.sample_space.sample[solution_idx]
        neighbors = self.sample_space.get_nearest_neighbors(
                solution_idx, self.neighborhood_size)
        llp = [1<<i if solution < neighbor else 0
                for i,neighbor in enumerate(neighbors)]
        return sum(llp)

    def update_llp_histogram(self):
        histogram = [0] * (2**self.neighborhood_size)
        for idx in range(len(self.sample_space.sample)):
            llp = self.compute_llp(idx)
            histogram[llp] += 1
        # normalize by sample size
        self.histogram = [x/self.sample_size for x in histogram]

    def reset(self):
        self.sample_space.clear()
        histogram = [0] * (2**self.neighborhood_size)

    def get_state(self):
        return self.histogram

    def update(self, action, reward, solution):
        self.sample_space.update(solution)
        self.update_llp_histogram()
