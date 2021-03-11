class ImprovementRate:
    def __init__(self, config, actions, *args):
        pass

    def get_reward(self, action, new_fitness, past_fitness):
        return (past_fitness - new_fitness) / past_fitness

    def reset(self):
        pass
