import sys
import typing
from itertools import zip_longest


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "test_input.txt"


class PairIterator:
    def __init__(self, filename: str):
        self.__f = open(filename, 'r')

    def __iter__(self):
        return self

    def __next__(self) -> tuple[list[int | list[int]]]:
        if self.__f.closed:
            raise StopIteration
        pair =  tuple(eval(self.__f.readline()) for _ in range(2))
        end = self.__f.readline()
        if end == '':
            self.__f.close()
        return pair


def is_sorted(pair: tuple[list[int | list[int]]]) -> bool:
    smaller = False
    for a, b in zip_longest(*pair):
        match a, b:
            case int(), int():
                if b < a:
                    print(f"-> {pair=} - False, because {a=} > {b=} list")
                    return False
                elif a < b:
                    smaller = True

            case int(), None:
                print(f"-> {pair=} - {smaller}, because {a=} int {b=}")
                return smaller
                # print(f"{pair=} - False, because {a=} int {b=}")
                # return False

            case list(), None:
                print(f"-> {pair=} - False, because {a=} int {b=}")
                return False

            case None, int() | list():
                print(f"-> {pair=} - True, because {a=} int {b=}")
                return True
                # print(f"{pair=} - {smaller}, because {a=} int {b=}")
                # return smaller

            case list(), list():
                if not is_sorted((a, b)):
                    return False

            case int(), list():
                if not is_sorted(([a], b)):
                    return False

            case list(), int():
                if not is_sorted((a, [b])):
                    return False
            case _:
                continue
    return True


def solve(filename):

    sum_of_indices = 0
    for i, pair in enumerate(PairIterator(filename), start=1):
        print(f"\nPAIR {i} {pair}")
        if is_sorted(pair):
            print(f"Correct {i} {pair=}")
            sum_of_indices += i

    return sum_of_indices, 0


if __name__ == "__main__":
    part1, _ = solve(FILENAME)

    print("ANSWER",
          f"Part 1: {part1}",
          sep='\n')
