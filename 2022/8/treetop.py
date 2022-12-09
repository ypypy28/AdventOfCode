import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

buf = []
with open(filename, 'r') as f:
    for line in f:
        buf.append([int(ch) for ch in line.rstrip()])

all_edges = len(buf)*2 + (len(buf[0])-2)*2
max_score = 0
visible = 0
for x in range(1, len(buf[1])-1):
    for y in range(1, len(buf)-1):
        size = buf[y][x]
        up_visible = all(size > buf[j][x] for j in range(0, y))
        right_visible = all(size > buf[y][i] for i in range(x+1, len(buf[y])))
        bottom_visible = all(size > buf[j][x] for j in range(y+1, len(buf)))
        left_visible = all(size > buf[y][i] for i in range(x))
        if any((up_visible, right_visible, bottom_visible, left_visible)):
            visible += 1

            # PART 2 stuff
            upper_visible_trees = 0
            for j in range(y-1, -1, -1):
                if buf[j][x] <= buf[y][x]:
                    upper_visible_trees += 1
                if buf[j][x] >= buf[y][x]:
                    break

            right_visible_trees = 0
            for i in range(x+1, len(buf[y])):
                if buf[y][i] <= buf[y][x]:
                    right_visible_trees += 1
                if buf[y][i] >= buf[y][x]:
                    break

            bottom_visible_trees = 0
            for j in range(y+1, len(buf)):
                if buf[j][x] <= buf[y][x]:
                    bottom_visible_trees += 1
                if buf[j][x] >= buf[y][x]:
                    break

            left_visible_trees = 0
            for i in range(x-1, -1, -1):
                if buf[y][i] <= buf[y][x]:
                    left_visible_trees += 1
                if buf[y][i] >= buf[y][x]:
                    break


            score = (left_visible_trees
                     * right_visible_trees
                     * bottom_visible_trees
                     * upper_visible_trees)

            if score > max_score:
                max_score = score


print("ASNWER:",
      f"Part 1: {visible + all_edges}",
      f"Part 2: {max_score}",
      sep='\n')
