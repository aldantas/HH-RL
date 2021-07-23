import heapq


class PriorityFIFOList(list):
    def  __init__(self, max_len=float('inf')):
        self.max_len = max_len
        self.count = 0
        list.__init__(self)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max_len and self.n < len(self):
            (*_, x) = self[self.n]
            self.n += 1
            return x
        else:
            raise StopIteration()

    def push(self, x, priority):
        # we want to keep the solutions with the lowest objective funcion
        # on the list, hence the priority is inverted. The count is
        # inverted as well because older solutions are kept in case of ties
        entry = (-priority, -self.count, x)
        heapq.heappush(self, entry)
        self.count += 1
        if len(self) > self.max_len:
            self.pop()

    def pop(self):
        (*_, x) = heapq.heappop(self)
        return x

    def isEmpty(self):
        return len(self) == 0

if __name__ == "__main__":
    l = PriorityFIFOList(5)
    l.push(0, 0)
    l.push(1, 1)
    l.push(2, 2)
    print(l)
    for x in l:
        print(x)
