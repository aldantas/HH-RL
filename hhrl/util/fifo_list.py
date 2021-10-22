class FIFOList(list):
    def __init__(self, max_size):
        self.max_size = max_size
        list.__init__(self)

    def _truncate(self):
        dif = len(self)-self.max_size
        if dif > 0:
            popped = self[:dif][0]
            self[:dif]=[]
            return popped
        return None

    def push(self, x):
        list.append(self, x)
        return self._truncate()

    def is_full(self):
        return len(self) == self.max_size
