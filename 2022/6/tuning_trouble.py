from collections import deque


MARKER_SIZE = 4
MESSAGE_START_MARKER_SIZE = 14
buf_packet = deque(maxlen=MARKER_SIZE)
buf_message = deque(maxlen=MESSAGE_START_MARKER_SIZE)
cursor = cursor_packet = cursor_message = 0
with open("input.txt", 'r') as f:
    stream = f.read(MARKER_SIZE)
    buf_packet.extend(stream)
    buf_message.extend(stream)
    cursor += MARKER_SIZE

    while len(set(buf_packet)) != MARKER_SIZE:
        stream = f.read(1)
        buf_packet.append(stream)
        buf_message.append(stream)
        cursor += 1

    cursor_packet = cursor

    while len(set(buf_message)) != MESSAGE_START_MARKER_SIZE:
        buf_message.append(f.read(1))
        cursor += 1
    cursor_message = cursor

print("ANSWER:",
      f"PART 1: {cursor_packet}",
      f"PART 2: {cursor_message}",
      sep='\n')

