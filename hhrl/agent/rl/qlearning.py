from collections import defaultdict

import numpy as np

from hhrl.agent import Agent
from .egreedy import EpsilonGreedyPolicy


class QLearningAgent(Agent):
    def __init__(self, config, actions, state_env, prior=[], **kwargs):
        super().__init__(actions, EpsilonGreedyPolicy(config))
        self.prior = prior
        self.gamma = config['QLearningAgent'].getfloat('gamma', .9)
        n_actions = len(actions)
        if len(prior) != n_actions:
            self.prior = [.0] * n_actions
        self.value_estimates = self.prior
        self.state_env = state_env
        self.learning_rate = config['QLearningAgent'].getfloat('learning_rate', .001)
        self.q_table = defaultdict(lambda: [.0] * n_actions)
        self.state = tuple(self.state_env.get_state())

    def __str__(self):
        return f'QLearning - Policy: {str(self.policy)}'

    def reset(self):
        self.value_estimates = self.prior
        self.state_env.reset()
        self.q_table = defaultdict(lambda: [.0] * len(self.actions))

    def __get_qvalues(self, state):
        return self.q_table[state]

    def get_env_state(self):
        return self.state

    def update(self, action, reward, **kwargs):
        action_idx = self.actions.index(action)
        self.state_env.update(action=action, reward=reward, **kwargs)
        next_state = tuple(self.state_env.get_state())

        next_qvalues = self.__get_qvalues(next_state)

        old_value = (1 - self.learning_rate) * self.q_table[self.state][action_idx]
        temporal_difference = self.learning_rate * (reward + self.gamma * max(next_qvalues))

        self.q_table[self.state][action_idx] = old_value + temporal_difference

        self.state = next_state
        self.value_estimates = next_qvalues
