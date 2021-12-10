from hhrl.util import SlidingWindow


class SlidingWindowState:
    def __init__(self, config, actions):
        self.window_size = config['SlidingWindowState'].getint('window_size', 100)
        self.sliding_window = SlidingWindow(self.window_size, len(actions))
        self.actions = actions

    def reset(self):
        self.sliding_window = SlidingWindow(self.window_size, len(self.actions))

    def get_state(self):
        state = [sum/count if count > 0 else 0 for sum,count in zip(
            self.sliding_window.sum_list, self.sliding_window.count_list)]
        return [(float(x)-min(state))/(max(state)-min(state)+1e-16) for x in state]

    def update(self, action, reward, **kwargs):
        action_idx = self.actions.index(action)
        self.sliding_window.update(action_idx, reward)
