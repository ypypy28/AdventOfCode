import sys
from itertools import repeat
from os import get_terminal_size
from time import sleep


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
START_X = 500
SCREEN_WIDTH, SCREEN_HEIGHT = get_terminal_size()
SCREEN_HEIGHT -= 1
HALF_SCREEN_W = SCREEN_WIDTH >> 1
QUARTER_SCREEN_W = SCREEN_WIDTH >> 2
QUARTER_SCREEN_H = SCREEN_HEIGHT >> 2
THREE_QUARTERS_H = SCREEN_HEIGHT - QUARTER_SCREEN_H
SIGN = {'empty': '.', 'rock': '#', 'sand': 'o', 'start': '+'}


class Sand:
    DIRECTIONS = ((0, 1), (-1, 1), (1, 1))

    def __init__(self, start_coords: tuple[int, int], field: list[list[str]]):
        self._start = start_coords
        self.x = start_coords[0]
        self.y = start_coords[1]
        self.field = field
        self.field[self.y][self.x] = self
        self.end_of_part1 = False

    def __repr__(self) -> str:
        return SIGN['sand']

    def step_down(self) -> bool:
        for dx, dy in self.DIRECTIONS:
            new_x, new_y = self.x+dx, self.y+dy
            if not self.end_of_part1 and (
                0 > new_x or new_x >= len(self.field[self.y])
                or 0 > new_y or new_y >= len(self.field) - 2):  # 2 - floor part2
                self.end_of_part1 = True

            if self.field[new_y][new_x] == SIGN['empty']:
                self.field[new_y][new_x] = self
                self.field[self.y][self.x] = SIGN['empty'] if new_y != 1 else SIGN['start']
                self.x, self.y = new_x, new_y
                return True
        if self.y == 0:
            raise ValueError("End of part2")
        return False


def get_rocks(filename: str) -> list[tuple[int, int]]:
    rocks: list[tuple[int, int]] = []
    with open(FILENAME, 'r') as f:
        for line in f:
            points = [tuple(int(c) for c in p.split(',')) for p in line.split(' -> ')]
            points_iter = iter(points)
            prev = next(points_iter)
            for cur in points_iter:
                if prev[0] == cur[0]:
                    min_, max_ = ((cur[1], prev[1]), (prev[1], cur[1]))[prev[1] < cur[1]]
                    rocks.extend(tuple(zip(repeat(cur[0]), range(min_, max_+1))))
                else:
                    min_, max_ = ((cur[0], prev[0]), (prev[0], cur[0]))[prev[0] < cur[0]]
                    rocks.extend(tuple(zip(range(min_, max_+1), repeat(cur[1]))))
                prev = cur
    return rocks


def solve(filename: str) -> tuple[int, int]:
    rocks = get_rocks(filename)

    max_x = max(rocks, key=lambda r: r[0])[0]
    min_x = min(rocks, key=lambda r: r[0])[0]
    max_y = max(rocks, key=lambda r: r[1])[1]
    size_x = max_x - min_x + max_y*2
    field = [[SIGN['empty'] for _ in range(size_x)] for _ in range(max_y+1)]
    floor = [[SIGN[name] for _ in range(size_x)] for name in ('empty', 'rock')]
    field += floor

    offset_x = size_x >> 2
    sand_start_position = (START_X - min_x + offset_x, 0)
    field[0][START_X-min_x+offset_x] = SIGN['start']
    for x, y in rocks:
        field[y][x-min_x+offset_x] = SIGN['rock']

    part1_end = False
    part1 = sand_count = 0
    while True:
        new_sand = Sand(sand_start_position, field)
        sand_count += 1
        try:
            while new_sand.step_down():
                show_field(field, new_sand)
        except ValueError as e:
            break
        if not part1_end and new_sand.end_of_part1:
            part1_end = True
            part1 = sand_count-1

    show_field(field)
    return part1, sand_count


def show_field(
    field: list[list[str | Sand]],
    sand: Sand | None = None
) -> None:
    start, stop = 0, len(field)
    left, right = 0, len(field[0])
    if sand is not None:
        sleep(.05)
        right = min(right, max(sand._start[0] + HALF_SCREEN_W, sand.x + QUARTER_SCREEN_W))
        left = max(sand._start[0] - HALF_SCREEN_W, sand.x - QUARTER_SCREEN_W - HALF_SCREEN_W)
        if stop > SCREEN_HEIGHT:
            start = max(0, sand.y - THREE_QUARTERS_H)
            stop = max(SCREEN_HEIGHT, sand.y + QUARTER_SCREEN_H)

    print('\033c',  # Escape sequence to clear terminal buffer (mb only in bash)
          '\n'.join(''.join(str(field[start+y][left+x])
                            for x, _ in enumerate(line[left:right]))
                    for y, line in enumerate(field[start:stop])),
          sep='')


if __name__ == "__main__":
    part1, part2 = solve(FILENAME)
    print("ANSWER",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
