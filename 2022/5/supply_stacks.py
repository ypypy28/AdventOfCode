from typing.io import TextIO


def read_header(fd: TextIO) -> list[str]:
    header = []
    while (line:=f.readline()) != '\n':
        header.append(line.rstrip('\n'))
    return header


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


inputfile = "input.txt"
with open(inputfile, 'r') as f:
    header = read_header(f)
    stacks = get_default_stacks(header)
    stacks2 = [[cargo for cargo in st] for st in stacks]

    # execute rearrangements
    for line in f:
        _, cargos, _, from_, _, to_ = line.split()
        cargos = int(cargos)
        from_, to_ = (int(n)-1 for n in (from_, to_))
        # For Part 1
        for _ in range(cargos):
            cargo = stacks[from_].pop()
            stacks[to_].append(cargo)

        # For Part 2
        stacks2[to_] += stacks2[from_][-cargos:]
        stacks2[from_] = stacks2[from_][:-cargos]


print("ANSWER:",
      f"PART 1: {''.join(st[-1] for st in stacks)}",
      f"PART 2: {''.join(st[-1] for st in stacks2)}",
      sep='\n')
