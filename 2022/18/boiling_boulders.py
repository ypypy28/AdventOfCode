import sys
from collections import namedtuple


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
Cube = namedtuple("Cube", "x y z")


def manhattan_distance(cube1, cube2):
    return sum(abs(cube1[c] - cube2[c])
               for c in range(len(cube1)))


def solve(filename: str):

    with open(filename, 'r') as f:
        cubes = []
        for line in f:
            x, y, z = (int(n) for n in line.split(','))
            cube = Cube(x, y, z)
            cubes.append(cube)

        touching_sides = 0
        for i, _ in enumerate(cubes):
            for j in range(i+1, len((cubes))):
                if manhattan_distance(cubes[i], cubes[j]) == 1:
                    touching_sides += 2

        part1 = len(cubes)*6 - touching_sides

    return part1, 0


if __name__ == "__main__":
    part1, part2 = solve(FILENAME)
    print("\nANSWER",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
