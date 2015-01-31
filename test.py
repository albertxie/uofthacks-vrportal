class Stack(list):

    def __init__(self, M):
        self.maxSize = M
        self._data = []


    def add(self, element):

        if len(self._data) < self.maxSize:
            self._data.append(element)

        else:
            self._data = [self._data[x - 1] for x in range(len(self._data))]
            self._data[-1] = element


    def midpoint(self):
        if len(self._data) > 0:
            cache = self._data[::]
            cache.sort()
            return cache[len(cache) // 2]

        else:
            raise Exception("Stack must be populated to get midpoint.")


if __name__ == '__main__':

    S = Stack(10)
    for x in range(100):
        import random
        a = random.randint(0, 100)
        print(a)
        S.add(a)

    print("SAKDJFHSALKJFHSADLF")
    print(S.midpoint())
