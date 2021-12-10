class FitnessImprovementRate:
    def __init__(self, config, **kwargs):
        self.discrete = config['FIR'].getboolean('discrete', False)
        self.fir = 0
        self.last_fitness = None

    def reset(self):
        self.fir = 0
        self.last_fitness = None

    def _get_discrete_state(self):
        if self.fir > 0:
            return 1
        elif self.fir == 0:
            return 0
        else:
            return -1

    def get_state(self):
        if self.discrete:
            return [self._get_discrete_state()]
        return [self.fir]

    def update(self, solution, **kwargs):
        if self.last_fitness != None:
            self.fir = (self.last_fitness - solution.fitness) / self.last_fitness
        self.last_fitness = solution.fitness
