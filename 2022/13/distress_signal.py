import sys
import typing

FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
DIVIDER_PACKETS = ([[2]], [[6]])
Packet = typing.Union[list[int], list['Packet']]


class PairIterator:
    def __init__(self, filename: str):
        self.__f = open(filename, 'r')

    def __iter__(self):
        return self

    def __next__(self) -> tuple[Packet]:
        if self.__f.closed:
            raise StopIteration
        pair: tuple[Packet] = tuple(eval(self.__f.readline()) for _ in range(2))
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


def reordered(pairs: list[Packet]) -> list[Packet]:
    res = []
    while pairs:
        min_ = pairs[0]
        for packet in pairs[1:]:
            if is_sorted((packet, min_)):
                min_ = packet
        res.append(min_)
        pairs.remove(min_)
    return res


def solve(filename):
    sum_of_indices = 0
    for i, pair in enumerate(PairIterator(filename), start=1):
        if is_sorted(pair):
            sum_of_indices += i

    # Part 2
    pairs = [*DIVIDER_PACKETS] + [p for pair in PairIterator(filename) for p in pair]
    pairs = reordered(pairs)
    d1, d2 = (pairs.index(divider)+1 for divider in DIVIDER_PACKETS)
    part2 = d1 * d2

    return sum_of_indices, part2


if __name__ == "__main__":
    part1, part2 = solve(FILENAME)

    print("ANSWER",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
