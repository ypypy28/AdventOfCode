import sys


filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

DIRECTIONS = {
    "R": (1, 0),
    "D": (0, -1),
    "L": (-1, 0),
    "U": (0, 1),
    "RU": (1, 1),
    "RD": (1, -1),
    "LU": (-1, 1),
    "LD": (-1, -1),
}


class Knot:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.history = [(x, y)]
        self.tail = None

    def move(self, direction: str) -> None:
        dx, dy = DIRECTIONS[direction]
        self.x += dx
        self.y += dy
        self.history.append((self.x, self.y))
        if self.tail is not None:
            self.tail.move(self.x, self.y)

    def add_tail(self, new_tail) -> None:
        if not self.tail:
            self.tail = new_tail
            return
        old_tail = self.tail
        while old_tail.tail is not None:
            old_tail = old_tail.tail
        old_tail.add_tail(new_tail)

    def __getitem__(self, i: int):
        knot = self
        for _ in range(i):
            knot = knot.tail
            if knot is None:
                raise IndexError
        return knot


class Tail(Knot):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)

    def move(self, head_x: int, head_y: int) -> None:
        dx, dy = head_x - self.x, head_y - self.y
        if abs(dx) < 2 and abs(dy) < 2:
            return

        direction: str = (
            (('L', 'R')[dx > 0], '')[dx == 0]
            + (('D', 'U')[dy > 0], '')[dy == 0]
        )
        super().move(direction)


def solve() -> int:

    head = Knot()
    for _ in range(9):
        head.add_tail(Tail())

    with open(filename, 'r') as f:
        for line in f:
            direction, repeats = line.split(' ')
            repeats = int(repeats)

            for _ in range(repeats):
                head.move(direction)

        first_tail, last_tail = head[1], head[9]

        return len(set(first_tail.history)), len(set(last_tail.history))


if __name__ == "__main__":
    part1, part2 = solve()
    print("ANSWER:",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
