import sys
from collections import namedtuple, deque


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
Cube = namedtuple("Cube", "x y z")


def get_neighbors(cube: Cube) -> tuple[Cube, Cube, Cube, Cube, Cube, Cube]:
    return (
            Cube(cube.x+1, cube.y, cube.z),
            Cube(cube.x-1, cube.y, cube.z),
            Cube(cube.x, cube.y+1, cube.z),
            Cube(cube.x, cube.y-1, cube.z),
            Cube(cube.x, cube.y, cube.z+1),
            Cube(cube.x, cube.y, cube.z-1),
    )


def get_outside(lava: set[Cube],
                maxx: int,
                maxy: int,
                maxz: int,
                minx: int,
                miny: int,
                minz: int,
                ) -> set[Cube]:
    maxx, maxy, maxz = (c + 2 for c in (maxx, maxy, maxz))
    minx, miny, minz = (c - 2 for c in (minx, miny, minz))

    start = Cube(minx, miny, minz)
    outside = set((start,))
    queue = deque(outside)

    while queue:
        neighbors = [cube for cube in get_neighbors(queue.popleft())
                     if (
                         cube not in lava
                         and cube not in outside
                         and minx <= cube.x <= maxx
                         and miny <= cube.y <= maxy
                         and minz <= cube.z <= maxz
                     )]
        outside.update(neighbors)
        queue.extend(neighbors)
    return outside


def solve(filename: str) -> tuple[int, int]:
    maxx = maxy = maxz = minx = miny = minz = 1
    with open(filename, 'r') as f:
        cubes_of_lava = set()
        for line in f:
            x, y, z = (int(n) for n in line.split(','))
            if x < minx:
                minx = x
            if y < miny:
                miny = y
            if z < minz:
                minz = z
            if z > maxz:
                maxz = z
            if y > maxy:
                maxy = y
            if x > maxx:
                maxx = x
            cubes_of_lava.add(Cube(x, y, z))

    touching_sides = 0
    cubes_of_air_touching_lava = set()
    for cube in cubes_of_lava:
        aircubes = [n for n in get_neighbors(cube) if n not in cubes_of_lava]
        cubes_of_air_touching_lava.update(aircubes)
        touching_sides += 6 - len(aircubes)

    part1 = len(cubes_of_lava)*6 - touching_sides

    air_outside = get_outside(cubes_of_lava, maxx, maxy, maxz, minx, miny, minz)
    cubes_of_air_touching_inside = {cube
                                    for cube in cubes_of_air_touching_lava
                                    if cube not in air_outside}

    touching_lava_from_inside = 0
    for aircube in cubes_of_air_touching_inside:
        touching_lava_from_inside += sum(n in cubes_of_lava
                                         for n in get_neighbors(aircube))

    part2 = part1 - touching_lava_from_inside
    return part1, part2


if __name__ == "__main__":
    part1, part2 = solve(FILENAME)
    print("\nANSWER",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
