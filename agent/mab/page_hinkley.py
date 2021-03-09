class PageHinkley:
    def __init__(self, config):
        self.delta = config['PageHinkley'].getfloat('delta', .005)
        self.threshold = config['PageHinkley'].getint('threshold', 50)
        self.reward_mean = None
        self.mt = None
        self.mt_list = []
        self.sample_count = None
        self.sum = None
        self.in_concept_change = None
        self.reset()

    def reset(self):
        self.in_concept_change = False
        self.mt_list = []
        self.sample_count = 1
        self.reward_mean = 0.0
        self.mt = 0.0
        self.sum = 0.0

    def detected_change(self):
        return self.in_concept_change

    def add_element(self, x):
        if self.in_concept_change:
            self.reset()
        self.reward_mean = (self.reward_mean + x) / float(self.sample_count)
        self.mt += x - self.reward_mean + self.delta
        self.mt_list.append(self.mt)
        # self.x_mean = self.x_mean + (x - self.x_mean) / float(self.sample_count)
        # self.sum = max(0., self.alpha * self.sum + (x - self.x_mean - self.delta))
        self.sum = max(self.mt_list)
        self.sample_count += 1
        if self.sum - self.mt > self.threshold:
            self.in_concept_change = True
