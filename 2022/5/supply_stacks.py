import sys


def count_stacks(filename: str) -> tuple[int, int]:
    prev = ''
    height = -1
    with open(filename, 'r') as f:
        while (line:= f.readline()) != '\n':
            height += 1
            prev = line
    return int(prev.rstrip().split()[-1]), height


inputfile = "input.txt"
len_stacks, max_height = count_stacks(inputfile)
stacks = [None for _ in range(len_stacks)]

with open("input.txt", 'r') as f:
    # interprete the default cargo stacks
    height = max_height
    while (line:= f.readline()) != '\n':
        line = line.rstrip('\n')
        if '[' in line:
            for i in range(1, len(line), 4):
                if line[i] != ' ':
                    stack_i = (i-1)//4
                    if stacks[stack_i] is None:
                        stacks[stack_i] = ['' for _ in range(height)]
                    stacks[stack_i][height-1] = line[i]
        height -=1

    # print('BEFORE:', *enumerate(stacks), sep='\n')

    # execute rearrangements
    for line in f:
        _, repeat, _, from_, _, to_ = line.split()
        for _ in range(int(repeat)):
            cargo = stacks[int(from_)-1].pop()
            stacks[int(to_)-1].append(cargo)



# print('AFTER:', *enumerate(stacks), sep='\n')

print("ANSWER:",
      f"PART 1: {''.join(st[-1] for st in stacks)}",
      f"PART 2: {None}",
      sep='\n')

