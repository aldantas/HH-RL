class ImprovementOrPenalty:
    def __init__(self, config, actions, *args):
        self.penalty = config['Reward'].getfloat('penalty', .1)

    def get_reward(self, action, new_fitness, past_fitness, *args):
        fir = (past_fitness - new_fitness) / past_fitness
        if fir > 0:
            return fir
        else:
            return -self.penalty

    def reset(self):
        pass
