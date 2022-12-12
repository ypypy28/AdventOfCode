import math
import sys
import typing
from heapq import nlargest


filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


class Monkey:
    def __init__(
        self, starting_items: list[int],
        operation: typing.Callable,
        test: tuple[int, int, int],
        can_calm: bool = True
    ) -> None:
        self.inspections = 0
        self.items = starting_items
        self.op = operation
        self.divisor, *self._not_ok_or_ok = test
        self.can_calm = can_calm

    def round(self, monkeys: list["Monkey"], LCM_DIV: int) -> None:
        self.inspections += len(self.items)
        for item in self.items:
            item = self.op(item) % LCM_DIV
            item //= 3 if self.can_calm else 1
            next_monkey_id = self._not_ok_or_ok[item % self.divisor == 0]
            monkeys[next_monkey_id].receive(item)
        self.items.clear()

    def receive(self, item: int) -> None:
        self.items.append(item)

    def __repr__(self):
        return f"Monkey: {', '.join((str(it) for it in self.items))} inspections: {self.inspections}"


def read_monkey(file: typing.TextIO) -> list[str]:
    monkey = []
    while (line:=file.readline().strip()) not in ('\n', ''):
        monkey.append(line)
    return monkey


def parse_operation(example: str) -> typing.Callable:
    arg1, op, arg2 = example.partition('=')[2].split()

    operation: typing.Callable[[int], int]
    match op, arg1, arg2:
        case '+', "old", "old":
            def operation(old: int) -> int:
                return old + old
        case '+', "old", n:
            num = int(n)
            def operation(old: int) -> int:
                return old + num
        case '-', "old", "old":
            def operation(old: int) -> int:
                return 0
        case '-', "old", n:
            num = int(n)
            def operation(old: int) -> int:
                return old - num
        case '*', "old", "old":
            def operation(old: int) -> int:
                return old * old
        case '*', "old", n:
            num = int(n)
            def operation(old: int) -> int:
                return old * num
        case _:
            raise NotImplementedError

    return operation


def parse_test(example: list[str]) -> tuple[int, int, int]:
    if "divisible" not in example[0]:
        raise NotImplementedError

    divisor, ok, not_ok = tuple(int(line.rpartition(' ')[2]) for line in example)
    return divisor, not_ok, ok


def create_monkey(monkey_data: list[str], can_calm: bool):
    start_items = [int(it)
                   for it in (monkey_data[1]
                              .removeprefix('Starting items: ')
                              .split(', '))]
    operation = parse_operation(monkey_data[2].removeprefix("Operation: "))
    test = parse_test(monkey_data[3:6])

    return Monkey(start_items, operation, test, can_calm)


def play(rounds: int, can_calm: bool=True) -> int:
    monkeys = []
    with open(filename, 'r') as f:
        monkey_data = read_monkey(f)
        while len(monkey_data) == 6:
            monkeys.append(create_monkey(monkey_data, can_calm))
            monkey_data = read_monkey(f)

    LCM_DIV = math.lcm(*(monkey.divisor for monkey in monkeys))

    interesting_rounds = {20, 1000, 2000, 3000, 4000,
                          5000, 6000, 7000, 8000, 9000, 10000}

    for i in range(1, rounds+1):
        for monkey in monkeys:
            monkey.round(monkeys, LCM_DIV)
        if i in interesting_rounds:
            show_state(i, can_calm, monkeys)

    two_largest = nlargest(2, monkeys, key=lambda m: m.inspections)
    return two_largest[0].inspections * two_largest[1].inspections


def show_state(round: int, can_calm: bool, monkeys: list[Monkey]) -> None:
    print(
        f"== After round {round} == ({can_calm=})",
        *(f"Monkey {i} inspected items {m.inspections} times."
          for i, m in enumerate(monkeys)),
        sep='\n',
        end='\n\n'
    )


def solve() -> tuple[int, int]:
    # return play(rounds=20), play(rounds=10000, can_calm=False)
    return play(rounds=20), play(rounds=10000, can_calm=False)


if __name__ == "__main__":
    part1, part2 = solve()

    print("ANSWER:",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
