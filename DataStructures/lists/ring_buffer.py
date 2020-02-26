class RingQueue:
    def __init__(self, max_size):
        self._data = [None] * max_size
        self._begin = 0
        self._size = 0

    def push(self, elm):
        if self._size == len(self._data): raise Exception('Queue is full')
        pos = (self._begin + self._size) % len(self._data)
        self._data[pos] = elm
        self._size += 1

    def pop(self):
        if self._size == 0: return None
        res = self._data[self._begin]
        self._begin = (self._begin + 1) % len(self._data)
        self._size -= 1
        return res

    def is_empty(self):
        return self._size == 0

queue = RingQueue(5)
for i in range(5):
    queue.push(i)

while not queue.is_empty():
    print(queue.pop())
