class LastActionVector:
    def __init__(self, config, actions, **kwargs):
        self.actions = actions
        self.binary_vector = [0] * len(actions)
        self.last_idx = 0

    def reset(self):
        self.binary_vector = [0] * len(self.actions)

    def get_state(self):
        return self.binary_vector

    def update(self, action, **kwargs):
        action_idx = self.actions.index(action)
        self.binary_vector[self.last_idx] = 0
        self.binary_vector[action_idx] = 1
        self.last_idx = action_idx
