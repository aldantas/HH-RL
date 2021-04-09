import numpy as np
from hhrl.util import SlidingWindow
from .ucb import UCBPolicy


class FRRMABAgent:
    def __init__(self, config, actions, prior=[], **kwargs):
        self.policy = UCBPolicy(config)
        self.prior = prior
        n_actions = len(actions)
        if len(prior) != n_actions:
            self.prior = [.0] * n_actions
        self.value_estimates = self.prior
        self.decay_factor = config['FRRMABAgent'].getfloat('decay_factor', 1)
        window_size = config['FRRMABAgent'].getint('window_size', 100)
        self.sliding_window = SlidingWindow(window_size, n_actions)
        self.action_attempts = self.sliding_window.count_list
        self.actions = actions
        self.t = 0

    def __str__(self):
        return f'FRRMAB - Policy: {str(self.policy)}'

    def reset(self):
        self.value_estimates = self.prior
        self.sliding_window.clear()
        self.t = 0

    def select(self):
        action_idx = self.policy.select(self)
        return self.actions[action_idx]

    def update(self, action, reward):
        self.t += 1
        action_idx = self.actions.index(action)
        self.sliding_window.update(action_idx, reward)

        action_reward_sum = self.sliding_window.sum_list
        ranking = np.argsort(action_reward_sum)[::-1]
        decays = [0] * len(self.actions)
        for rank, action_idx  in enumerate(ranking):
            action_reward = action_reward_sum[action_idx]
            decays[action_idx] = (self.decay_factor ** rank) * action_reward
        decay_sum = sum(decays)
        if decay_sum == 0:
            return
        # Update the value estimates (FRR)
        for action_idx in range(len(self.actions)):
            FRR = decays[action_idx] / decay_sum
            self.value_estimates[action_idx] = FRR
