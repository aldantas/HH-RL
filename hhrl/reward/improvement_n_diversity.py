from hhrl.reward import ImprovementRate, Diversity


class ImprovementAndDiversity:
    def __init__(self, config, *args):
        self.imp_ca = ImprovementRate(config, args)
        self.div_ca = Diversity(config, args)

    def get_reward(self, action, new_fitness, past_fitness, solution):
        imp = self.imp_ca.get_reward(action, new_fitness, past_fitness)
        div = self.div_ca.get_reward(action, new_fitness, past_fitness, solution)
        return imp+div

    def reset(self):
        self.imp_ca.reset()
        self.div_ca.reset()
