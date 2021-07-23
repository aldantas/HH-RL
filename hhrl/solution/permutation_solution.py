from hhrl.solution import Solution


class PermutationSolution(Solution):
    def __init__(self, permutation):
        self.permutation = permutation

    def __str__(self):
        return f'{self.permutation}'

    def __eq__(self, other):
        return self.permutation == other.permutation

    def __ne__(self, other):
        return not self.__eq__(other)

    def distance(self, other):
        diff = [1 if a!=b else 0 for a,b in zip(self.permutation, other.permutation)]
        return sum(diff)/len(self.permutation)
