import numpy as np
from hhrl.util.fifo_list import FIFOList
from .ucb import UCBPolicy


class FRRMABAgent:
    def __init__(self, config, actions, prior=[]):
        self.policy = UCBPolicy(config)
        self.prior = prior
        n_actions = len(actions)
        if len(prior) != n_actions:
            self.prior = [.0] * n_actions
        self.value_estimates = self.prior
        self.D = config['FRRMABAgent'].getint('D', 1)
        W = config['FRRMABAgent'].getint('W', 100)
        self.sliding_window = FIFOList(W)
        self.action_attempts = [0] * n_actions
        self.action_reward_sum = [0] * n_actions
        self.actions = actions
        self.t = 0

    def __str__(self):
        return f'FRRMAB - Policy: {str(self.policy)}'

    def reset(self):
        self.value_estimates = self.prior
        self.action_attempts = [0] * len(self.actions)
        self.action_reward_sum = [0] * len(self.actions)
        self.sliding_window.clear()
        self.t = 0

    def select(self):
        action_idx = self.policy.select(self)
        return self.actions[action_idx]

    def update(self, reward, action):
        self.t += 1
        action_idx = self.actions.index(action)
        # Insert new action reward
        self.action_attempts[action_idx] += 1
        self.action_reward_sum[action_idx] += reward
        expired = self.sliding_window.append((action_idx, reward))
        # Remove expring action rewards
        for action_idx, reward in expired:
            self.action_attempts[action_idx] -= 1
            self.action_reward_sum[action_idx] -= reward

        ranking = np.argsort(self.action_reward_sum)[::-1]
        decays = [0] * len(self.actions)
        for rank, action_idx  in enumerate(ranking):
            action_reward = self.action_reward_sum[action_idx]
            decays[action_idx] = (self.D ** rank) * action_reward
        decay_sum = sum(decays)
        if decay_sum == 0:
            return
        # Update the value estimates (FRR)
        for action_idx in range(len(self.actions)):
            FRR = decays[action_idx] / decay_sum
            self.value_estimates[action_idx] = FRR
