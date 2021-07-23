import numpy as np


np.seterr(divide='ignore', invalid='ignore')


class UCBPolicy():
    def __init__(self, config):
        self.c = config['UCBPolicy'].getint('c', 1)

    def __str__(self):
        return f'UCB (c={self.c})'

    def select(self, agent):
        if agent.t == 0:
            exploration = np.zeros(len(agent.actions))
        else:
            attempts_sum = sum(agent.action_attempts)
            exploration = (2 * np.log(attempts_sum)) / agent.action_attempts
            exploration[np.isnan(exploration)] = np.inf #fix the divisions by zero
            exploration = np.sqrt(exploration) * self.c
        q = agent.value_estimates + exploration
        return int(np.argmax(q))
