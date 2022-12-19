import sys
from collections import namedtuple
from functools import cache


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
Cube = namedtuple("Cube", "x y z")


@cache
def manhattan_distance(cube1, cube2):
    return sum(abs(cube1[c] - cube2[c])
               for c in range(len(cube1)))


def get_cubes_of_air(cubes: list[Cube]) -> list[Cube]:
    cubes_s = set(cubes)
    cubes_of_air = set()
    for cube in cubes:
        neighbors = (
            Cube(cube.x+1, cube.y, cube.z),
            Cube(cube.x-1, cube.y, cube.z),
            Cube(cube.x, cube.y+1, cube.z),
            Cube(cube.x, cube.y-1, cube.z),
            Cube(cube.x, cube.y, cube.z+1),
            Cube(cube.x, cube.y, cube.z-1),
        )

        for cube_n in neighbors:
            if cube_n not in cubes_s:
                cubes_of_air.add(cube_n)
    return list(cubes_of_air)


def solve(filename: str) -> tuple[int, int]:
    with open(filename, 'r') as f:
        cubes_of_lava = []
        for line in f:
            x, y, z = (int(n) for n in line.split(','))
            cube = Cube(x, y, z)
            cubes_of_lava.append(cube)

        touching_sides = 0
        for i, _ in enumerate(cubes_of_lava):
            for j in range(i+1, len(cubes_of_lava)):
                if manhattan_distance(cubes_of_lava[i], cubes_of_lava[j]) == 1:
                    touching_sides += 2

        part1 = len(cubes_of_lava)*6 - touching_sides

        cubes_of_air = get_cubes_of_air(cubes_of_lava)
        cubes_of_air_inside = []

        for i, aircube in enumerate(cubes_of_air):
            touches = 0
            for j in range(i+1, len(cubes_of_air)):
                if manhattan_distance(aircube, cubes_of_air[j]) == 1:
                    touches += 1

            if touches == 6:
                cubes_of_air_inside.append(aircube)
                continue

            for lavacube in cubes_of_lava:
                if manhattan_distance(aircube, lavacube) == 1:
                    touches += 1
            if touches == 6:
                cubes_of_air_inside.append(aircube)


        touching_sides_inner_aircubes = 0
        for i, _ in enumerate(cubes_of_air_inside):
            for j in range(i+1, len(cubes_of_air_inside)):
                # print(f"{manhattan_distance(cubes_of_air_inside[i], cubes_of_air_inside[j])=}")
                if manhattan_distance(cubes_of_air_inside[i],
                                      cubes_of_air_inside[j]) == 1:
                    touching_sides_inner_aircubes += 2

        print(f"{len(cubes_of_lava)=} {len(cubes_of_air)=} {len(cubes_of_air_inside)=} {touching_sides_inner_aircubes=}")

        part2 = (len(cubes_of_lava)*6 - touching_sides
                 - (len(cubes_of_air_inside)*6 - touching_sides_inner_aircubes))

    return part1, part2


if __name__ == "__main__":
    part1, part2 = solve(FILENAME)
    print("\nANSWER",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
