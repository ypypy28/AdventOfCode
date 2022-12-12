import operator
import sys
import typing
from heapq import nlargest


filename = sys.argv[1] if len(sys.argv) > 1 else "test_input.txt"


class Monkey:
    def __init__(
        self, starting_items: list[int],
        operation: typing.Callable,
        test: typing.Callable,
        can_calm: bool = True
    ) -> None:
        self.inspections = 0
        self.items = starting_items
        self.op = operation
        self.test = test
        if can_calm:
            self.calm = lambda val: val // 3
        else:
            self.calm = lambda val: val

    def round(self, monkeys: list["Monkey"]) -> None:
        for item in self.items:
            self.inspections += 1
            item = self.op(item)
            item = self.calm(item)
            next_monkey_id = self.test(item)
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

    match op:
        case '+':
            op = operator.add
        case '-':
            op = operator.sub
        case '*':
            op = operator.mul
        case _:
            raise NotImplementedError

    match arg1, arg2:
        case "old", "old":
            return lambda old: op(old, old)
        case "old", num:
            num = int(num)
            return lambda old: op(old, num)
        case _:
            raise ValueError(f"bad args {arg1=}, {arg2=} {example=}")


def parse_test(example: list[str]) -> typing.Callable:
    if "divisible" not in example[0]:
        raise NotImplementedError

    divisor, ok, not_ok = (int(line.rpartition(' ')[2]) for line in example)

    def test(val):
        return ok if val % divisor == 0 else not_ok
    return test


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

    interesting_rounds = {20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000}

    for i in range(rounds):
        for monkey in monkeys:
            monkey.round(monkeys)
        if i+1 in interesting_rounds:
            show_state(i+1, can_calm, monkeys)



    two_largest = nlargest(2, monkeys, key=lambda m: m.inspections)
    return two_largest[0].inspections * two_largest[1].inspections


def show_state(round: int, can_calm: bool, monkeys: list[Monkey]) -> None:
    print(
        f"\n== After round {round} == ({can_calm=})",
        *(f"Monkey {i} inspected items {m.inspections} times."
          for i, m in enumerate(monkeys)),
        sep='\n'
    )


def solve() -> tuple[int, int]:
    return play(rounds=20), play(rounds=10000, can_calm=False)


if __name__ == "__main__":
    part1, part2 = solve()

    print("ANSWER:",
          f"Part 1: {part1}",
          f"Part 2: {part2}",
          sep='\n')
