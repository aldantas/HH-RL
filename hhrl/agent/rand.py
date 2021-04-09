import random


class RandomAgent:
    def __init__(self, config, actions, prior=[], **kwargs):
        self.policy = RoulettePolicy(config)
        self.actions = actions
        self.prior = prior
        n_actions = len(actions)
        if len(prior) != n_actions:
            self.prior = [float(1/n_actions)] * n_actions
        self.value_estimates = self.prior

    def __str__(self):
        return f'Random Selection'

    def reset(self):
        self.value_estimates = self.prior

    def select(self):
        action_idx = self.policy.select(self)
        return self.actions[action_idx]

    def update(self, action, reward):
        pass


class RoulettePolicy():
    def __init__(self, config):
        pass

    def __str__(self):
        return f'Roulette Wheel'

    def select(self, agent):
        sample = range(len(agent.actions))
        return random.choices(sample, weights=agent.value_estimates)[0]
