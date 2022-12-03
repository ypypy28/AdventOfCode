import string

sum_of_priotities = 0

with open("input.txt", 'r') as f:

    for line in f:
        line = line.rstrip()
        common_item_type = set(line[:len(line)//2]) & set(line[len(line)//2:])
        if not common_item_type or len(common_item_type) != 1:
            raise ValueError(f"{common_item_type=}, {line=}")
        sum_of_priotities += 1 + string.ascii_letters.index(common_item_type.pop())

print("ANSWER:",
      f"PART 1: {sum_of_priotities}",
      sep='\n')
