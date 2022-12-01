from collections import namedtuple
from heapq import nlargest


Elf = namedtuple("Elf", "id calories")


class ElfIterator:
    def __init__(self, filename):
        self.filename = filename
        self.__i = 0
        self.__EOF = False

    def __iter__(self):
        self.f = open(self.filename, 'r')
        return self

    def __next__(self):
        if self.__EOF:
            raise StopIteration
        calories = 0
        self.__i += 1
        while (line:= self.f.readline() ) not in  ('\n', ''):
            calories += int(line)

        if line == '':
            self.f.close()
            self.__EOF = True
        return Elf(self.__i, calories)


res = nlargest(3, ElfIterator("input.txt"), key=lambda elf: elf.calories)

print(f'ANSWER: {sum(e.calories for e in res)} ({res})')
