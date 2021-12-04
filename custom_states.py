from hhrl.state import *
from hhrl.state.landscape import *


class State1:
    def __init__(self, config, **kwargs):
        self.fir = FitnessImprovementRate(config, **kwargs)
        self.la_vec = LastActionVector(config, **kwargs)

    def reset(self):
        self.fir.reset()
        self.la_vec.reset()

    def get_state(self):
        return self.fir.get_state() + self.la_vec.get_state()

    def update(self, action, reward, solution):
        self.fir.update(action, reward, solution)
        self.la_vec.update(action, reward, solution)


class State2:
    def __init__(self, config, **kwargs):
        self.ufdc = UnitaryFitnessDistanceCorrelation(config, **kwargs)
        self.la_vec = LastActionVector(config, **kwargs)

    def reset(self):
        self.ufdc.reset()
        self.la_vec.reset()

    def get_state(self):
        return self.ufdc.get_state() + self.la_vec.get_state()

    def update(self, action, reward, solution):
        self.ufdc.update(action, reward, solution)
        self.la_vec.update(action, reward, solution)


class State3:
    def __init__(self, config, **kwargs):
        self.la_vec = LastActionVector(config, **kwargs)

    def reset(self):
        self.la_vec.reset()

    def get_state(self):
        return self.la_vec.get_state()

    def update(self, action, reward, solution):
        self.la_vec.update(action, reward, solution)


class State4:
    def __init__(self, config, **kwargs):
        self.fir = FitnessImprovementRate(config, **kwargs)
        self.ufdc = UnitaryFitnessDistanceCorrelation(config, **kwargs)
        self.la_vec = LastActionVector(config, **kwargs)

    def reset(self):
        self.fit.reset()
        self.ufdc.reset()
        self.la_vec.reset()

    def get_state(self):
        return self.fir.get_state() + self.ufdc.get_state() + self.la_vec.get_state()

    def update(self, action, reward, solution):
        self.fir.update(action, reward, solution)
        self.ufdc.update(action, reward, solution)
        self.la_vec.update(action, reward, solution)


custom_state_dict = {
        'S1': State1,
        'S2': State2,
        'S3': State3,
        'S4': State4,
        }
