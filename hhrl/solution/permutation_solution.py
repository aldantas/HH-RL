from hhrl.solution import Solution
import numpy as np

class PermutationSolution(Solution):
    def __init__(self, id=0, permutation=[], fitness=float('inf')):
        super().__init__(id, fitness)
        self.permutation = permutation

    def __str__(self):
        return f'{self.permutation}'

    def compare(self, other):
        return self.permutation == other.permutation

    def distance(self, other):
        diff = [1 if a!=b else 0 for a,b in zip(self.permutation, other.permutation)]
        return sum(diff)/len(self.permutation)

    def generate_random(self, n=10):
        self.permutation = tuple(np.random.permutation(n))
