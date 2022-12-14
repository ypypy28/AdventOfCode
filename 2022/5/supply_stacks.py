from typing import TextIO


def count_stacks(header: list[str]) -> tuple[int, int]:
    return int(header[-1].rstrip().split()[-1]), len(header)-1


def get_default_stacks(header: list[str]) -> list[list[str]]:
    len_stacks, height = count_stacks(header)
    stacks = [None for _ in range(len_stacks)]
    for i in range(len(header)-1):
        for j in range(1, len(header[i]), 4):
            if header[i][j] != ' ':
                stack_i = (j-1)//4
                if stacks[stack_i] is None:
                    stacks[stack_i] = [None for _ in range(height)]
                stacks[stack_i][height-1] = header[i][j]
        height -= 1

    return stacks


def rearrangements_part1(
    cargos: int, from_: int, to_: int,
    stacks: list[list[str]]
) -> None:
    for _ in range(cargos):
        cargo = stacks[from_].pop()
        stacks[to_].append(cargo)


def rearrangements_part2(
    cargos: int, from_: int, to_: int,
    stacks: list[list[str]]
) -> None:
    stacks[to_] += stacks[from_][-cargos:]
    stacks[from_] = stacks[from_][:-cargos]


def solve_task(f: TextIO) -> tuple[str, str]:
    header = list(iter(f.readline, '\n'))
    stacks = get_default_stacks(header)
    stacks2 = [[cargo for cargo in st] for st in stacks]

    # execute rearrangements
    for line in f:
        _, cargos_str, _, from_str, _, to_str = line.split()
        cargos = int(cargos_str)
        from_, to_ = int(from_str)-1, int(to_str)-1
        rearrangements_part1(cargos, from_, to_, stacks)
        rearrangements_part2(cargos, from_, to_, stacks2)

    return tuple(''.join(st[-1] for st in stks) for stks in (stacks, stacks2))


if __name__ == "__main__":
    with open("input.txt", 'r') as f:
        part1, part2 = solve_task(f)


    print("ANSWER:",
        f"PART 1: {part1}",
        f"PART 2: {part2}",
        sep='\n')
