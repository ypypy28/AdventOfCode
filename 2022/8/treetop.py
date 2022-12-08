import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

buf = []
with open(filename, 'r') as f:
    for line in f:
        buf.append([int(ch) for ch in line.rstrip()])

all_edges = len(buf)*2 + (len(buf[0])-2)*2
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

print("ASNWER:",
      f"Part 1: {visible + all_edges}",
      f"Part 2: ",
      sep='\n')
