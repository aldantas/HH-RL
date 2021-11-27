import copy


class Solution:
    def __init__(self, id, solution, fitness):
        self.id = id
        self.solution = solution
        self.fitness = fitness

    def __len__(self):
        return len(self.solution)

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

    def compare(self, other):
        return self.solution == other.solution

    def distance(self, other):
        return 0
