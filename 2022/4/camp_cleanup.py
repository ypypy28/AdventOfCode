one_fully_contains_another = overlap = 0
with open("input.txt", 'r') as f:
    for line in f:
        edges = ((int(n) for n in elf.split('-'))
                 for elf in line.rstrip().split(','))
        assign1, assign2 = tuple(range(l, r+1) for l, r in edges)
        common_assignments = set(assign1) & set(assign2)

        if common_assignments:
            overlap += 1

        if len(common_assignments) == min(len(assign1), len(assign2)):
            one_fully_contains_another += 1

print("ANSWER:",
      f"PART 1: {one_fully_contains_another}",
      f"PART 2: {overlap}",
      sep='\n')
