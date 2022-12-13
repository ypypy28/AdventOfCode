import sys
import typing
from collections import namedtuple, deque
from functools import cache
from time import sleep


filename = sys.argv[1] if len(sys.argv) > 1 else "test_input.txt"


MOVEMENTS = {
    (0, 1): 'v',
    (0, -1): '^',
    (1, 0): '>',
    (-1, 0): '<',
}
Variant = namedtuple("Variant", "distance path")


def path_to_movements(path: tuple[tuple[int, int]]
                      ) -> typing.Generator[str, None, None]:
    prev = path[0]
    for i in range(1, len(path)):
        cur = path[i]
        move = cur[0] - prev[0], cur[1] - prev[1]
        yield MOVEMENTS[move]
        prev = cur

    yield 'E'

@cache
def calculate_distance(from_: tuple[int, int], to_: tuple[int, int]) -> float:
    return ((from_[0] - to_[0])**2 + (from_[1] - to_[1])**2)**.5


def parse_input(
    filepath: typing.TextIO
) -> tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
    start = (0, 0)
    end = (0, 0)
    field: list[list[int]] = []
    with open(filename, 'r') as f:
        for j, line in enumerate(f):
            field.append([])
            line = line.rstrip()
            for i, ch in enumerate(line):
                if ch == 'S':
                    ch = 'a'
                    start = (i, j)
                elif ch == 'E':
                    ch  = 'z'
                    end = (i, j)
                field[-1].append(ch)
    return field, start, end


def solve():
    field_a, start, end = parse_input(filename)
    field = [[ord(ch) - ord('a') for ch in line] for line in field_a]

    walked = set()
    S = Variant(calculate_distance(start, end), (start,))
    closest_variant = S
    queue = deque((S,))
    while queue:
        cur = queue.popleft()
        if cur.distance == 0:
            closest_variant = cur
            break

        x, y = cur.path[-1]
        walked.add((x, y))

        next_ = [Variant(
            calculate_distance(new_coords, end),
            tuple((*cur.path, new_coords)),
        ) for dx, dy in MOVEMENTS.keys()
            if (
                (-1 < (new_x:=x+dx) < len(field[y]))
                and (-1 < (new_y:=y+dy) < len(field))
                and ((new_coords:=(new_x, new_y)) not in walked)
                and ((field[new_y][new_x] - field[y][x]) in (-1, 0, 1))
            )]

        # make closes point new end if we cannot reach the end
        if not next_:
            print(f"step={len(cur.path)-1}", end='\r')
            if cur.distance < closest_variant.distance:
                closest_variant = cur
                show_field(field_a, cur.path)
        else:
            # next_.sort(key=lambda v: v.distance)
            queue.extend(next_)


    show_field(field_a, cur.path)
    return len(closest_variant.path) - 1


def show_field(field: list[list[str]], path: tuple[tuple[int, int]]) -> None:
    movements = path_to_movements(path)
    pd = dict(zip(path, movements))
    res = '\n'.join(''.join((ch if (coords:=(x, y)) not in pd else pd[coords])
                           for x, ch in enumerate(line))
                    for y, line in enumerate(field))
    print(f"\n{res}", end='\n')


if __name__ == "__main__":
    part1 = solve()
    print("ANSWER:",
          f"Part 1: {part1}",
          sep='\n')
