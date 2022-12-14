import sys
import typing
from itertools import zip_longest


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

Packet = typing.Union[list[int], list['Packet']]


class PairIterator:
    def __init__(self, filename: str):
        self.__f = open(filename, 'r')

    def __iter__(self):
        return self

    def __next__(self) -> tuple[Packet]:
        if self.__f.closed:
            raise StopIteration
        pair: tuple[Packet] =  tuple(eval(self.__f.readline()) for _ in range(2))
        end = self.__f.readline()
        if end == '':
            self.__f.close()
        return pair


def is_sorted(pair: tuple[Packet]) -> bool:
    a, b = pair
    match a, b:
        case int(), int():
            return a < b

        case int(), None:
            return False

        case None, int() | list():
            return True

        case list(), None:
            return False

        case int(), list():
            return is_sorted(([a], b))

        case list(), int():
            return is_sorted((a, [b]))

        case list(), list():
            for l, r in zip(a, b):
                if is_sorted((l, r)):
                    return True
                elif is_sorted((r, l)):  # elif not equal (l > r)
                    return False

            return len(a) < len(b)

        case _:
            raise NotImplementedError


def solve(filename):

    sum_of_indices = 0
    for i, pair in enumerate(PairIterator(filename), start=1):
        print(f"\nPAIR {i} {pair=}",
              '\n\n'.join(f"\t(L):{p1}\n\t(R):{p2}"
                          for p1, p2 in zip_longest(*pair)))
        if is_sorted(pair):
            print(f"Correct {i}")
            sum_of_indices += i

    return sum_of_indices, 0


if __name__ == "__main__":
    part1, _ = solve(FILENAME)

    print("ANSWER",
          f"Part 1: {part1}",
          sep='\n')
