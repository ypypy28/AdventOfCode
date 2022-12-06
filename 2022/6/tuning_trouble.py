from array import array


PACKET_MARKER_SIZE = 4
MESSAGE_MARKER_SIZE = 14
buf = array('B')
start_packet = start_message = -1
with open("input.txt", 'rb') as f:
    buf.fromfile(f, PACKET_MARKER_SIZE)

    while len(set(buf)) != PACKET_MARKER_SIZE:
        buf = buf[1:]
        buf.fromfile(f, 1)
    start_packet = f.tell()

    buf.fromfile(f, MESSAGE_MARKER_SIZE-PACKET_MARKER_SIZE)

    while len(set(buf)) != MESSAGE_MARKER_SIZE:
        buf = buf[1:]
        buf.fromfile(f, 1)
    start_message = f.tell()

print("ANSWER:",
      f"PART 1: {start_packet}",
      f"PART 2: {start_message}",
      sep='\n')

