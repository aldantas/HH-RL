from .fifo_list import FIFOList


class SolutionSpace:
    def __init__(self, max_size):
        self.max_size = max_size
        self.sample = FIFOList(max_size)
        self.distance_matrix = FIFOList(max_size)

    def clear(self):
        self.memory = FIFOList(self.max_size)
        self.distance_matrix = [FIFOList(self.max_size) for _ in range(self.max_size)]

    def __str__(self):
        for sol in self.memory:
            print(sol)
        for row in self.distance_matrix:
            print(f'{[dist for dist,sol in row]}')
        return ''

    def get_nearest_neighbors(self, idx, n):
        return [sol for dist,sol in sorted(self.distance_matrix[idx])[:n]]

    def get_sample_dispersion(self, idx_list=None):
        if not idx_list:
            idx_list = list(range(len(self.sample)))
        if len(idx_list) <= 1:
            return 0
        dist_sum = 0
        count = 0
        for l_idx, i in enumerate(idx_list[:-1]):
            for j in idx_list[l_idx+1:]:
                dist_sum += self.distance_matrix[i][j][0]
                count += 1
        return dist_sum / count

    def update(self, new_solution):
        # push new solution and remove the oldest if the memory is full
        popped = self.sample.push(new_solution)
        new_solution_dists = FIFOList(self.max_size)
        # remove the first row of the matrix, corresponding to the removed
        # solution and append the new row
        self.distance_matrix.push(new_solution_dists)
        for i, sol in enumerate(self.sample[:-1]):
            distance = new_solution.distance(sol)
            # create the new row of items that will be appended to the matrix
            new_solution_dists.push((distance, sol))
            # remove the first column item and append new value to the last column
            self.distance_matrix[i].push((distance, new_solution))
        # append the distance to itself value of the row
        # use float('inf') so it does not count as the nearest neighbor when sorting the list
        new_solution_dists.append((float('inf'), new_solution))
        return popped
