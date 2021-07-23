class ImprovementRate:
    def __init__(self, config, actions, *args):
        pass

    def get_reward(self, action, new_fitness, past_fitness, *args):
        fir = (past_fitness - new_fitness) / past_fitness
        return max(0, fir)

    def reset(self):
        pass
