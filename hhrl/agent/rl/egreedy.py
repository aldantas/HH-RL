import numpy as np
import random


class EpsilonGreedyPolicy():
    def __init__(self, config):
        self.epsilon = config['EpsilonGreedyPolicy'].getfloat('epsilon', 0.05)

    def __str__(self):
        return f'EpsilonGreedy (epsilon={self.epsilon})'

    def select(self, agent):
        if random.random() < self.epsilon:
            return random.randrange(len(agent.actions))
        return np.argmax(agent.value_estimates)
