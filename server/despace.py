from collections import UserDict

class Despace(UserDict):
    def __init__(self, *args, **kwargs):
        self.__unused = []
        self.__max = 0
        super().__init__()

    def __delitem__(self, key):
        self.__unused.append(key)
        super().__delitem__(key)

    def add(self, item):
        if len(self.__unused):
            key = self.__unused.pop()
        else:
            key = self.__max
            self.__max += 1

        self[key] = item

