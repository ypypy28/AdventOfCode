import sys
from collections import namedtuple


FILENAME = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
Cube = namedtuple("Cube", "x y z")


def get_neighbors(cube: Cube) -> tuple[Cube]:

    return (
            Cube(cube.x+1, cube.y, cube.z),
            Cube(cube.x-1, cube.y, cube.z),
            Cube(cube.x, cube.y+1, cube.z),
            Cube(cube.x, cube.y-1, cube.z),
            Cube(cube.x, cube.y, cube.z+1),
            Cube(cube.x, cube.y, cube.z-1),
        )


def get_cubes_of_air(cubes: set[Cube]) -> list[Cube]:
    cubes_of_air = set()
    for cube in cubes:
        neighbors = get_neighbors(cube)

        for cube_n in neighbors:
            if cube_n not in cubes:
                cubes_of_air.add(cube_n)
    return cubes_of_air


def is_inside(cube: Cube, lava: set[Cube], maxx, maxy, maxz, minx, miny, minz):

    for direction, end in (
        (Cube(1, 0, 0), Cube(max(maxx, cube.x), cube.y, cube.z)),
        (Cube(-1, 0, 0), Cube(min(minx, cube.x), cube.y, cube.z)),
        (Cube(0, 1, 0), Cube(cube.x, max(maxy, cube.y), cube.z)),
        (Cube(0, -1, 0), Cube(cube.x, min(miny, cube.y), cube.z)),
        (Cube(0, 0, 1), Cube(cube.x, cube.y, max(maxz, cube.z))),
        (Cube(0, 0, -1), Cube(cube.x, cube.y, min(minz, cube.z))),
    ):
        ray = cube
        while ray != end:
            ray = Cube(ray.x + direction.x, ray.y + direction.y, ray.z + direction.z)
            if ray in lava:
                break
        else:
            return False
        if cube == Cube(14, 7, 7):
            print(f"!! cube 14.7.7 inside, {ray=} {end=} {ray in lava=}")



    return True


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
            cube = Cube(x, y, z)
            cubes_of_lava.add(cube)

    touching_sides = 0
    for cube in cubes_of_lava:
        touching_sides += sum(n in cubes_of_lava for n in get_neighbors(cube))

    part1 = len(cubes_of_lava)*6 - touching_sides

    cubes_of_air = get_cubes_of_air(cubes_of_lava)

    cubes_of_air_inside = {cube
                           for cube in cubes_of_air
                           if is_inside(cube, cubes_of_lava,
                                        maxx, maxy, maxz, minx, miny, minz)}

    cubes_of_air_outside = {cube
                            for cube in cubes_of_air
                            if not is_inside(cube, cubes_of_lava,
                                             maxx, maxy, maxz, minx, miny, minz)}

    print(f"{len(cubes_of_air_outside)}")

    touching_lava_from_outside = 0
    for aircube in cubes_of_air_outside:
        touching_lava_from_outside += sum(n in cubes_of_lava for n in get_neighbors(aircube))
    print(f"{touching_lava_from_outside=}")

    touching_sides_inner_aircubes = 0
    touching_lava_from_inside = 0
    bad = 0
    for aircube in cubes_of_air_inside:
        neighbors = get_neighbors(aircube)
        touching_sides_inner_aircubes += sum(n in cubes_of_air_inside
                                             for n in neighbors)
        touching_lava_from_inside += sum(n in cubes_of_lava
                                         for n in neighbors)
        touching_aircubes = sum(n in cubes_of_air_inside
                                for n in neighbors)
        touching_lava = sum(n in cubes_of_lava
                            for n in neighbors)
        if touching_aircubes + touching_lava != 6:
            bad +=1
            bad_neighbors = [n for n in neighbors
                             if n not in cubes_of_lava and n not in cubes_of_air_inside]
            print(f"{touching_aircubes} + {touching_lava} {aircube=}",
                  f"{bad_neighbors=}", sep='\n', end='\n\n')

    print(bad)
    # print(f"{len(cubes_of_lava)=} {len(cubes_of_air)=} {len(cubes_of_air_inside)=} {touching_sides_inner_aircubes=}")

    print(touching_lava_from_inside + touching_sides_inner_aircubes, len(cubes_of_air_inside)*6)

    part2 = len(cubes_of_lava)*6 - touching_sides - touching_lava_from_inside
             # - (len(cubes_of_air_inside)*6 - touching_sides_inner_aircubes))

    return part1, part2


if __name__ == "__main__":
    part1, part2 = solve(FILENAME)
    print("\nANSWER",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
