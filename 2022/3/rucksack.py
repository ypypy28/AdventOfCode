import string

sum_of_group_priorities = sum_of_priorities = 0
group_counter = 0
group_type = set()

with open("input.txt", 'r') as f:
    for line in f:
        line = line.rstrip()
        common_item_type = set(line[:len(line)//2]) & set(line[len(line)//2:])
        if not common_item_type or len(common_item_type) != 1:
            raise ValueError(f"{common_item_type=}, {line=}")
        sum_of_priorities += 1 + string.ascii_letters.index(common_item_type.pop())

        if group_counter == 0:
            group_type = set(line)
        else:
            group_type &= set(line)
        group_counter += 1

        if group_counter == 3:
            if not group_type or len(group_type) != 1:
                raise ValueError(f"{group_type=}, {line=}")
            sum_of_group_priorities += 1 + string.ascii_letters.index(group_type.pop())
            group_counter = 0

print("ANSWER:",
      f"PART 1: {sum_of_priorities}",
      f"PART 2: {sum_of_group_priorities}",
      sep='\n')
