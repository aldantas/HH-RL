from .fifo_list import FIFOList


class ExtremeValue:
    def __init__(self, config, n_actions, normalize=False):
        self.window_size = config['ExtremeValue'].getint('window_size', 20)
        self.normalize = normalize
        self.n_actions = n_actions
        self.reward_windows = [FIFOList(self.window_size) for _ in range(n_actions)]

    def get_reward(self, value, action_idx):
        action_reward_window = self.reward_windows[action_idx]
        action_reward_window.append(value)
        reward = max(action_reward_window)
        if self.normalize:
            return self.normalize_reward(reward)
        return reward

    def normalize_reward(self, reward):
        highest_reward = float('-inf')
        for action_window in self.reward_windows:
            if len(action_window) > 0:
                max_r = max(action_window)
                highest_reward = max(highest_reward, max_r)
        return 0 if highest_reward == 0 else reward/highest_reward

    def reset(self):
        self.reward_windows = [FIFOList(self.window_size) for _ in range(self.n_actions)]
