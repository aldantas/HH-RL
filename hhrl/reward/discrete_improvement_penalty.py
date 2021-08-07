class DiscreteImprovementPenalty:
    def __init__(self, config, actions, *args):
        self.reward = config['Reward'].getfloat('reward', 1.0)
        self.penalty = config['Reward'].getfloat('penalty', .1)

    def get_reward(self, action, new_fitness, past_fitness, *args):
        fir = (past_fitness - new_fitness) / past_fitness
        if fir > 0:
            return self.reward
        else:
            return -self.penalty

    def reset(self):
        pass
