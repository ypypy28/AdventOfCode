import sys
import typing
from itertools import zip_longest


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "test_input.txt"


def parse_data(file: typing.TextIO) -> list[tuple[list[int | list[int]]]]:
    vals = []
    while True:
        pair = tuple(eval(file.readline()) for _ in range(2))
        vals.append(pair)
        end = file.readline()
        if end == '':
            break
    return vals


def is_sorted(pair: tuple[list[int | list[int]]]) -> bool:
    smaller = False
    for a, b in zip_longest(*pair):
        match a, b:
            case int(), int():
                if b < a:
                    print(f"{pair=} - False, because {a=} > {b=} list")
                    return False
                elif a < b:
                    smaller = True

            case int() | list(), None:
                print(f"{pair=} - {smaller}, because {a=} int {b=}")
                return smaller
                # print(f"{pair=} - False, because {a=} int {b=}")
                # return False

            case None, int() | list():
                print(f"{pair=} - True, because {a=} int {b=}")
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

    with open(filename, 'r') as f:
        packets_pairs = parse_data(f)

    sum_of_indices = 0
    for i, pair in enumerate(packets_pairs, start=1):
        print(f"PAIR {i} {pair}")
        if is_sorted(pair):
            print(f" Correct {i} {pair=}")
            sum_of_indices += i

    return sum_of_indices, 0


if __name__ == "__main__":
    part1, _ = solve(FILENAME)

    print("ANSWER",
          f"Part 1: {part1}",
          sep='\n')
