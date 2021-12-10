class StateBuilder:
    def __init__(self, state_classes, config, **kwargs):
        self.states = [state_cls(config, **kwargs) for state_cls in state_classes]

    def reset(self):
        for state_obj in self.states:
            state_obj.reset()

    def get_state(self):
        state = []
        for state_obj in self.states:
            state.extend(state_obj.get_state())
        return state

    def update(self, **kwargs):
        for state_obj in self.states:
            state_obj.update(**kwargs)
