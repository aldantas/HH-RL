import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.exceptions import NotFittedError
from hhrl.agent import Agent
from .egreedy import EpsilonGreedyPolicy


class DQNAgent(Agent):
    def __init__(self, config, actions, state_env, prior=[], **kwargs):
        super().__init__(actions, EpsilonGreedyPolicy(config))
        self.prior = prior
        self.gamma = config['DQNAgent'].getfloat('gamma', .9)
        n_actions = len(actions)
        if len(prior) != n_actions:
            self.prior = [.0] * n_actions
        self.value_estimates = self.prior
        self.state_env = state_env
        self.learning_rate = config['DQNAgent'].getfloat('learning_rate', .001)
        self.dqn = MLPRegressor(hidden_layer_sizes=(30,20), solver='adam',
                learning_rate_init=self.learning_rate)
        self.state = self.state_env.get_state()

    def __str__(self):
        return f'DQN - Policy: {str(self.policy)}'

    def reset(self):
        self.value_estimates = self.prior
        self.state_env.reset()
        self.dqn = MLPRegressor(hidden_layer_sizes=(30,20), solver='adam',
                learning_rate_init=self.learning_rate)

    def __get_qvalues(self, state):
        try:
            return self.dqn.predict([state])[0]
        except NotFittedError:
            return [0] * len(self.actions)

    def get_env_state(self):
        return self.state

    def update(self, action, reward, **kwargs):
        action_idx = self.actions.index(action)
        self.state_env.update(action=action, reward=reward, **kwargs)
        next_state = self.state_env.get_state()

        next_qvalues = self.__get_qvalues(next_state)
        target_qvalue = reward + self.gamma * max(next_qvalues)
        target = self.value_estimates
        target[action_idx] = target_qvalue
        self.dqn.partial_fit([self.state], [target])

        self.state = next_state
        self.value_estimates = next_qvalues
