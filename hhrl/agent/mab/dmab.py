from hhrl.util.page_hinkley import PageHinkley
from hhrl.agent import Agent
from .ucb import UCBPolicy


class DMABAgent(Agent):
    def __init__(self, config, actions, prior=[], **kwargs):
        super().__init__(actions, UCBPolicy(config))
        self.prior = prior
        n_actions = len(actions)
        if len(prior) != n_actions:
            self.prior = [.0] * n_actions
        self.value_estimates = self.prior
        self.action_attempts = [0] * n_actions
        self.t = 0
        self.ph = PageHinkley(config)
        self.n, self.p = 0, 0

    def __str__(self):
        return f'DMAB - Policy: {str(self.policy)}'

    def reset(self):
        self.value_estimates = self.prior
        self.action_attempts = [0] * len(self.actions)
        self.t = 0

    def update(self, action, reward, **kwargs):
        self.ph.add_element(reward)
        if self.ph.detected_change():
            self.p += 1
            self.reset()
            return
        action_idx = self.actions.index(action)
        self.action_attempts[action_idx] += 1
        self.t += 1
        self.n += 1

        # Update the empirical reward (average)
        n = self.action_attempts[action_idx]
        q = self.value_estimates[action_idx]
        new_q = (q * (n-1) + reward) / n #online average
        self.value_estimates[action_idx] = new_q
