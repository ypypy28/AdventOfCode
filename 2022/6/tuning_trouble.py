from array import array
from collections import deque


PACKET_MARKER_SIZE = 4
MESSAGE_MARKER_SIZE = 14
buf_packet = deque(maxlen=PACKET_MARKER_SIZE)
buf_message = deque(maxlen=MESSAGE_MARKER_SIZE)
start_packet = start_message = -1
with open("input.txt", 'r') as f:
    stream = f.read(PACKET_MARKER_SIZE)
    buf_packet.extend(stream)
    buf_message.extend(stream)

    while len(set(buf_packet)) != PACKET_MARKER_SIZE:
        stream = f.read(1)
        buf_packet.append(stream)
        buf_message.append(stream)
    start_packet = f.tell()

    while len(set(buf_message)) != MESSAGE_MARKER_SIZE:
        buf_message.append(f.read(1))
    start_message = f.tell()

print("ANSWER:",
      f"PART 1: {start_packet}",
      f"PART 2: {start_message}",
      sep='\n')

