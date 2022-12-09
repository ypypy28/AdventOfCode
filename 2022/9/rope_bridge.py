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

    def move(self, direction: str) -> None:
        dx, dy = DIRECTIONS[direction]
        self.x += dx
        self.y += dy
        self.history.append((self.x, self.y))


class Tail(Knot):
    def __init__(self, head: Knot, x=0, y=0):
        super().__init__(x, y)
        self.__head = head

    def move(self) -> None:
        dx = self.__head.x - self.x
        dy = self.__head.y - self.y
        if abs(dx) < 2 and abs(dy) < 2:
            return

        direction: str = (
            (('L', 'R')[dx > 0], '')[dx == 0]
            + (('D', 'U')[dy > 0], '')[dy == 0]
        )
        super().move(direction)


def solve() -> int:

    head = Knot()
    tail = Tail(head)

    with open(filename, 'r') as f:
        for line in f:
            direction, repeats = line.split(' ')
            repeats = int(repeats)

            for _ in range(repeats):
                head.move(direction)
                tail.move()

        return len(set(tail.history))


if __name__ == "__main__":
    part1 = solve()
    print("ANSWER:",
          f"Part 1: {part1}",
          sep='\n')
