from hhrl.solution import Solution


class BooleanSolution(Solution):
    def __init__(self, bool_list):
        self.bool_list = bool_list

    def __str__(self):
        return f'{self.bool_list}'

    def __eq__(self, other):
        return self.bool_list == other.bool_list

    def __ne__(self, other):
        return not self.__eq__(other)

    def distance(self, other):
        diff = [a^b for a,b in zip(self.bool_list, other.bool_list)]
        return sum(diff)/len(self.bool_list)
