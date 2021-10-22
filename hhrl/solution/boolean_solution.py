from hhrl.solution import Solution


class BooleanSolution(Solution):
    def __init__(self, bool_tuple):
        self.bool_tuple = bool_tuple

    def __str__(self):
        return f'{self.bool_tuple}'

    def distance(self, other):
        diff = [a^b for a,b in zip(self.bool_tuple, other.bool_tuple)]
        return sum(diff)/len(self.bool_list)
