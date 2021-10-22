import copy


class Solution():
    def __init__(self, id, fitness):
        self.id = id
        self.fitness = fitness

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return (self.fitness, self.id) < (other.fitness, other.id)

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return (self.fitness, self.id) > (other.fitness, other.id)

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def copy(self):
        return copy.deepcopy(self)

    def distance(self, other):
        return 0
