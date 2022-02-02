class Agent:
    def __init__(self, actions, policy):
        self.actions = actions
        self.policy = policy

    def reset(self):
        raise NotImplementedError

    def select(self):
        action_idx = self.policy.select(self)
        return self.actions[action_idx]

    def get_env_state(self):
        return None

    def update(self, **kwargs):
        raise NotImplementedError
