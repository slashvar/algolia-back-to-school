class Vector:
    def __init__(self, capacity=1):
        self._data = [None] * capacity
        self._size = 0

    def size(self):
        return self._size

    def capacity(self):
        return len(self._data)

    def push_back(self, elm):
        # Support for dynamic capacity
        if self._size == len(self._data):
            self._data = self._data + ([None] * len(self._data))
        self._data[self._size] = elm
        self._size += 1

    def push_front(self, elm):
        # Support for dynamic capacity
        if self._size == len(self._data):
            self._data = self._data + ([None] * len(self._data))
        # Shift all elements to the right
        for i in range(self._size, 0, -1):
            self._data[i] = self._data[i - 1]
        self._data[0] = elm
        self._size += 1

v = Vector(16)
print(v._data)
for i in range(8):
    v.push_back(i)
print(v._data)
v.push_front(42)
print(v._data)
