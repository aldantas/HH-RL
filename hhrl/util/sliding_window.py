from .fifo_list import FIFOList


class SlidingWindow:
    def __init__(self, max_size, n_actions):
        self.max_size = max_size
        self.n_actions = n_actions
        self.sliding_window = FIFOList(max_size)
        self.count_list = [0] * n_actions
        self.sum_list = [0] * n_actions

    def clear(self):
        self.sliding_window.clear()
        self.count_list = [0] * self.n_actions
        self.sum_list = [0] * self.n_actions

    def update(self, idx, reward):
        # Insert new action reward
        self.count_list[idx] += 1
        self.sum_list[idx] += reward
        expired = self.sliding_window.push((idx, reward))
        # Remove expiring action rewards
        if expired != None:
            self.count_list[idx] -= 1
            self.sum_list[idx] -= reward
