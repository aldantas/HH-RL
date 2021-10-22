from hhrl.util.priority_fifo_list import PriorityFIFOList


class Diversity:
    def __init__(self, config, *args):
        self.window_size = config['Reward'].getint('window_size', 10)
        self.elite_solutions = PriorityFIFOList(self.window_size)

    def get_reward(self, action, new_fitness, past_fitness, solution):
        dist_sum = 0
        for sol, fitness in self.elite_solutions:
            dist_sum += solution.distance(sol)
        self.elite_solutions.push(solution, new_fitness)
        return dist_sum / self.window_size

    def reset(self):
        self.elite_solutions.clear()
