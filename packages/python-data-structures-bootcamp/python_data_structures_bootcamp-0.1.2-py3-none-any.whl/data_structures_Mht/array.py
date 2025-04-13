class Array:
    def __init__(self, cap=5):
        self.data = [None] * cap
        self.cap = cap
        self.size = 0

    def append(self, value):
        if self.size >= self.cap:
            self._resize()
        self.data[self.size] = value
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise IndexError("Pop from empty array")
        self.size -= 1
        value = self.data[self.size]
        self.data[self.size] = None
        return value

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds bro")
        return self.data[index]

    def last(self):
        if self.size == 0:
            return None
        return self.data[self.size - 1]

    def is_empty(self):
        return self.size == 0

    def _resize(self):
        self.cap *= 2
        self.data += [None] * (self.cap - len(self.data))

    def __str__(self):
        return str(self.data[:self.size])
