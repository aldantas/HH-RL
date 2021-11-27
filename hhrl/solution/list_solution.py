import numpy as np
from hhrl.solution import Solution


class ListSolution(Solution):
    def __init__(self, id=0, solution=[], fitness=float('inf')):
        super().__init__(id, solution, fitness=fitness)

    def __str__(self):
        return f'{self.solution}'

    def distance(self, other):
        diff = [1 if a != b else 0 for a, b in zip(self.solution, other.solution)]
        diff.extend([1] * abs(len(self) - len(other)))
        return np.mean(diff)

    def generate_random(self, n=10):
        self.solution = tuple(np.random.permutation(n))
