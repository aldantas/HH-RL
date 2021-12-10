class ElapsedTime:
    def __init__(self, config, time_limit, **kwargs):
        self.time_limit = time_limit
        self.elapsed = 0

    def reset(self):
        pass

    def get_state(self):
        return [self.elapsed / self.time_limit]

    def update(self, elapsed, **kwargs):
        self.elapsed = elapsed
