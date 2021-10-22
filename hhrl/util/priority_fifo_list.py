import heapq


class PriorityFIFOList(list):
    def  __init__(self, max_len=float('inf'), enable_safe_check=False, inversed_priority=True):
        self.max_len = max_len
        self.count = 0
        self.enable_safe_check = enable_safe_check
        self.inversed_priority = inversed_priority
        list.__init__(self)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max_len and self.n < len(self):
            p, c, x = self[self.n]
            self.n += 1
            if self.inversed_priority:
                p *= -1
            return x, p
        else:
            raise StopIteration()

    def push(self, x, priority):
        if self.inversed_priority:
            priority *= -1
        entry = (priority, self.count, x)
        # entry = (priority, x)
        if self.enable_safe_check and len(self) == self.max_len:
            (lowest_priority, *_) = self[0]
            if priority < lowest_priority:
                return None
        heapq.heappush(self, entry)
        self.count += 1
        if len(self) > self.max_len:
            self.pop()

    def pop(self):
        p, c, x = heapq.heappop(self)
        if self.inversed_priority:
            p *= -1
        return x, p

    def isEmpty(self):
        return len(self) == 0

if __name__ == "__main__":
    l = PriorityFIFOList(10, inversed_priority=True)
    l.push('a', 1)
    l.push('b', 2)
    l.push('c', 3)
    l.push('d', 4)
    l.push('e', 5)
    l.push('f', 6)
    l.push('g', 7)
    print(l)
    # print(l[0])
    print(sorted(l, key=lambda x: -x[1])[:3])
    print(heapq.nsmallest(3, l, key=lambda x: -x[1]))
    # l.remove(l[3])
    # print(l)
    # print(sorted(l)[:3])
    # heapq.heapify(l)
    while not l.isEmpty():
        print(l.pop())
