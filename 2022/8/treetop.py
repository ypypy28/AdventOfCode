import sys
from collections import namedtuple


Tree = namedtuple("Tree", "x y size")
MAX_TREE_HEIGHT = 9


def check_row_left(
    buffer: list[list[int]],
    line_i: int,
    left_edge: Tree,
    visible_inside: set[Tree],
) -> None:
    max_height = left_edge.size
    for x in range(1, len(buffer[-1])-1):
        if max_height == MAX_TREE_HEIGHT:
            break
        size = buffer[-1][x]
        if size > max_height:
            visible_inside.add(Tree(x, line_i, size))
            print(f"visible from left: ({x}, {line_i}) {size}")
            max_height = size


def check_row_right(
    buffer: list[list[int]],
    line_i: int,
    right_edge: Tree,
    visible_inside: set[Tree],
) -> None:
    max_height = right_edge.size
    for x in range(len(buffer[-1])-1, 0, -1):
        if max_height == MAX_TREE_HEIGHT:
            break
        print("CHECK right:", x)
        size = buffer[-1][x]
        if size > max_height:
            print(f"visible from right: ({x}, {line_i}) {size}")
            visible_inside.add(Tree(x, line_i, size))
            max_height = size


def check_top(
    buffer: list[list[int]],
    line_i: int,
    top: list[Tree],
    visible_inside: set[Tree],
) -> None:
    for x in range(1, len(buffer[-1])-1):
        print("CHECK top:", x)
        size = buffer[-1][x]
        if size > top[x].size:
            visible = True
            for upper in (buffer[j][x] for j in range(len(buffer)-2, -1, -1)):
                if upper > size:
                    visible = False
                    break
            if visible:
                print(f"visible from top: ({x}, {line_i}) {size}")
                visible_inside.add(Tree(x, line_i, size))


def check_bottom(
    buffer: list[list[int]],
    line_i: int,
    bottom: list[Tree],
    visible_inside: set[Tree],
) -> None:
    if any(bottom):
        max_x = min(len(buffer[-1]), len(bottom)) - 1
        for x in range(1, max_x):
            if bottom[x] is not None:
                max_height = bottom[x].size
                for j in range(len(buffer)-1, -1, -1):
                    print(f"CHECK bottom ({x}, {line_i-len(buffer)+1+j}) {buffer[j][x]=} {line_i=} {j=} {buffer=}")
                    if max_height == MAX_TREE_HEIGHT:
                        break
                    if buffer[j][x] > max_height:
                        print(f"visible from bottom: ({x}, {line_i-len(buffer)+1+j}) {buffer[j][x]}")
                        visible_inside.add(Tree(x, line_i-len(buffer)+1+j, buffer[j][x]))
                        max_height = buffer[j][x]


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    top, left, right, bottom = [], [], [], []
    all_edges = set()
    inner_visible = set()
    y = 0
    with open(filename, 'r') as f:
        top = [Tree(x, y, int(size))
            for x, size in enumerate(f.readline().rstrip())]
        all_edges.update(top)

        buf = [[int(ch) for ch in f.readline().rstrip()]]
        len_prev = len(buf[-1])
        y += 1

        for line in f:
            line = line.rstrip()
            if bottom and len(line) - len(bottom) > 0:
                bottom += [Tree(x, y, int(size))
                        for x, size in enumerate(line[len(bottom):])]
                all_edges.update(bottom)
            left.append(Tree(0, y, buf[-1][0]))
            right.append(Tree(len(buf[-1])-1, y, buf[-1][-1]))
            all_edges.add(left[-1])
            all_edges.add(right[-1])
            print(f"{y=}")
            # print(f"{top=}")
            # print(f"{buf=}")
            # print(f"{line=}")
            # print(f"{bottom=}")
            print("-"*10)

            check_row_left(buf, y, left[-1], inner_visible)
            check_row_right(buf, y, right[-1], inner_visible)
            check_top(buf, y, top, inner_visible)
            check_bottom(buf, y, bottom, inner_visible)

            diff_len = len_prev - len(top)
            if diff_len > 0:
                top += [Tree(x, y, int(size))
                        for x, size in enumerate(buf[-1][len(top):])]
                all_edges.update(top)
            elif diff_len < 0:
                top = top[:len_prev]
                bottom = ([None for _ in range(diff_len)] +
                        [Tree(x, y, buf[-1][x])
                        for x in range(diff_len, len_prev)])
                all_edges.update(bottom)

            buf.append([int(ch) for ch in line])
            len_prev = len(line)
            y += 1

    bottom[:len(buf[-1])] = [Tree(x, y, int(size)) for x, size in enumerate(buf[-1])]
    all_edges.update(bottom)
    buf.pop()
    check_bottom(buf, y-1, bottom, inner_visible)

    print(f"{len(all_edges)=}", f"{len(inner_visible)=}",
          f"{inner_visible=}",
          f"{top=}",
          f"{right=}",
          f"{bottom=}",
          f"{left=}",
          f"{all_edges=}",
          sep='\n')

    print("ANSWER:",
        f"Part 1: {len(all_edges) + len(inner_visible)}",
        f"Part 2: ",
        sep='\n')


if __name__ == "__main__":
    main()
