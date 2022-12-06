from collections import deque


MARKER_SIZE = 4
buf = deque(maxlen=MARKER_SIZE)
cursor = 0
with open("input.txt", 'r') as f:
    buf.extend(f.read(MARKER_SIZE))
    cursor += MARKER_SIZE

    while len(set(buf)) != MARKER_SIZE:
        buf.append(f.read(1))
        cursor += 1

print("ANSWER:",
      f"PART 1: {cursor}",
      f"PART 2:",
      sep='\n')

