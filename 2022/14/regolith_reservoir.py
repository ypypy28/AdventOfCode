import sys
from itertools import repeat
from time import sleep


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "test_input.txt"
SIGN = {'empty': '.', 'rock': '#', 'sand': 'o', 'start': '+'}


class Sand:
    DIRECTIONS = ((0, 1), (-1, 1), (1, 1))

    def __init__(self, start_coords, field):
        self.x = start_coords[0]
        self.y = start_coords[1]+1
        self.field = field
        if self.field[self.y][self.y] != SIGN['empty']:
            raise NotImplementedError(("collision detected: trying to put Sand on"
                                       f" ({self.x}, {(self.y)}) wich is not empty"
                                       f" ({field[self.y][self.x]})"))
        self.field[self.y][self.x] = self

    def __repr__(self) -> str:
        return SIGN['sand']

    def step_down(self) -> bool:
        for dx, dy in self.DIRECTIONS:
            new_x, new_y = self.x+dx, self.y+dy
            if (0 > new_x or new_x >= len(self.field[self.y])
                or 0 > new_y or new_y >= len(self.field)):
                raise ValueError("Sand is getting out of the cave")

            if self.field[new_y][new_x] == SIGN['empty']:
                self.field[new_y][new_x], self.field[self.y][self.x] = self, SIGN['empty']
                self.x, self.y = new_x, new_y
                return True
        return False


def get_rocks(filename: str) -> list[tuple[int, int]]:
    rocks: list[tuple[int, int]] = []
    paths = 0
    with open(FILENAME, 'r') as f:
        for line in f:
            points = [tuple(int(c) for c in p.split(',')) for p in line.split(' -> ')]
            paths += 1
            points_iter = iter(points)
            prev = next(points_iter)
            for cur in points_iter:
                if prev[0] == cur[0]:
                    min_, max_ = ((cur[1], prev[1]), (prev[1], cur[1]))[prev[1] < cur[1]]
                    rocks.extend((zip(repeat(cur[0]), range(min_, max_+1))))
                else:
                    min_, max_ = ((cur[0], prev[0]), (prev[0], cur[0]))[prev[1] < cur[1]]
                    rocks.extend((zip(range(min_, max_+1), repeat(cur[1]))))
                prev = cur
    return rocks


def solve(filename: str) -> tuple[int, int]:
    rocks = get_rocks(filename)

    max_x = max(rocks, key=lambda r: r[0])[0]
    min_x = min(rocks, key=lambda r: r[0])[0]
    offset_x = max_x - min_x + 3
    max_y = max(rocks, key=lambda r: r[1])[1]
    field = [['.' for _ in range(offset_x)] for _ in range(max_y+1)]

    sand_start_position = (501-min_x, 0)
    field[0][501-min_x] = SIGN['start']
    for x, y in rocks:
        field[y][x-min_x+1] = SIGN['rock']

    sand_count = 0
    while True:
        new_sand = Sand(sand_start_position, field)
        show_field(field)
        try:
            while new_sand.step_down():
                show_field(field, new_sand)
        except ValueError as e:
            print("The end:", e)
            break
        sand_count += 1
        sleep(1)

    return sand_count, None


def show_field(field: list[list[str | Sand]], sand: Sand = None) -> None:
    start, stop = 0, len(field)
    if stop > 40 and sand:
        start, stop = max(0, sand.y-20), min(stop, sand.y+20)

    print('\033[2J\033[H',
          '\n'.join(''.join(str(field[start+y][x])
                            for x, _ in enumerate(line))
                    for y, line in enumerate(field[start:stop])),
          sep='')
    sleep(.05)


if __name__ == "__main__":
    part1, part2 = solve(FILENAME)
    print("ANSWER",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
