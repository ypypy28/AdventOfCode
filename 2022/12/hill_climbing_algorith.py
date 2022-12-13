import sys
import typing
from time import sleep


filename = sys.argv[1] if len(sys.argv) > 1 else "test_input.txt"


MOVEMENTS = {
    (0, 1): 'v',
    (0, -1): '^',
    (1, 0): '>',
    (-1, 0): '<',
}


def parse_input(
    filepath: typing.TextIO
) -> tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
    start = (0, 0)
    end = (0, 0)
    field: list[list[int]] = []
    with open(filename, 'r') as f:
        for j, line in enumerate(f):
            field.append([])
            line = line.rstrip()
            for i, ch in enumerate(line):
                if ch == 'S':
                    ch = 'a'
                    start = (i, j)
                elif ch == 'E':
                    ch  = 'z'
                    end = (i, j)
                field[-1].append(ch)
    return field, start, end


def solve():
    field_a, start, end = parse_input(filename)
    field_b = [[ch for ch in line] for line in field_a]
    field = [[ord(ch) - ord('a') for ch in line] for line in field_a]

    cur = start
    walked = [cur]
    bad_walked = dict()
    dist, steps, new_end = 999, 0, end
    while cur != end:
        sleep(.1)
        x, y = cur

        next_ = [(
            (new_x, new_y),
            ((new_y-end[1])**2 + (new_x - end[0])**2)**.5,
            (dx, dy),
        ) for dx, dy in MOVEMENTS.keys()
            if (
                (-1 < (new_x:=x+dx) < len(field[y]))
                and (-1 < (new_y:=y+dy) < len(field))
                and ((new_x, new_y) not in walked)
                and (
                    (step:=len(walked)) not in bad_walked
                    # (x, y) not in bad_walked
                    or ((new_x, new_y) not in bad_walked[step]))
                    # or ((new_x, new_y) not in bad_walked[(x, y)]))
                and ((field[new_y][new_x] - field[y][x]) in (-1, 0, 1))
            )]

        # make closes point new end if we cannot reach the end
        if not next_ and len(walked)==1:
            print("NEW END!>>>>>>>>>>>>>>>>>>>>>>>>>")
            sleep(5)
            cur = start
            end = new_end
            field_a = [[ch for ch in line] for line in field_b]
            walked = [cur]
        elif not next_:
            print(f"BAD step: {cur=} min_dist={dist} min_steps={steps} {field_a[y][x]=}")
            prev = walked.pop()
            cur_step = len(walked)
            bad_walked[cur_step] = bad_walked.get(cur_step, set())
            # bad_walked[prev] = bad_walked.get(prev, set())
            bad_walked[cur_step].add(cur)
            # bad_walked[prev].add(cur)
            cur = walked[-1]
            if field_a[cur[1]][cur[0]] in MOVEMENTS.values():
                field_a[cur[1]][cur[0]] = chr(field[cur[1]][cur[0]] + ord('a'))
        else:
            next_.sort(key=lambda x: x[1])
            field_a[y][x] = MOVEMENTS[next_[0][2]]
            if next_[0][1] < dist:
                dist = next_[0][1]
                steps = len(walked)-1
                new_end = cur
            elif next_[0][1] == dist and len(walked)-1 < steps:
                steps = len(walked)-1
                new_end = cur
            cur = next_[0][0]
            walked.append(cur)
            print(f"{walked=}")
            print(f"{bad_walked=}\nstep: {cur=} dist:{next_[0][1]} {len(walked)-1=} {field_a[y][x]=}")
            print(f"{next_=}")
        show_field(field_a)

    return steps

def show_field(field: list[list[str]]) -> None:
    print(*(''.join(line) for line in field),
          sep='\n')


if __name__ == "__main__":
    part1 = solve()
    print("ANSWER:",
          f"Part 1: {part1}",
          sep='\n')
