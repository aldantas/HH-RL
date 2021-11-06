import random
from hhrl.agent import Agent


class RandomAgent(Agent):
    def __init__(self, config, actions, state_env, prior=[], **kwargs):
        super().__init__(actions, RoulettePolicy(config))
        self.prior = prior
        n_actions = len(actions)
        if len(prior) != n_actions:
            self.prior = [float(1/n_actions)] * n_actions
        self.value_estimates = self.prior
        self.state_env = state_env
        self.state = self.state_env.get_state()

    def __str__(self):
        return f'Random Selection'

    def reset(self):
        self.value_estimates = self.prior

    def get_env_state(self):
        return self.state

    def update(self, action, reward, solution):
        self.state_env.update(action, reward, solution)
        self.state = self.state_env.get_state()


class RoulettePolicy():
    def __init__(self, config):
        pass

    def __str__(self):
        return f'Roulette Wheel'

    def select(self, agent):
        sample = range(len(agent.actions))
        return random.choices(sample, weights=agent.value_estimates)[0]
